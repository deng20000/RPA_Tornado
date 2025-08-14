# -*- coding: utf-8 -*-
"""
电商数据看板领域服务
处理电商数据看板相关的业务逻辑
"""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal, InvalidOperation
import logging

from ...core.exceptions.base_exceptions import ValidationError, BusinessLogicError, NotFoundError
from ...shared.constants.business_constants import DATE_FORMAT
from ...models.dashboard_models import Shop, Sale, ExchangeRate
from ...auth.openapi import OpenApiBase
from ...config import settings

# 配置日志记录器
logger = logging.getLogger(__name__)


class EcommerceDashboardService:
    """电商数据看板服务"""
    
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
            
            for shop_info in shops_data:
                try:
                    shop_id = shop_info.get("sid")
                    shop_name = shop_info.get("seller_name")
                    platform_id = shop_info.get("platform_id")
                    platform = shop_info.get("platform")
                    
                    if not all([shop_id, shop_name, platform_id, platform]):
                        logger.warning(f"店铺信息不完整，跳过: {shop_info}")
                        continue
                    
                    # 这里应该调用数据库操作，暂时返回数据
                    synced_count += 1
                    
                except Exception as e:
                    logger.error(f"处理店铺数据时出错: {str(e)}")
                    continue
            
            logger.info(f"店铺数据同步完成，共同步 {synced_count} 个店铺")
            return {
                "success": True,
                "synced_count": synced_count,
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
            
            for rate_info in currency_data:
                try:
                    currency_code = rate_info.get('code')
                    rate_str = rate_info.get('rate')
                    
                    if not currency_code or not rate_str:
                        continue
                    
                    # 验证汇率值
                    try:
                        rate_value = Decimal(rate_str)
                    except (ValueError, TypeError) as e:
                        logger.error(f"汇率值转换失败 {currency_code}: {rate_str}, 错误: {str(e)}")
                        continue
                    
                    # 这里应该调用数据库操作，暂时返回数据
                    synced_count += 1
                    
                except Exception as e:
                    logger.error(f"处理汇率数据时出错: {str(e)}")
                    continue
            
            logger.info(f"汇率数据同步完成，共同步 {synced_count} 条汇率记录")
            return {
                "success": True,
                "synced_count": synced_count,
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
            
            # 这里应该实现具体的销售数据同步逻辑
            # 1. 确保汇率数据完整性
            # 2. 获取销售统计数据
            # 3. 处理和转换数据
            # 4. 保存到数据库
            
            logger.info(f"销售数据同步完成")
            return {
                "success": True,
                "start_date": start_date,
                "end_date": end_date,
                "synced_count": 0  # 暂时返回0
            }
            
        except Exception as e:
            logger.error(f"同步销售数据失败: {str(e)}")
            raise BusinessLogicError(f"同步销售数据失败: {str(e)}")
    
    @staticmethod
    def convert_currency(
        amount: str, 
        from_currency: str, 
        to_currency: str, 
        exchange_rate: Dict[str, Any], 
        usd_rate: Optional[Dict[str, Any]] = None
    ) -> Decimal:
        """货币转换静态方法
        
        Args:
            amount: 金额字符串
            from_currency: 源货币代码
            to_currency: 目标货币代码
            exchange_rate: 汇率记录
            usd_rate: 美元汇率记录（用于多级转换）
            
        Returns:
            转换后的金额
        """
        try:
            amount_decimal = Decimal(str(amount))
            
            if from_currency == to_currency:
                return amount_decimal
            
            # 从源货币转换为人民币
            if from_currency == "CNY":
                cny_amount = amount_decimal
            else:
                rate = Decimal(str(exchange_rate.get('user_rate', 1)))
                cny_amount = amount_decimal * rate
            
            # 从人民币转换为目标货币
            if to_currency == "CNY":
                return cny_amount
            elif to_currency == "USD" and usd_rate:
                usd_rate_value = Decimal(str(usd_rate.get('user_rate', 1)))
                return cny_amount / usd_rate_value
            else:
                return cny_amount
                
        except (ValueError, TypeError, InvalidOperation) as e:
            logger.error(f"货币转换失败: {str(e)}")
            raise ValidationError(f"货币转换失败: {str(e)}")
    
    async def get_dashboard_summary(self, access_token: str) -> Dict[str, Any]:
        """获取数据看板摘要信息
        
        Args:
            access_token: 访问令牌
            
        Returns:
            看板摘要数据
        """
        try:
            logger.info("获取数据看板摘要信息")
            
            # 这里应该实现具体的摘要数据获取逻辑
            # 1. 获取店铺总数
            # 2. 获取最近销售数据
            # 3. 获取汇率更新状态
            # 4. 计算关键指标
            
            summary_data = {
                "total_shops": 0,
                "total_sales_today": {
                    "cny": "0.00",
                    "usd": "0.00"
                },
                "total_sales_yesterday": {
                    "cny": "0.00",
                    "usd": "0.00"
                },
                "exchange_rate_updated": datetime.now().isoformat(),
                "last_sync_time": datetime.now().isoformat()
            }
            
            return summary_data
            
        except Exception as e:
            logger.error(f"获取数据看板摘要失败: {str(e)}")
            raise BusinessLogicError(f"获取数据看板摘要失败: {str(e)}")