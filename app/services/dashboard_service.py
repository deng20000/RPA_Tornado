# -*- coding: utf-8 -*-
"""
电商数据看板服务类
提供电商数据看板相关的业务逻辑处理
"""

import asyncio
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal, InvalidOperation
import logging
import json
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc

from ..core.exceptions.base_exceptions import ValidationError, BusinessLogicError, NotFoundError
from ..shared.constants.business_constants import DATE_FORMAT
from ..models.dashboard_models import Shop, Sale, ExchangeRate
from ..auth.openapi import OpenApiBase
from ..config import settings
from ..core.database import get_db_session

# 配置日志记录器
logger = logging.getLogger(__name__)


class DashboardService:
    """电商数据看板服务类"""
    
    def __init__(self):
        """初始化服务"""
        self.api = OpenApiBase(settings.LLX_API_HOST, settings.LLX_APP_ID, settings.LLX_APP_SECRET)
    
    async def sync_shop_data(self, access_token: str) -> Dict[str, Any]:
        """同步店铺数据
        
        Args:
            access_token: 访问令牌
            
        Returns:
            同步结果
        """
        try:
            logger.info("开始同步店铺数据")
            
            # 调用API获取店铺列表
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/seller/lists",
                method="GET",
                req_body=None
            )
            
            resp_data = resp.model_dump()
            
            # 检查API响应状态
            if resp_data.get("code") != 0:
                raise BusinessLogicError(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            
            # 提取店铺数据
            shops_data = resp_data.get("data", [])
            synced_count = 0
            updated_count = 0
            
            # 获取数据库会话
            with get_db_session() as session:
                for shop_info in shops_data:
                    try:
                        shop_id = shop_info.get("sid")
                        shop_name = shop_info.get("seller_name")
                        platform_id = shop_info.get("platform_id")
                        platform = shop_info.get("platform")
                        
                        if not all([shop_id, shop_name, platform_id, platform]):
                            logger.warning(f"店铺信息不完整，跳过: {shop_info}")
                            continue
                        
                        # 检查店铺是否已存在
                        existing_shop = session.query(Shop).filter(
                            and_(
                                Shop.shop_id == shop_id,
                                Shop.platform_id == platform_id
                            )
                        ).first()
                        
                        if existing_shop:
                            # 更新现有店铺信息
                            existing_shop.shop_name = shop_name
                            existing_shop.platform = platform
                            existing_shop.updated_at = datetime.now()
                            updated_count += 1
                        else:
                            # 创建新店铺记录
                            new_shop = Shop(
                                shop_id=shop_id,
                                shop_name=shop_name,
                                platform_id=platform_id,
                                platform=platform,
                                status='active'
                            )
                            session.add(new_shop)
                            synced_count += 1
                        
                    except Exception as e:
                        logger.error(f"处理店铺数据时出错: {str(e)}")
                        continue
                
                # 提交事务
                session.commit()
            
            logger.info(f"店铺数据同步完成，新增 {synced_count} 个店铺，更新 {updated_count} 个店铺")
            return {
                "success": True,
                "synced_count": synced_count,
                "updated_count": updated_count,
                "total_count": len(shops_data)
            }
            
        except Exception as e:
            logger.error(f"同步店铺数据失败: {str(e)}")
            raise BusinessLogicError(f"同步店铺数据失败: {str(e)}")
    
    async def sync_exchange_rate_data(self, access_token: str, target_date: Optional[str] = None) -> Dict[str, Any]:
        """同步汇率数据
        
        Args:
            access_token: 访问令牌
            target_date: 目标日期，格式为 YYYY-MM，默认为昨天所在月份
            
        Returns:
            同步结果
        """
        try:
            # 如果没有提供日期，默认使用昨天所在月份
            if target_date is None:
                yesterday = datetime.now() - timedelta(days=1)
                target_date = yesterday.strftime("%Y-%m")
            
            logger.info(f"开始同步汇率数据，目标月份: {target_date}")
            
            # 构建请求参数
            query_data = {
                "date": target_date
            }
            
            # 调用API获取汇率数据
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/finance/currency/currencyMonth",
                method="POST",
                req_body=query_data
            )
            
            resp_data = resp.model_dump()
            
            # 检查API响应状态
            if resp_data.get("code") != 0:
                raise BusinessLogicError(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            
            # 提取汇率数据
            currency_data = resp_data.get("data", [])
            synced_count = 0
            updated_count = 0
            
            # 获取数据库会话
            with get_db_session() as session:
                for rate_info in currency_data:
                    try:
                        currency_code = rate_info.get('code')
                        rate_str = rate_info.get('rate')
                        currency_name = rate_info.get('name', currency_code)
                        
                        if not currency_code or not rate_str:
                            continue
                        
                        # 验证汇率值
                        try:
                            rate_value = Decimal(rate_str)
                        except (ValueError, TypeError) as e:
                            logger.error(f"汇率值转换失败 {currency_code}: {rate_str}, 错误: {str(e)}")
                            continue
                        
                        # 解析目标日期
                        rate_date = datetime.strptime(f"{target_date}-01", "%Y-%m-%d")
                        
                        # 检查汇率是否已存在
                        existing_rate = session.query(ExchangeRate).filter(
                            and_(
                                ExchangeRate.currency_code == currency_code,
                                ExchangeRate.rate_date == rate_date,
                                ExchangeRate.base_currency == 'CNY'
                            )
                        ).first()
                        
                        if existing_rate:
                            # 更新现有汇率
                            existing_rate.rate = rate_value
                            existing_rate.currency_name = currency_name
                            existing_rate.updated_at = datetime.now()
                            updated_count += 1
                        else:
                            # 创建新汇率记录
                            new_rate = ExchangeRate(
                                currency_code=currency_code,
                                currency_name=currency_name,
                                base_currency='CNY',
                                rate=rate_value,
                                rate_date=rate_date,
                                effective_date=rate_date,
                                source='api',
                                status='active'
                            )
                            session.add(new_rate)
                            synced_count += 1
                        
                    except Exception as e:
                        logger.error(f"处理汇率数据时出错: {str(e)}")
                        continue
                
                # 提交事务
                session.commit()
            
            logger.info(f"汇率数据同步完成，新增 {synced_count} 条汇率记录，更新 {updated_count} 条记录")
            return {
                "success": True,
                "synced_count": synced_count,
                "updated_count": updated_count,
                "total_count": len(currency_data),
                "target_date": target_date
            }
            
        except Exception as e:
            logger.error(f"同步汇率数据失败: {str(e)}")
            raise BusinessLogicError(f"同步汇率数据失败: {str(e)}")
    
    async def sync_sales_data_with_period(
        self, 
        access_token: str,
        start_date: Optional[str] = None, 
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """同步指定时间区间的销售数据
        
        Args:
            access_token: 访问令牌
            start_date: 开始日期，格式为 YYYY-MM-DD，默认为昨天
            end_date: 结束日期，格式为 YYYY-MM-DD，默认为昨天
            
        Returns:
            同步结果
        """
        try:
            # 如果没有指定日期，使用昨天的日期
            if start_date is None or end_date is None:
                yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                start_date = start_date or yesterday
                end_date = end_date or yesterday
            
            logger.info(f"开始同步销售数据，时间区间: {start_date} 到 {end_date}")
            
            # 验证日期格式
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError as e:
                raise ValidationError(f"日期格式错误: {str(e)}")
            
            if start_date_obj > end_date_obj:
                raise ValidationError("开始日期不能大于结束日期")
            
            # 1. 确保汇率数据完整性
            await self._ensure_exchange_rates_for_period(access_token, start_date_obj, end_date_obj)
            
            # 2. 获取销售统计数据
            sales_data = await self._get_sales_stats(access_token, start_date, end_date)
            
            # 3. 处理和转换数据
            synced_count = await self._process_sales_data(sales_data, start_date_obj, end_date_obj)
            
            logger.info(f"销售数据同步完成，共处理 {synced_count} 条记录")
            return {
                "success": True,
                "start_date": start_date,
                "end_date": end_date,
                "synced_count": synced_count
            }
            
        except Exception as e:
            logger.error(f"同步销售数据失败: {str(e)}")
            raise BusinessLogicError(f"同步销售数据失败: {str(e)}")
    
    async def _ensure_exchange_rates_for_period(self, access_token: str, start_date: date, end_date: date):
        """确保指定时间段内的汇率数据完整性
        
        Args:
            access_token: 访问令牌
            start_date: 开始日期
            end_date: 结束日期
        """
        try:
            # 获取时间段内需要的月份
            current_date = start_date.replace(day=1)
            end_month = end_date.replace(day=1)
            
            while current_date <= end_month:
                target_month = current_date.strftime("%Y-%m")
                
                # 检查该月份是否已有汇率数据
                with get_db_session() as session:
                    existing_rates = session.query(ExchangeRate).filter(
                        func.date_format(ExchangeRate.rate_date, '%Y-%m') == target_month
                    ).count()
                    
                    if existing_rates == 0:
                        logger.info(f"同步缺失的汇率数据: {target_month}")
                        await self.sync_exchange_rate_data(access_token, target_month)
                
                # 移动到下一个月
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1)
                    
        except Exception as e:
            logger.error(f"确保汇率数据完整性失败: {str(e)}")
            raise
    
    async def _get_sales_stats(self, access_token: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """获取销售统计数据
        
        Args:
            access_token: 访问令牌
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            销售统计数据列表
        """
        try:
            # 构建请求参数
            query_data = {
                "start_date": start_date,
                "end_date": end_date
            }
            
            # 调用API获取销售统计数据
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/finance/sales/statistics",
                method="POST",
                req_body=query_data
            )
            
            resp_data = resp.model_dump()
            
            # 检查API响应状态
            if resp_data.get("code") != 0:
                raise BusinessLogicError(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")
            
            return resp_data.get("data", [])
            
        except Exception as e:
            logger.error(f"获取销售统计数据失败: {str(e)}")
            raise
    
    async def _process_sales_data(self, sales_data: List[Dict[str, Any]], start_date: date, end_date: date) -> int:
        """处理销售数据
        
        Args:
            sales_data: 销售数据列表
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            处理的记录数
        """
        try:
            synced_count = 0
            
            with get_db_session() as session:
                for sale_info in sales_data:
                    try:
                        # 提取销售数据字段
                        shop_id = sale_info.get('shop_id')
                        sale_date_str = sale_info.get('sale_date')
                        original_amount = sale_info.get('amount')
                        original_currency = sale_info.get('currency', 'CNY')
                        order_id = sale_info.get('order_id')
                        product_id = sale_info.get('product_id')
                        
                        if not all([shop_id, sale_date_str, original_amount]):
                            continue
                        
                        # 解析销售日期
                        sale_date = datetime.strptime(sale_date_str, "%Y-%m-%d")
                        
                        # 获取店铺信息
                        shop = session.query(Shop).filter(Shop.shop_id == shop_id).first()
                        if not shop:
                            logger.warning(f"未找到店铺: {shop_id}")
                            continue
                        
                        # 货币转换
                        cny_amount, usd_amount, exchange_rate = await self._convert_currency(
                            session, original_amount, original_currency, sale_date
                        )
                        
                        # 检查销售记录是否已存在
                        existing_sale = session.query(Sale).filter(
                            and_(
                                Sale.shop_id == shop.id,
                                Sale.sale_date == sale_date,
                                Sale.order_id == order_id,
                                Sale.product_id == product_id
                            )
                        ).first()
                        
                        if not existing_sale:
                            # 创建新销售记录
                            new_sale = Sale(
                                shop_id=shop.id,
                                sale_date=sale_date,
                                order_id=order_id,
                                product_id=product_id,
                                product_name=sale_info.get('product_name'),
                                original_amount=Decimal(str(original_amount)),
                                original_currency=original_currency,
                                cny_amount=cny_amount,
                                usd_amount=usd_amount,
                                exchange_rate=exchange_rate,
                                exchange_rate_date=sale_date,
                                quantity=sale_info.get('quantity', 1),
                                raw_data=json.dumps(sale_info)
                            )
                            session.add(new_sale)
                            synced_count += 1
                        
                    except Exception as e:
                        logger.error(f"处理销售记录时出错: {str(e)}")
                        continue
                
                # 提交事务
                session.commit()
            
            return synced_count
            
        except Exception as e:
            logger.error(f"处理销售数据失败: {str(e)}")
            raise
    
    async def _convert_currency(
        self, 
        session: Session, 
        amount: str, 
        from_currency: str, 
        sale_date: datetime
    ) -> Tuple[Decimal, Optional[Decimal], Optional[Decimal]]:
        """货币转换
        
        Args:
            session: 数据库会话
            amount: 金额
            from_currency: 源货币
            sale_date: 销售日期
            
        Returns:
            (人民币金额, 美元金额, 使用的汇率)
        """
        try:
            amount_decimal = Decimal(str(amount))
            
            if from_currency == 'CNY':
                cny_amount = amount_decimal
                exchange_rate = Decimal('1.0')
            else:
                # 获取汇率
                rate_record = ExchangeRate.get_rate_by_date(
                    session, from_currency, sale_date, 'CNY'
                )
                
                if not rate_record:
                    logger.warning(f"未找到汇率: {from_currency} -> CNY, 日期: {sale_date}")
                    return amount_decimal, None, None
                
                exchange_rate = rate_record.rate
                cny_amount = amount_decimal * exchange_rate
            
            # 转换为美元
            usd_rate_record = ExchangeRate.get_rate_by_date(
                session, 'USD', sale_date, 'CNY'
            )
            
            if usd_rate_record:
                usd_amount = cny_amount / usd_rate_record.rate
            else:
                usd_amount = None
            
            return cny_amount, usd_amount, exchange_rate
            
        except Exception as e:
            logger.error(f"货币转换失败: {str(e)}")
            raise
    
    async def get_dashboard_summary(self, access_token: str) -> Dict[str, Any]:
        """获取数据看板摘要信息
        
        Args:
            access_token: 访问令牌
            
        Returns:
            看板摘要数据
        """
        try:
            logger.info("获取数据看板摘要信息")
            
            with get_db_session() as session:
                # 获取店铺总数
                total_shops = session.query(Shop).filter(Shop.status == 'active').count()
                
                # 获取今天和昨天的日期
                today = datetime.now().date()
                yesterday = today - timedelta(days=1)
                
                # 获取今天的销售数据
                today_sales = session.query(
                    func.sum(Sale.cny_amount).label('total_cny'),
                    func.sum(Sale.usd_amount).label('total_usd'),
                    func.count(Sale.id).label('order_count')
                ).filter(
                    func.date(Sale.sale_date) == today
                ).first()
                
                # 获取昨天的销售数据
                yesterday_sales = session.query(
                    func.sum(Sale.cny_amount).label('total_cny'),
                    func.sum(Sale.usd_amount).label('total_usd'),
                    func.count(Sale.id).label('order_count')
                ).filter(
                    func.date(Sale.sale_date) == yesterday
                ).first()
                
                # 获取最新汇率更新时间
                latest_rate = session.query(ExchangeRate).filter(
                    ExchangeRate.status == 'active'
                ).order_by(desc(ExchangeRate.updated_at)).first()
                
                summary_data = {
                    "total_shops": total_shops,
                    "total_sales_today": {
                        "cny": str(today_sales.total_cny or 0),
                        "usd": str(today_sales.total_usd or 0),
                        "order_count": today_sales.order_count or 0
                    },
                    "total_sales_yesterday": {
                        "cny": str(yesterday_sales.total_cny or 0),
                        "usd": str(yesterday_sales.total_usd or 0),
                        "order_count": yesterday_sales.order_count or 0
                    },
                    "exchange_rate_updated": latest_rate.updated_at.isoformat() if latest_rate else None,
                    "last_sync_time": datetime.now().isoformat()
                }
            
            return summary_data
            
        except Exception as e:
            logger.error(f"获取数据看板摘要失败: {str(e)}")
            raise BusinessLogicError(f"获取数据看板摘要失败: {str(e)}")
    
    async def get_shop_list(self, page: int = 1, page_size: int = 20, platform: Optional[str] = None) -> Dict[str, Any]:
        """获取店铺列表
        
        Args:
            page: 页码
            page_size: 每页数量
            platform: 平台筛选
            
        Returns:
            店铺列表数据
        """
        try:
            with get_db_session() as session:
                # 构建查询条件
                query = session.query(Shop).filter(Shop.status == 'active')
                
                if platform:
                    query = query.filter(Shop.platform == platform)
                
                # 获取总数
                total = query.count()
                
                # 分页查询
                shops = query.order_by(desc(Shop.created_at)).offset(
                    (page - 1) * page_size
                ).limit(page_size).all()
                
                # 转换为字典格式
                shop_list = [shop.to_dict() for shop in shops]
                
                return {
                    "shops": shop_list,
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": (total + page_size - 1) // page_size
                }
                
        except Exception as e:
            logger.error(f"获取店铺列表失败: {str(e)}")
            raise BusinessLogicError(f"获取店铺列表失败: {str(e)}")
    
    async def get_sales_statistics(
        self, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        shop_id: Optional[str] = None,
        currency: str = 'CNY'
    ) -> Dict[str, Any]:
        """获取销售统计
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            shop_id: 店铺ID
            currency: 货币类型
            
        Returns:
            销售统计数据
        """
        try:
            with get_db_session() as session:
                # 构建查询条件
                query = session.query(Sale)
                
                if start_date:
                    query = query.filter(Sale.sale_date >= datetime.strptime(start_date, "%Y-%m-%d"))
                
                if end_date:
                    query = query.filter(Sale.sale_date <= datetime.strptime(end_date, "%Y-%m-%d"))
                
                if shop_id:
                    shop = session.query(Shop).filter(Shop.shop_id == shop_id).first()
                    if shop:
                        query = query.filter(Sale.shop_id == shop.id)
                
                # 根据货币类型选择金额字段
                amount_field = Sale.cny_amount if currency == 'CNY' else Sale.usd_amount
                
                # 计算统计数据
                stats = query.with_entities(
                    func.sum(amount_field).label('total_sales'),
                    func.count(Sale.id).label('total_orders'),
                    func.avg(amount_field).label('avg_order_value')
                ).first()
                
                # 按店铺分组统计
                shop_stats = query.join(Shop).with_entities(
                    Shop.shop_name,
                    Shop.platform,
                    func.sum(amount_field).label('shop_sales'),
                    func.count(Sale.id).label('shop_orders')
                ).group_by(Shop.id, Shop.shop_name, Shop.platform).all()
                
                return {
                    "total_sales": str(stats.total_sales or 0),
                    "total_orders": stats.total_orders or 0,
                    "average_order_value": str(stats.avg_order_value or 0),
                    "currency": currency,
                    "period": {
                        "start_date": start_date,
                        "end_date": end_date
                    },
                    "shop_breakdown": [
                        {
                            "shop_name": stat.shop_name,
                            "platform": stat.platform,
                            "sales": str(stat.shop_sales or 0),
                            "orders": stat.shop_orders or 0
                        }
                        for stat in shop_stats
                    ]
                }
                
        except Exception as e:
            logger.error(f"获取销售统计失败: {str(e)}")
            raise BusinessLogicError(f"获取销售统计失败: {str(e)}")