# 导入所需的库和模块
import platform
from sqlalchemy import create_engine, text, Column, String, Integer, Date, DECIMAL, TIMESTAMP, ForeignKey, UniqueConstraint, Index, func, Numeric, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict, Any
import logging
import json
import requests
from jsonpath_ng import parse
import sys

# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建SQLAlchemy基类
Base = declarative_base()

# 模型定义
class Shop(Base):
    """店铺模型类
    
    用于存储店铺的基本信息，包括店铺ID、名称、平台ID和平台名称等
    """
    __tablename__ = 'shops'
    
    # 定义表字段
    shop_id = Column(String(50), primary_key=True)  # 店铺唯一标识符
    shop_name = Column(String(100), nullable=False)  # 店铺名称
    platform_id = Column(String(20), nullable=False)  # 平台ID
    platform = Column(String(50), nullable=False)    # 平台名称
    created_at = Column(TIMESTAMP, default=datetime.now)  # 创建时间
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)  # 更新时间
    
    # 定义与销售记录的一对多关系
    sales = relationship("Sale", back_populates="shop")
    
    # 定义索引
    __table_args__ = (
        Index('idx_shops_platform', 'platform_id'),  # 平台ID索引
        Index('idx_shops_name', 'platform'),        # 平台名称索引
    )

class Sale(Base):
    """销售记录模型类
    
    用于存储店铺的销售记录，包括销售ID、店铺ID、销售日期、销售金额等
    """
    __tablename__ = 'sales'
    
    # 定义表字段
    sale_id = Column(Integer, primary_key=True, autoincrement=True)     # 销售记录ID（自增主键）
    shop_id = Column(String(50), ForeignKey('shops.shop_id'), nullable=False)  # 关联的店铺ID
    sale_date = Column(Date, nullable=False)        # 销售日期
    cny_amount = Column(DECIMAL(12,2), nullable=False)  # 人民币金额
    usd_amount = Column(DECIMAL(12,2), nullable=False)  # 美元金额
    entry_time = Column(TIMESTAMP, default=datetime.now)  # 记录创建时间
    
    # 定义与店铺的多对一关系
    shop = relationship("Shop", back_populates="sales")
    
    # 定义唯一约束：确保每个店铺在同一天只有一条销售记录
    __table_args__ = (
        UniqueConstraint('shop_id', 'sale_date', name='uq_shop_date'),
    )

class ExchangeRate(Base):
    """汇率模型类
    
    用于存储不同货币的汇率信息，包括货币代码、汇率值、更新时间等
    """
    __tablename__ = 'exchange_rate'
    
    # 定义表字段
    id = Column(Integer, primary_key=True)          # 主键ID
    date = Column(Date, nullable=False)             # 汇率日期
    currency_code = Column(String(3))               # 货币代码（如：USD）
    currency_icon = Column(String(10))              # 货币图标
    currency_name = Column(String(50))              # 货币名称
    user_rate = Column(DECIMAL(20,10), nullable=False)  # 用户设置的汇率值
    update_time = Column(TIMESTAMP, default=datetime.now)  # 更新时间
    org_rate = Column(DECIMAL(20,10))              # 原始汇率值
    
    # 定义约束和索引
    __table_args__ = (
        # 确保同一货币在同一天只有一条汇率记录
        UniqueConstraint('currency_code', 'date', name='uniq_currency_date'),
        # 货币代码索引
        Index('idx_exchange_currency', 'currency_code'),
        # 日期索引
        Index('idx_exchange_date', 'date'),
    )

# 数据库连接配置
DATABASE_URL = "postgresql://postgres:a123456@localhost:5432/postgres"

def get_db_engine(echo=True):
    """创建并返回数据库引擎实例
    
    Args:
        echo (bool): 是否启用SQL语句输出，默认为True
        
    Returns:
        Engine: SQLAlchemy引擎实例
        
    Raises:
        Exception: 当数据库引擎创建失败时抛出异常
    """
    try:
        engine = create_engine(DATABASE_URL, echo=echo)
        return engine
    except Exception as e:
        logger.error(f"数据库引擎创建失败: {str(e)}")
        raise

class DatabaseManager:
    """数据库管理类
    
    用于管理数据库连接、会话创建以及数据库操作
    """
    def __init__(self):
        """初始化数据库管理器
        
        创建数据库引擎和会话工厂
        """
        self.engine = get_db_engine()
        self.Session = sessionmaker(bind=self.engine)
        
    # def drop_tables(self):
    #     """删除所有数据库表"""
    #     try:
    #         Base.metadata.drop_all(self.engine)
    #         logger.info("数据库表删除成功")
    #     except Exception as e:
    #         logger.error(f"数据库表删除失败: {str(e)}")
    #         raise
            
    def init_db(self):
        """初始化数据库表结构
        
        根据模型类定义创建所有数据库表。如果表已存在，则不会重新创建。
        
        Raises:
            Exception: 当表创建失败时抛出异常
        """
        try:
            Base.metadata.create_all(self.engine)
            logger.info("数据库表创建成功")
        except Exception as e:
            logger.error(f"数据库表创建失败: {str(e)}")
            raise
            
    def add_shop(self, shop_id: str, platform_id: str, shop_name: str, platform: str) -> Optional[Shop]:
        """添加新店铺到数据库
        
        Args:
            shop_id (str): 店铺唯一标识符
            platform_id (str): 平台ID
            shop_name (str): 店铺名称
            platform (str): 平台名称
            
        Returns:
            Optional[Shop]: 成功时返回新创建的店铺对象副本，失败时返回None
            
        Raises:
            Exception: 当店铺添加失败时抛出异常
        """
        session = self.Session()
        try:
            # 创建新的店铺对象
            shop = Shop(
                shop_id=shop_id,
                platform_id=platform_id,
                shop_name=shop_name,
                platform=platform
            )
            # 添加到会话并提交
            session.add(shop)
            session.commit()
            
            # 刷新对象以确保所有属性都已加载
            session.refresh(shop)
            
            # 创建对象副本以避免会话关闭后的访问问题
            shop_copy = Shop(
                shop_id=shop.shop_id,
                platform_id=shop.platform_id,
                shop_name=shop.shop_name,
                platform=shop.platform,
                created_at=shop.created_at,
                updated_at=shop.updated_at
            )
            logger.info(f"店铺添加成功: {shop_id}")
            return shop_copy
        except Exception as e:
            session.rollback()
            logger.error(f"店铺添加失败: {str(e)}")
            raise
        finally:
            session.close()
            
    def add_sale(self, sale_data: dict) -> Optional[Sale]:
        """添加销售记录到数据库
        
        Args:
            sale_data (dict): 包含销售记录信息的字典，必须包含以下字段：
                - sale_id: 销售记录ID
                - shop_id: 店铺ID
                - sale_date: 销售日期
                - cny_amount: 人民币金额
                - usd_amount: 美元金额
                
        Returns:
            Optional[Sale]: 成功时返回新创建的销售记录对象副本，失败时返回None
            
        Raises:
            Exception: 当销售记录添加失败时抛出异常
        """
        session = self.Session()
        try:
            # 创建新的销售记录对象
            sale = Sale(**sale_data)
            # 添加到会话并提交
            session.add(sale)
            session.commit()
            
            # 刷新对象以确保所有属性都已加载
            session.refresh(sale)
            
            # 创建对象副本以避免会话关闭后的访问问题
            sale_copy = Sale(
                sale_id=sale.sale_id,
                shop_id=sale.shop_id,
                sale_date=sale.sale_date,
                cny_amount=sale.cny_amount,
                usd_amount=sale.usd_amount,
                entry_time=sale.entry_time
            )
            logger.info(f"销售记录添加成功: {sale_data['sale_id']}")
            return sale_copy
        except Exception as e:
            session.rollback()
            logger.error(f"销售记录添加失败: {str(e)}")
            raise
        finally:
            session.close()
            
    def add_exchange_rate(self, rate_data: dict) -> Optional[ExchangeRate]:
        """添加汇率记录到数据库
        
        Args:
            rate_data (dict): 包含汇率信息的字典，必须包含以下字段：
                - date: 汇率日期
                - currency_code: 货币代码
                - user_rate: 用户设置的汇率值
                可选字段：
                - currency_icon: 货币图标
                - currency_name: 货币名称
                - org_rate: 原始汇率值
                
        Returns:
            Optional[ExchangeRate]: 成功时返回新创建的汇率记录对象副本，失败时返回None
            
        Raises:
            Exception: 当汇率记录添加失败时抛出异常
        """
        session = self.Session()
        try:
            # 创建新的汇率记录对象
            rate = ExchangeRate(**rate_data)
            # 添加到会话并提交
            session.add(rate)
            session.commit()
            
            # 刷新对象以确保所有属性都已加载
            session.refresh(rate)
            
            # 创建对象副本以避免会话关闭后的访问问题
            rate_copy = ExchangeRate(
                id=rate.id,
                date=rate.date,
                currency_code=rate.currency_code,
                currency_icon=rate.currency_icon,
                currency_name=rate.currency_name,
                user_rate=rate.user_rate,
                update_time=rate.update_time,
                org_rate=rate.org_rate
            )
            logger.info(f"汇率记录添加成功: {rate_data['currency_code']}-{rate_data['date']}")
            return rate_copy
        except Exception as e:
            session.rollback()
            logger.error(f"汇率记录添加失败: {str(e)}")
            raise
        finally:
            session.close()
            
    def get_shop_sales(self, shop_id: str, start_date: date, end_date: date) -> List[Sale]:
        """获取指定店铺在指定日期范围内的销售记录
        
        Args:
            shop_id (str): 店铺ID
            start_date (date): 开始日期
            end_date (date): 结束日期
            
        Returns:
            List[Sale]: 销售记录列表
        """
        session = self.Session()
        try:
            # 查询指定日期范围内的销售记录
            sales = session.query(Sale).filter(
                Sale.shop_id == shop_id,
                Sale.sale_date.between(start_date, end_date)
            ).all()
            return sales
        finally:
            session.close()
            
    def get_platform_total_sales(self, platform: str, date: date) -> Decimal:
        """获取指定平台在指定日期的总销售额（人民币）
        
        Args:
            platform (str): 平台名称
            date (date): 查询日期
            
        Returns:
            Decimal: 总销售额，如果没有记录则返回0.00
        """
        session = self.Session()
        try:
            # 联表查询计算总销售额
            total = session.query(func.sum(Sale.cny_amount)).join(Shop).filter(
                Shop.platform == platform,
                Sale.sale_date == date
            ).scalar()
            # 如果没有记录，返回0.00
            return Decimal('0.00') if total is None else total
        finally:
            session.close()
            
    def get_exchange_rate(self, currency_code: str, date: date) -> Optional[ExchangeRate]:
        """获取指定货币在指定日期（或之前最近日期）的汇率记录
        
        Args:
            currency_code (str): 货币代码（如：USD）
            date (date): 查询日期
            
        Returns:
            Optional[ExchangeRate]: 汇率记录对象，如果没有找到则返回None
        """
        session = self.Session()
        try:
            # 查询指定日期或之前最近的汇率记录
            rate = session.query(ExchangeRate).filter(
                ExchangeRate.currency_code == currency_code,
                ExchangeRate.date <= date
            ).order_by(ExchangeRate.date.desc()).first()
            return rate
        finally:
            session.close()
            
    def update_shop(self, shop_id: str, new_data: dict) -> bool:
        """更新店铺信息
        
        Args:
            shop_id (str): 要更新的店铺ID
            new_data (dict): 包含要更新的字段和值的字典
                可更新的字段包括：
                - shop_name: 店铺名称
                - platform_id: 平台ID
                - platform: 平台名称
            
        Returns:
            bool: 更新成功返回True，失败返回False
        """
        session = self.Session()
        try:
            # 查找要更新的店铺
            shop = session.query(Shop).filter(Shop.shop_id == shop_id).first()
            if not shop:
                logger.error(f"找不到店铺: {shop_id}")
                return False
            
            # 更新提供的字段
            for key, value in new_data.items():
                if hasattr(shop, key):
                    setattr(shop, key, value)
            
            # 提交更改
            session.commit()
            logger.info(f"店铺信息更新成功: {shop_id}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"店铺信息更新失败: {str(e)}")
            return False
        finally:
            session.close()
    
    def update_sale(self, sale_id: int, new_data: dict) -> bool:
        """更新销售记录信息
        
        Args:
            sale_id (int): 要更新的销售记录ID
            new_data (dict): 包含要更新的字段和值的字典
                可更新的字段包括：
                - shop_id: 店铺ID
                - sale_date: 销售日期
                - cny_amount: 人民币金额
                - usd_amount: 美元金额
            
        Returns:
            bool: 更新成功返回True，失败返回False
        """
        session = self.Session()
        try:
            # 查找要更新的销售记录
            sale = session.query(Sale).filter(Sale.sale_id == sale_id).first()
            if not sale:
                logger.error(f"找不到销售记录: {sale_id}")
                return False
            
            # 更新提供的字段
            for key, value in new_data.items():
                if hasattr(sale, key):
                    setattr(sale, key, value)
            
            # 提交更改
            session.commit()
            logger.info(f"销售记录更新成功: {sale_id}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"销售记录更新失败: {str(e)}")
            return False
        finally:
            session.close()
    
    def delete_shop(self, shop_id: str) -> bool:
        """删除指定店铺及其关联的销售记录
        
        Args:
            shop_id (str): 要删除的店铺ID
            
        Returns:
            bool: 删除成功返回True，失败返回False
            
        Note:
            由于外键约束，删除店铺时会自动删除该店铺的所有销售记录
        """
        session = self.Session()
        try:
            # 查找要删除的店铺
            shop = session.query(Shop).filter(Shop.shop_id == shop_id).first()
            if not shop:
                logger.error(f"找不到店铺: {shop_id}")
                return False
            
            # 删除店铺（会级联删除相关的销售记录）
            session.delete(shop)
            session.commit()
            logger.info(f"店铺删除成功: {shop_id}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"店铺删除失败: {str(e)}")
            return False
        finally:
            session.close()
    
    def delete_sale(self, sale_id: int) -> bool:
        """删除指定的销售记录
        
        Args:
            sale_id (int): 要删除的销售记录ID
            
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        session = self.Session()
        try:
            # 查找要删除的销售记录
            sale = session.query(Sale).filter(Sale.sale_id == sale_id).first()
            if not sale:
                logger.error(f"找不到销售记录: {sale_id}")
                return False
            
            # 删除销售记录
            session.delete(sale)
            session.commit()
            logger.info(f"销售记录删除成功: {sale_id}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"销售记录删除失败: {str(e)}")
            return False
        finally:
            session.close()

class GetData:
    """数据获取和处理类
    
    负责从API获取店铺、销售和汇率数据，并进行数据处理和同步到数据库
    """
    
    # API配置
    BASE_URL = "http://192.168.17.123:8888"  # API基础URL
    
    # API端点
    SELLER_LIST_ENDPOINT = "/api/basicOpen/platformStatisticsV2/saleStat/pageList/seller-list"  # 店铺列表接口
    AMAZON_SELLER_ENDPOINT = "/api/erp/sc/data/seller/lists" # 亚马逊店铺数据接口
    CURRENCY_ENDPOINT = "/api/erp/sc/routing/finance/currency/currencyMonth"  # 汇率数据接口
    SALES_STATS_ENDPOINT = "/api/basicOpen/platformStatisticsV2/saleStat/pageList"  # 销售统计接口
    
    @staticmethod
    def get_seller_list(offset: int = 0, length: int = 200) -> Dict[str, Any]:
        """
        从API获取店铺列表数据
        
        Args:
            offset: 起始位置，默认为0
            length: 获取数量，默认为200
            
        Returns:
            Dict[str, Any]: API返回的原始JSON数据
            
        Raises:
            requests.RequestException: 当API请求失败时
            ValueError: 当API返回的数据格式不正确时
        """
        url = f"{GetData.BASE_URL}{GetData.SELLER_LIST_ENDPOINT}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "offset": offset,
            "length": length,
            "is_sync": 1,
            "status": 1
        }
        
        logger.info(f"正在请求API: {url}")
        logger.info(f"请求参数: {json.dumps(payload, ensure_ascii=False)}")
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # 检查响应状态
            
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("API返回的数据格式不正确")
            
            # 打印返回的数据结构
            logger.info("API返回数据结构:")
            logger.info(json.dumps(data, ensure_ascii=False, indent=2))
                
            return data
            
        except requests.RequestException as e:
            logger.error(f"获取店铺列表失败: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"解析API响应失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"未预期的错误: {str(e)}")
            raise
        
    # 获取多平台店铺信息
    @staticmethod
    def extract_store_info_as_dict(json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract store information from JSON data
        
        Args:
            json_data: JSON data containing store information
            
        Returns:    
            List[Dict[str, Any]]: List of store information dictionaries
        """
        if isinstance(json_data, str):
            try:
                json_obj = json.loads(json_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"无效的JSON字符串: {str(e)}")
        elif isinstance(json_data, dict):
            json_obj = json_data
        else:
            # 抛出类型错误异常,提示输入格式要求
            logger.error("输入数据格式错误:必须是JSON字符串或字典对象")
            return None

        try:
            # 记录原始数据结构
            logger.debug("正在解析的数据结构:")
            logger.debug(json.dumps(json_obj, ensure_ascii=False, indent=2))
            
            # 首先验证data字段是否存在
            if 'data' not in json_obj:
                logger.error("数据结构错误：缺少 data 字段")
                logger.debug(f"实际数据结构：{json.dumps(json_obj, ensure_ascii=False, indent=2)}")
                return None
            
            # 检查data字段的内容结构
            data_content = json_obj['data']
            if not isinstance(data_content, dict):
                logger.error("data 字段不是字典类型")
                return None
                
            # 检查是否存在list字段
            if 'list' not in data_content:
                logger.error("数据结构错误：data 中缺少 list 字段")
                logger.debug(f"data 字段内容：{json.dumps(data_content, ensure_ascii=False, indent=2)}")
                return None

            # 获取店铺列表数据
            store_list = data_content['list']
            if not isinstance(store_list, list):
                logger.error("data.list 不是列表类型")
                return None
                
            if not store_list:
                logger.warning("data.list 为空列表")
                return []

            logger.info(f"找到 {len(store_list)} 个店铺记录")
            
            # 分析第一个店铺记录的字段结构
            if store_list:
                sample_store = store_list[0]
                logger.debug(f"店铺数据示例：{json.dumps(sample_store, ensure_ascii=False, indent=2)}")
                available_fields = list(sample_store.keys())
                logger.info(f"可用字段：{available_fields}")

            # 直接遍历店铺列表，逐个处理每个店铺
            stores_info = []
            
            for i, store_data in enumerate(store_list):
                try:
                    if not isinstance(store_data, dict):
                        logger.warning(f"跳过第 {i+1} 个店铺：数据不是字典格式")
                        continue
                    
                    # 提取店铺信息
                    store_info = {}
                    
                    # 获取店铺ID（优先使用sid，如果不存在则使用store_id）
                    shop_id = store_data.get('sid') or store_data.get('store_id')
                    if not shop_id:
                        logger.warning(f"跳过第 {i+1} 个店铺：缺少有效的店铺ID (sid 或 store_id)")
                        continue
                    
                    store_info['shop_id'] = shop_id
                    
                    # 提取其他必要字段
                    store_info['platform_id'] = store_data.get('platform_code')
                    store_info['shop_name'] = store_data.get('store_name')
                    store_info['platform'] = store_data.get('platform_name')
                    
                    # 验证必要字段是否存在
                    required_fields = ['shop_id', 'platform_id', 'shop_name', 'platform']
                    missing_fields = [field for field in required_fields if not store_info.get(field)]
                    
                    if missing_fields:
                        logger.warning(f"跳过第 {i+1} 个店铺：缺少必要字段 {missing_fields}")
                        logger.debug(f"店铺原始数据：{json.dumps(store_data, ensure_ascii=False, indent=2)}")
                        continue
                    
                    stores_info.append(store_info)
                    logger.debug(f"成功提取店铺 {i+1}: {store_info['shop_name']} (ID: {store_info['shop_id']})")
                    
                except Exception as e:
                    logger.error(f"处理第 {i+1} 个店铺时出错：{str(e)}")
                    continue
            
            logger.info(f"成功提取 {len(stores_info)} 条有效店铺信息")
            
            # 统计店铺ID类型
            sid_count = sum(1 for info in stores_info if 'sid' in store_list[stores_info.index(info)])
            store_id_count = len(stores_info) - sid_count
            logger.info(f"店铺ID统计：sid类型 {sid_count} 个，store_id类型 {store_id_count} 个")
            
            return stores_info
            
        except Exception as e:
            raise ValueError(f"数据结构解析错误: {str(e)}")
    
    @staticmethod
    def extract_amazon_store_as_dict(json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract Amazon store information from JSON data
        Args:
            json_data: JSON data containing Amazon store information
        Returns:
            List[Dict[str, Any]]: List of Amazon store information dictionaries
        """           

    
    @staticmethod
    def get_currency_rates(target_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get exchange rate data.

        Args:
            target_date: Target date in YYYY-MM format.

        Returns:
            List[Dict[str, Any]]: List of exchange rate data.
        """
        if target_date is None:
            # 获取昨天的日期并格式化为YYYY-MM格式
            yesterday = datetime.now() - timedelta(days=1)
            target_date = yesterday.strftime("%Y-%m")
        
        url = f"{GetData.BASE_URL}{GetData.CURRENCY_ENDPOINT}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "date": target_date
        }
        
        logger.info(f"正在请求汇率数据: {url}")
        logger.info(f"请求参数: {json.dumps(payload, ensure_ascii=False)}")
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            if not isinstance(response_data, dict):
                raise ValueError("API返回的数据格式不正确")
            
            if response_data.get("code") != 0:
                raise ValueError(f"API返回错误: {response_data.get('message', '未知错误')}")
            
            # 从响应中提取实际的汇率数据
            currency_data = []
            rate_data = response_data.get("data", [])
            
            logger.info(f"获取到的原始汇率数据: {json.dumps(rate_data, ensure_ascii=False)}")
            if not rate_data:
                logger.error("汇率数据为空")
                return []
                
            # 记录返回的原始数据结构
            logger.debug("汇率API返回数据结构:")
            logger.debug(json.dumps(rate_data, ensure_ascii=False, indent=2))
            
            # 处理列表格式的汇率数据
            for rate_info in rate_data:
                if not isinstance(rate_info, dict):
                    logger.warning(f"跳过无效的汇率数据格式: {rate_info}")
                    continue
                
                # 提取汇率数据
                code = rate_info.get("code")
                rate = rate_info.get("my_rate")
                
                # 基本验证
                try:
                    if rate:  # 如果汇率存在，验证是否为有效数字
                        rate_value = float(rate)
                        if rate_value <= 0:
                            logger.warning(f"跳过无效的汇率值 {code}: {rate}")
                            continue
                    else:
                        logger.warning(f"汇率值为空 {code}")
                        continue
                        
                    # 添加完整的汇率信息
                    currency_data.append({
                        'code': code,
                        'rate': str(rate),
                        'name': rate_info.get('name'),
                        'icon': rate_info.get('icon'),
                        'rate_org': rate_info.get('rate_org')
                    })
                    
                except (ValueError, TypeError) as e:
                    logger.warning(f"跳过无效的汇率数据 {code}: {str(e)}")
                    continue
            
            logger.info(f"成功获取汇率数据: {len(currency_data)} 个有效汇率")
            return currency_data
            
        except requests.RequestException as e:
            logger.error(f"获取汇率数据失败: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"解析汇率数据失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"获取汇率数据时发生未预期的错误: {str(e)}")
            raise
            
    @staticmethod
    def sync_currency_data(db_manager, currency_data: List[Dict[str, Any]], target_date: date) -> bool:
        """
        同步汇率数据到数据库
        
        Args:
            db_manager: DatabaseManager实例
            currency_data: 汇率信息列表
            target_date: 目标日期
            
        Returns:
            bool: 同步是否成功
        """
        session = db_manager.Session()
        try:
            current_time = datetime.now()
            logger.info(f"开始同步汇率数据，目标日期: {target_date}, 数据条数: {len(currency_data)}")
            
            for rate_info in currency_data:
                try:
                    currency_code = rate_info.get('code')
                    rate_str = rate_info.get('rate')
                    
                    if not currency_code or not rate_str:
                        continue
                        
                    logger.info(f"处理货币 {currency_code} 的汇率数据: {rate_str}")
                    # 检查是否已存在该货币的汇率记录
                    existing_rate = session.query(ExchangeRate).filter(
                        ExchangeRate.currency_code == currency_code,
                        ExchangeRate.date == target_date
                    ).first()
                    
                    try:
                        # 将字符串汇率转换为Decimal
                        rate_value = Decimal(rate_str)
                    except (ValueError, TypeError) as e:
                        logger.error(f"汇率值转换失败 {currency_code}: {rate_str}, 错误: {str(e)}")
                        continue
                    
                    if existing_rate:
                        # 如果记录存在且汇率不同，则更新
                        if existing_rate.user_rate != rate_value:
                            existing_rate.user_rate = rate_value
                            existing_rate.update_time = current_time
                            existing_rate.currency_name = rate_info.get('name')
                            existing_rate.currency_icon = rate_info.get('icon')
                            # 处理 org_rate
                            org_rate_str = rate_info.get('rate_org')
                            if org_rate_str:
                                try:
                                    existing_rate.org_rate = Decimal(str(org_rate_str))
                                except (ValueError, TypeError):
                                    pass
                            session.commit()
                            logger.info(f"更新汇率记录: {currency_code}-{target_date}, 新汇率: {rate_value}")
                    else:
                        # 创建新的汇率记录
                        new_rate_data = {
                            'date': target_date,
                            'currency_code': currency_code,
                            'currency_name': rate_info.get('name'),
                            'currency_icon': rate_info.get('icon'),
                            'user_rate': rate_value,
                            'update_time': current_time
                        }
                        
                        # 处理 org_rate
                        org_rate_str = rate_info.get('rate_org')
                        if org_rate_str:
                            try:
                                new_rate_data['org_rate'] = Decimal(str(org_rate_str))
                            except (ValueError, TypeError):
                                pass
                                
                        new_rate = ExchangeRate(**new_rate_data)
                        session.add(new_rate)
                        session.commit()
                        logger.info(f"添加新汇率记录: {currency_code}-{target_date}, 汇率: {rate_value}")
                        
                except Exception as e:
                    logger.error(f"处理货币 {currency_code} 的汇率数据时出错: {str(e)}")
                    session.rollback()
                    continue
                    
            return True
        except Exception as e:
            logger.error(f"同步汇率数据失败: {str(e)}")
            return False
        finally:
            session.close()
            
    @staticmethod
    def get_sales_stats(db_manager: DatabaseManager, start_date: Optional[str] = None, 
                       end_date: Optional[str] = None, 
                       shop_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get sales statistics data

        Args:
            db_manager (DatabaseManager): Database manager instance
            start_date (str, optional): Start date in YYYY-MM-DD format. Defaults to yesterday
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to yesterday
            shop_ids (List[str], optional): List of shop IDs. If None, get data for all shops

        Returns:
            Dict[str, Any]: Sales statistics data from API

        Raises:
            requests.RequestException: When API request fails
            ValueError: When API returns invalid data format
            SQLAlchemyError: When database operation fails
        """
        # 如果没有指定日期，使用昨天的日期
        if start_date is None or end_date is None:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            start_date = start_date or yesterday
            end_date = end_date or yesterday

        # 如果没有指定shop_ids，从数据库获取所有店铺ID
        session = db_manager.Session()
        try:
            if shop_ids is None:
                shop_query = session.query(Shop.shop_id).all()
                shop_ids = [shop[0] for shop in shop_query]
                logger.info(f"从数据库获取到 {len(shop_ids)} 个店铺ID")
        finally:
            session.close()

        if not shop_ids:
            logger.warning("没有找到有效的店铺ID")
            return {"code": -1, "message": "没有有效的店铺ID", "data": []}

        # 准备API请求
        url = f"{GetData.BASE_URL}{GetData.SALES_STATS_ENDPOINT}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "start_date": start_date,
            "end_date": end_date,
            "result_type": "3",
            "date_unit": "4",
            "data_type": "6",
            "page": 1,
            "length": 200,
            "shop_ids": shop_ids
        }

        logger.info(f"正在请求销售统计数据: {url}")
        logger.info(f"请求参数: {json.dumps(payload, ensure_ascii=False)}")

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("API返回的数据格式不正确")

            # 打印返回的数据结构
            logger.info("销售统计API返回数据结构:")
            logger.info(json.dumps(data, ensure_ascii=False, indent=2))
            
            # 检查返回的数据结构
            if 'data' not in data:
                logger.error("API返回数据中没有 'data' 字段")
                return {"code": -1, "message": "数据格式错误", "data": []}
            
            # 检查 data 字段的格式，可能是直接的列表或包含 list 字段的字典
            data_content = data['data']
            if not isinstance(data_content, (list, dict)):
                logger.error("API返回的 data 字段格式不正确")
                return {"code": -1, "message": "数据格式错误", "data": []}
            
            # 如果 data 是字典且包含 list 字段，检查 list 字段
            if isinstance(data_content, dict) and 'list' not in data_content:
                logger.error("API返回数据中没有 'data.list' 字段")
                return {"code": -1, "message": "数据格式错误", "data": []}

            return data

        except requests.RequestException as e:
            logger.error(f"获取销售统计数据失败: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"解析销售统计API响应失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"获取销售统计数据时发生未预期的错误: {str(e)}")
            raise

    @staticmethod
    def extract_storedata_mapping(json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract store data from JSON.

        Args:
            json_data: JSON data containing store information.

        Returns:
            List[Dict[str, Any]]: List of store data records.
        """
        try:
            data = json_data            
            # 提取所有数据项
            data_items = []
            if 'data' in data:
                data_items = data['data'].get('list', [])  # 适应API返回的数据结构
            else:
                # 从data中提取店铺数据
                if "data" in api_data and "list" in api_data["data"]:
                    data_items = api_data["data"]["list"]
            
            # 返回店铺信息列表
            return data_items
        except Exception as e:
            logger.error(f"提取JSON数据映射时出错: {str(e)}")
            raise Exception(f"提取JSON数据映射时出错: {str(e)}")

    @staticmethod
    def sync_sales_data(db_manager: DatabaseManager, sales_data: Dict[str, Any], target_date: date) -> bool:
        """
        同步销售数据到数据库
        
        Args:
            db_manager: DatabaseManager实例
            sales_data: API返回的销售统计数据
            target_date: 目标日期
            
        Returns:
            bool: 同步是否成功
        """
        session = db_manager.Session()
        try:
            # 提取销售数据
            logger.info("开始提取销售数据...")
            store_data_list = GetData.extract_storedata_mapping(sales_data)
            logger.info(f"提取的销售数据: {json.dumps(store_data_list, ensure_ascii=False, indent=2)}")
            if not store_data_list:
                logger.warning("没有找到有效的销售数据")
                return False
                
            current_time = datetime.now()
            success_count = 0
            error_count = 0
            
            for store_data in store_data_list:
                try:
                    # 获取店铺ID（优先使用sid，如果不存在则使用store_id）
                    shop_id = store_data.get('sid') or store_data.get('store_id')
                    if not shop_id:
                        logger.warning("店铺数据缺少有效的店铺ID")
                        logger.debug(f"店铺数据内容：{json.dumps(store_data, ensure_ascii=False, indent=2)}")
                        continue
                    
                    logger.info(f"正在处理店铺销售数据，shop_id: {shop_id}")
                    # 使用shop_id查找对应的shop记录，同时检查sid和store_id
                    shop = session.query(Shop).filter(
                        or_(
                            Shop.shop_id == shop_id,
                            Shop.shop_id == store_data.get('store_id')
                        )
                    ).first()
                    
                    if not shop:
                        logger.warning(f"找不到对应的店铺记录: shop_id={shop_id}, store_id={store_data.get('store_id')}")
                        continue
                        
                    volume_total = store_data.get('volumeTotal', '0')
                    currency_code = store_data.get('currency', '')
                    
                    # 使用shop_id查找对应的shop记录
                    shop = session.query(Shop).filter(Shop.shop_id == shop_id).first()
                    if not shop:
                        logger.warning(f"找不到对应的店铺记录: shop_id={shop_id}")
                        continue
                        
                    # 获取当前货币的汇率
                    exchange_rate = db_manager.get_exchange_rate(currency_code, target_date)
                    if not exchange_rate:
                        logger.warning(f"找不到对应的汇率记录: currency={currency_code}, date={target_date}")
                        continue
                        
                    # 计算不同币种的金额
                    try:
                        volume_decimal = Decimal(volume_total)
                        if currency_code == 'CNY':
                            cny_amount = volume_decimal
                            usd_amount = volume_decimal / exchange_rate.user_rate
                        else:
                            cny_amount = volume_decimal * exchange_rate.user_rate
                            if currency_code == 'USD':
                                usd_amount = volume_decimal
                            else:
                                # 获取USD汇率
                                usd_rate = db_manager.get_exchange_rate('USD', target_date)
                                if not usd_rate:
                                    logger.warning(f"找不到USD汇率记录: date={target_date}")
                                    continue
                                usd_amount = cny_amount / usd_rate.user_rate
                    except (ValueError, TypeError, InvalidOperation) as e:
                        logger.error(f"金额转换失败: {str(e)}, sid={sid}, volume={volume_total}")
                        continue
                    
                    # 检查是否已存在该销售记录
                    existing_sale = session.query(Sale).filter(
                        Sale.shop_id == shop.shop_id,
                        Sale.sale_date == target_date
                    ).first()
                    
                    if existing_sale:
                        # 更新现有记录
                        setattr(existing_sale, 'cny_amount', cny_amount)
                        setattr(existing_sale, 'usd_amount', usd_amount)
                        setattr(existing_sale, 'entry_time', current_time)
                    else:
                        # 创建新记录
                        new_sale = Sale(
                            shop_id=shop.shop_id,
                            sale_date=target_date,
                            cny_amount=cny_amount,
                            usd_amount=usd_amount,
                            entry_time=current_time
                        )
                        session.add(new_sale)
                    
                    session.commit()
                    success_count += 1
                    logger.info(f"成功同步销售数据: shop_id={shop_id}, date={target_date}")
                    
                except Exception as e:
                    error_count += 1
                    session.rollback()
                    logger.error(f"处理销售数据时出错: sid={sid}, error={str(e)}")
                    continue
            
            logger.info(f"销售数据同步完成: 成功={success_count}, 失败={error_count}")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"同步销售数据失败: {str(e)}")
            return False
        finally:
            session.close()

    @staticmethod
    def convert_currency(amount: str, from_currency: str, to_currency: str, 
                        exchange_rate: 'ExchangeRate', usd_rate: Optional['ExchangeRate'] = None) -> Decimal:
        """
        货币转换静态方法
        
        Args:
            amount: 金额字符串
            from_currency: 源货币代码
            to_currency: 目标货币代码 (CNY/USD)
            exchange_rate: 源货币汇率记录
            usd_rate: USD汇率记录（当需要转换为USD且源货币不是USD时需要）
            
        Returns:
            Decimal: 转换后的金额
        """
        try:
            amount_decimal = Decimal(str(amount))
            
            if from_currency == to_currency:
                return amount_decimal
                
            if to_currency == 'CNY':
                # 转换为人民币
                if from_currency == 'CNY':
                    return amount_decimal
                else:
                    return amount_decimal * exchange_rate.user_rate
                    
            elif to_currency == 'USD':
                # 转换为美元
                if from_currency == 'USD':
                    return amount_decimal
                elif from_currency == 'CNY':
                    if not usd_rate:
                        raise ValueError("缺少USD汇率数据")
                    return amount_decimal / usd_rate.user_rate
                else:
                    # 其他货币 -> CNY -> USD
                    cny_amount = amount_decimal * exchange_rate.user_rate
                    if not usd_rate:
                        raise ValueError("缺少USD汇率数据")
                    return cny_amount / usd_rate.user_rate
                    
        except (ValueError, TypeError, InvalidOperation) as e:
            logger.error(f"货币转换失败: amount={amount}, from={from_currency}, to={to_currency}, error={str(e)}")
            raise

    @staticmethod
    def ensure_exchange_rates_for_period(db_manager: DatabaseManager, start_date: date, end_date: date) -> bool:
        """
        确保指定时间区间内的汇率数据完整
        
        Args:
            db_manager: 数据库管理器
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            bool: 汇率数据是否完整
        """
        logger.info(f"检查时间区间 {start_date} 到 {end_date} 的汇率数据")
        
        # 获取时间区间内的所有月份
        current_date = start_date.replace(day=1)  # 月初
        end_month = end_date.replace(day=1)
        months_needed = []
        
        while current_date <= end_month:
            months_needed.append(current_date)
            # 移动到下个月
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        logger.info(f"需要检查的月份: {[month.strftime('%Y-%m') for month in months_needed]}")
        
        # 检查每个月份的汇率数据
        missing_months = []
        session = db_manager.Session()
        try:
            for month_date in months_needed:
                # 检查该月份是否有汇率数据
                existing_rate = session.query(ExchangeRate).filter(
                    ExchangeRate.date >= month_date,
                    ExchangeRate.date < (month_date.replace(day=28) + timedelta(days=4)).replace(day=1)
                ).first()
                
                if not existing_rate:
                    missing_months.append(month_date)
                    
        finally:
            session.close()
        
        # 获取缺失月份的汇率数据
        if missing_months:
            logger.info(f"缺少汇率数据的月份: {[month.strftime('%Y-%m') for month in missing_months]}")
            for month_date in missing_months:
                try:
                    # 获取该月份的汇率数据
                    target_date_str = month_date.strftime('%Y-%m-%d')
                    currency_data = GetData.get_currency_rates(target_date_str)
                    if currency_data:
                        success = GetData.sync_currency_data(db_manager, currency_data, month_date)
                        if not success:
                            logger.error(f"同步 {month_date.strftime('%Y-%m')} 汇率数据失败")
                            return False
                    else:
                        logger.error(f"无法获取 {month_date.strftime('%Y-%m')} 的汇率数据")
                        return False
                except Exception as e:
                    logger.error(f"处理 {month_date.strftime('%Y-%m')} 汇率数据时出错: {str(e)}")
                    return False
        
        logger.info("汇率数据检查完成")
        return True

    @staticmethod
    def get_required_months(start_date: date, end_date: date) -> List[str]:
        """获取指定日期范围内需要的月份列表
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            List[str]: 月份列表，格式为 YYYY-MM
        """
        from dateutil.relativedelta import relativedelta
        
        months = []
        current_date = start_date.replace(day=1)  # 从月初开始
        end_month = end_date.replace(day=1)
        
        while current_date <= end_month:
            months.append(current_date.strftime('%Y-%m'))
            current_date += relativedelta(months=1)
        
        logger.info(f"📅 需要的月份范围: {months}")
        return months
    
    @staticmethod
    def check_missing_exchange_rates(db_manager: DatabaseManager, required_months: List[str]) -> List[str]:
        """检查缺失的汇率数据月份
        
        Args:
            db_manager: 数据库管理器实例
            required_months: 需要的月份列表
            
        Returns:
            List[str]: 缺失汇率数据的月份列表
        """
        session = db_manager.Session()
        missing_months = []
        
        try:
            for month_str in required_months:
                year, month = map(int, month_str.split('-'))
                # 检查该月份是否有汇率数据
                month_start = date(year, month, 1)
                if month == 12:
                    month_end = date(year + 1, 1, 1) - timedelta(days=1)
                else:
                    month_end = date(year, month + 1, 1) - timedelta(days=1)
                
                # 查询该月份是否有汇率记录
                existing_rate = session.query(ExchangeRate).filter(
                    ExchangeRate.date >= month_start,
                    ExchangeRate.date <= month_end
                ).first()
                
                if not existing_rate:
                    missing_months.append(month_str)
                    logger.warning(f"❌ 缺少 {month_str} 月份的汇率数据")
                else:
                    logger.info(f"✅ {month_str} 月份汇率数据存在")
        
        except Exception as e:
            logger.error(f"检查汇率数据时出错: {str(e)}")
        finally:
            session.close()
        
        return missing_months
    
    @staticmethod
    def update_missing_exchange_rates(db_manager: DatabaseManager, missing_months: List[str]) -> bool:
        """更新缺失的汇率数据
        
        Args:
            db_manager: 数据库管理器实例
            missing_months: 缺失汇率数据的月份列表
            
        Returns:
            bool: 更新是否成功
        """
        if not missing_months:
            logger.info("✅ 所有月份的汇率数据都已存在，无需更新")
            return True
        
        logger.info(f"🔄 开始更新缺失的汇率数据: {missing_months}")
        
        success_count = 0
        for month_str in missing_months:
            try:
                # 获取该月份的汇率数据
                logger.info(f"📡 正在获取 {month_str} 月份的汇率数据...")
                currency_data = GetData.get_currency_rates(month_str)
                
                if not currency_data:
                    logger.error(f"❌ 无法获取 {month_str} 月份的汇率数据")
                    continue
                
                # 使用该月份第一天作为汇率日期
                year, month = map(int, month_str.split('-'))
                target_date = date(year, month, 1)
                
                # 同步汇率数据到数据库
                if GetData.sync_currency_data(db_manager, currency_data, target_date):
                    logger.info(f"✅ {month_str} 月份汇率数据更新成功")
                    success_count += 1
                else:
                    logger.error(f"❌ {month_str} 月份汇率数据更新失败")
                    
            except Exception as e:
                logger.error(f"更新 {month_str} 月份汇率数据时出错: {str(e)}")
        
        if success_count == len(missing_months):
            logger.info(f"🎉 所有缺失的汇率数据更新完成 ({success_count}/{len(missing_months)})")
            return True
        else:
            logger.warning(f"⚠️ 部分汇率数据更新失败 ({success_count}/{len(missing_months)})")
            return False
    
    @staticmethod
    def sync_sales_data_by_month(db_manager: DatabaseManager, start_date: date, end_date: date) -> bool:
        """按月份同步销售数据
        
        Args:
            db_manager: 数据库管理器实例
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            bool: 同步是否成功
        """
        logger.info(f"🔄 开始按月份同步销售数据: {start_date} 到 {end_date}")
        
        # 获取需要的月份
        required_months = GetData.get_required_months(start_date, end_date)
        
        success_count = 0
        total_records = 0
        
        for month_str in required_months:
            try:
                year, month = map(int, month_str.split('-'))
                
                # 计算该月份的开始和结束日期
                month_start = date(year, month, 1)
                if month == 12:
                    month_end = date(year + 1, 1, 1) - timedelta(days=1)
                else:
                    month_end = date(year, month + 1, 1) - timedelta(days=1)
                
                # 确保不超出用户指定的范围
                actual_start = max(month_start, start_date)
                actual_end = min(month_end, end_date)
                
                logger.info(f"📊 正在处理 {month_str} 月份数据: {actual_start} 到 {actual_end}")
                
                # 获取该月份的销售数据
                sales_data = GetData.get_sales_stats(
                    db_manager,
                    start_date=actual_start.strftime('%Y-%m-%d'),
                    end_date=actual_end.strftime('%Y-%m-%d')
                )
                
                if sales_data:
                    # 处理销售数据
                    processed_success = GetData.process_sales_data(db_manager, sales_data, actual_start, actual_end)
                    
                    if processed_success:
                        logger.info(f"✅ {month_str} 月份销售数据处理成功")
                        success_count += 1
                        total_records += 1  # 简化计数，表示该月份处理成功
                    else:
                        logger.warning(f"⚠️ {month_str} 月份销售数据处理失败")
                else:
                    logger.warning(f"⚠️ 无法获取 {month_str} 月份的销售数据")
                    
            except Exception as e:
                logger.error(f"处理 {month_str} 月份销售数据时出错: {str(e)}")
        
        logger.info(f"🎯 按月份销售数据同步完成: 成功处理 {success_count}/{len(required_months)} 个月份，共 {total_records} 条记录")
        return success_count == len(required_months)
    
    @staticmethod
    def sync_sales_data_with_improved_logic(db_manager: DatabaseManager, start_date: Optional[date] = None, end_date: Optional[date] = None) -> bool:
        """使用改进逻辑同步销售数据（支持跨月份）
        
        Args:
            db_manager: 数据库管理器实例
            start_date: 开始日期，如果为None则默认为昨天
            end_date: 结束日期，如果为None则默认为昨天
            
        Returns:
            bool: 同步是否成功
        """
        try:
            # 处理默认日期参数
            if start_date is None and end_date is None:
                # 默认处理昨天的数据
                yesterday = date.today() - timedelta(days=1)
                start_date = end_date = yesterday
                logger.info(f"📅 使用默认日期范围（昨天）: {yesterday}")
            elif start_date is None:
                start_date = end_date
            elif end_date is None:
                end_date = start_date
            
            # 验证日期范围
            if start_date > end_date:
                logger.error("❌ 开始日期不能大于结束日期")
                return False
            
            logger.info(f"🚀 开始改进的数据同步流程: {start_date} 到 {end_date}")
            
            # 步骤1: 获取需要的月份
            required_months = GetData.get_required_months(start_date, end_date)
            
            # 步骤2: 检查缺失的汇率数据
            missing_months = GetData.check_missing_exchange_rates(db_manager, required_months)
            
            # 步骤3: 更新缺失的汇率数据
            if missing_months:
                if not GetData.update_missing_exchange_rates(db_manager, missing_months):
                    logger.error("❌ 汇率数据更新失败，无法继续同步销售数据")
                    return False
            
            # 步骤4: 按月份同步销售数据
            if GetData.sync_sales_data_by_month(db_manager, start_date, end_date):
                logger.info("🎉 改进的数据同步流程完成成功")
                return True
            else:
                logger.error("❌ 销售数据同步失败")
                return False
                
        except Exception as e:
            logger.error(f"改进的数据同步流程出错: {str(e)}")
            return False

    @staticmethod
    def sync_sales_data_with_period(db_manager: DatabaseManager, start_date: Optional[date] = None, end_date: Optional[date] = None) -> bool:
        """
        同步指定时间区间的销售数据到数据库
        
        Args:
            db_manager: DatabaseManager实例
            start_date: 开始日期（可选，默认为昨天）
            end_date: 结束日期（可选，默认为昨天）
            
        Returns:
            bool: 同步是否成功
        """
        # 处理默认时间参数
        if start_date is None and end_date is None:
            # 默认获取昨天的数据
            yesterday = datetime.now().date() - timedelta(days=1)
            start_date = end_date = yesterday
            logger.info(f"未指定时间区间，默认获取昨天数据: {yesterday}")
        elif start_date is None:
            start_date = end_date
        elif end_date is None:
            end_date = start_date
            
        logger.info(f"开始同步销售数据，时间区间: {start_date} 到 {end_date}")
        
        # 验证时间区间
        if start_date > end_date:
            logger.error("开始时间不能大于结束时间")
            return False
            
        # 确保汇率数据完整
        if not GetData.ensure_exchange_rates_for_period(db_manager, start_date, end_date):
            logger.error("汇率数据不完整，无法进行销售数据同步")
            return False
        
        # 获取销售统计数据
        try:
            # 构建时间区间参数
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            logger.info(f"获取销售统计数据: {start_date_str} 到 {end_date_str}")
            sales_stats = GetData.get_sales_stats(db_manager, start_date_str, end_date_str)
            
            if sales_stats.get('code') != 0:
                logger.error(f"获取销售统计数据失败: {sales_stats.get('message', '未知错误')}")
                return False
                
            # 处理销售数据
            return GetData.process_sales_data(db_manager, sales_stats, start_date, end_date)
            
        except Exception as e:
            logger.error(f"同步销售数据失败: {str(e)}")
            return False

    @staticmethod
    def process_sales_data(db_manager: DatabaseManager, sales_data: Dict[str, Any], 
                          start_date: date, end_date: date) -> bool:
        """
        处理销售数据并写入数据库
        
        Args:
            db_manager: DatabaseManager实例
            sales_data: API返回的销售统计数据
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            bool: 处理是否成功
        """
        logger.info("开始处理销售数据")
        session = db_manager.Session()
        success_count = 0
        error_count = 0
        
        try:
            # 检查数据结构
            if 'data' not in sales_data:
                logger.error("销售数据格式错误：缺少 data 字段")
                logger.debug(f"实际数据结构：{json.dumps(sales_data, ensure_ascii=False, indent=2)}")
                return False
                
            data_content = sales_data['data']
            
            # 检查 data 是否直接是列表，或者包含 list 字段
            if isinstance(data_content, list):
                store_list = data_content
                logger.info("数据格式：data 字段直接是列表")
            elif isinstance(data_content, dict) and 'list' in data_content:
                store_list = data_content['list']
                logger.info("数据格式：data.list 字段包含列表")
            else:
                logger.error("销售数据格式错误：data 既不是列表也不包含 list 字段")
                logger.debug(f"data 字段内容：{json.dumps(data_content, ensure_ascii=False, indent=2)}")
                return False
            if not isinstance(store_list, list):
                logger.error("data.list 不是列表类型")
                return False
                
            if not store_list:
                logger.warning("data.list 为空列表")
                return True
                
            logger.info(f"找到 {len(store_list)} 个店铺的销售数据")
            current_time = datetime.now()
            
            for i, store_data in enumerate(store_list):
                try:
                    if not isinstance(store_data, dict):
                        logger.warning(f"跳过第 {i+1} 个店铺：数据不是字典格式")
                        continue
                    
                    # 提取店铺ID (使用 sid)
                    sid_data = store_data.get('sid')
                    if not sid_data:
                        logger.warning(f"跳过第 {i+1} 个店铺：缺少 sid 字段")
                        logger.debug(f"店铺数据：{json.dumps(store_data, ensure_ascii=False, indent=2)}")
                        continue
                    
                    # sid 可能是列表，需要提取第一个元素
                    if isinstance(sid_data, list):
                        if len(sid_data) > 0:
                            shop_id = sid_data[0]
                        else:
                            logger.warning(f"跳过第 {i+1} 个店铺：sid 列表为空")
                            continue
                    else:
                        shop_id = sid_data
                    
                    if not shop_id:
                        logger.warning(f"跳过第 {i+1} 个店铺：sid 值为空")
                        continue
                    
                    # 查找对应的店铺记录
                    shop = session.query(Shop).filter(Shop.shop_id == shop_id).first()
                    if not shop:
                        logger.warning(f"跳过第 {i+1} 个店铺：找不到对应的店铺记录 shop_id={shop_id}")
                        continue
                    
                    # 提取货币代码
                    currency_code = store_data.get('currency_code', '')
                    if not currency_code:
                        logger.warning(f"跳过第 {i+1} 个店铺：缺少 currency_code 字段")
                        continue
                    
                    # 提取 date_collect 数据
                    date_collect = store_data.get('date_collect', {})
                    if not isinstance(date_collect, dict):
                        logger.warning(f"跳过第 {i+1} 个店铺：date_collect 不是字典格式")
                        continue
                    
                    if not date_collect:
                        logger.warning(f"跳过第 {i+1} 个店铺：date_collect 为空")
                        continue
                    
                    logger.info(f"处理店铺 {shop_id} 的销售数据，包含 {len(date_collect)} 天的数据")
                    
                    # 处理每一天的销售数据
                    for date_str, amount_str in date_collect.items():
                        try:
                            # 解析日期
                            sale_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                            
                            # 检查日期是否在指定区间内
                            if not (start_date <= sale_date <= end_date):
                                continue
                            
                            # 获取汇率数据
                            exchange_rate = db_manager.get_exchange_rate(currency_code, sale_date)
                            if not exchange_rate:
                                logger.warning(f"找不到汇率记录: currency={currency_code}, date={sale_date}")
                                continue
                            
                            usd_rate = None
                            if currency_code != 'USD':
                                usd_rate = db_manager.get_exchange_rate('USD', sale_date)
                                if not usd_rate:
                                    logger.warning(f"找不到USD汇率记录: date={sale_date}")
                                    continue
                            
                            # 货币转换
                            cny_amount = GetData.convert_currency(amount_str, currency_code, 'CNY', exchange_rate, usd_rate)
                            usd_amount = GetData.convert_currency(amount_str, currency_code, 'USD', exchange_rate, usd_rate)
                            
                            # 检查是否已存在该销售记录
                            existing_sale = session.query(Sale).filter(
                                Sale.shop_id == shop.shop_id,
                                Sale.sale_date == sale_date
                            ).first()
                            
                            if existing_sale:
                                # 更新现有记录
                                old_cny = existing_sale.cny_amount
                                old_usd = existing_sale.usd_amount
                                existing_sale.cny_amount = cny_amount
                                existing_sale.usd_amount = usd_amount
                                existing_sale.entry_time = current_time
                                logger.info(f"🔄 更新销售记录: shop_id={shop_id}, date={sale_date}")
                                logger.info(f"   CNY: {old_cny} → {cny_amount}, USD: {old_usd} → {usd_amount}")
                            else:
                                # 创建新记录
                                new_sale = Sale(
                                    shop_id=shop.shop_id,
                                    sale_date=sale_date,
                                    cny_amount=cny_amount,
                                    usd_amount=usd_amount,
                                    entry_time=current_time
                                )
                                session.add(new_sale)
                                logger.info(f"➕ 新增销售记录: shop_id={shop_id}, date={sale_date}")
                                logger.info(f"   CNY: {cny_amount}, USD: {usd_amount}")
                            
                            success_count += 1
                            
                        except ValueError as e:
                            logger.error(f"日期解析失败: date_str={date_str}, error={str(e)}")
                            error_count += 1
                            continue
                        except Exception as e:
                            logger.error(f"处理销售记录失败: shop_id={shop_id}, date={date_str}, error={str(e)}")
                            error_count += 1
                            continue
                    
                    # 提交该店铺的所有销售记录
                    session.commit()
                    logger.info(f"店铺 {shop_id} 销售数据处理完成")
                    
                except Exception as e:
                    error_count += 1
                    session.rollback()
                    logger.error(f"处理第 {i+1} 个店铺时出错: {str(e)}")
                    continue
            
            logger.info(f"销售数据处理完成: 成功={success_count}, 失败={error_count}")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"处理销售数据失败: {str(e)}")
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def sync_store_data(db_manager: DatabaseManager, api_data: Dict[str, Any]) -> bool:
        """
        同步店铺数据到数据库
        
        Args:
            db_manager: DatabaseManager实例
            api_data: API返回的JSON数据，包含店铺信息
            
        Returns:
            bool: 同步是否成功
        """
        logger.info("开始同步店铺数据...")
        session = db_manager.Session()
        try:
            stores_info = GetData.extract_store_info_as_dict(api_data)
            logger.info(f"提取到 {len(stores_info)} 条店铺信息")
            
            for store_info in stores_info:
                try:
                    current_time = datetime.now()
                    shop_id = store_info.get('shop_id')  # 使用从 extract_store_info_as_dict 提取的 shop_id
                    if not shop_id:
                        logger.error(f"店铺数据缺少shop_id字段: {store_info}")
                        continue
                    
                    logger.info(f"处理店铺: {store_info['shop_name']} (ID: {shop_id})")
                    
                    # 先查询现有店铺
                    existing_shop = session.query(Shop).filter(Shop.shop_id == shop_id).first()
                    
                    # 准备店铺数据
                    shop_data = {
                        'shop_id': shop_id,
                        'platform_id': store_info.get('platform_id'),  # 使用get方法安全获取数据
                        'shop_name': store_info.get('shop_name'),
                        'platform': store_info.get('platform')
                    }
                    
                    # 验证必要字段
                    if not all(shop_data.values()):
                        logger.error(f"店铺数据缺少必要字段: {shop_data}")
                        continue
                    
                    if existing_shop:
                        # 如果店铺存在，检查是否需要更新
                        need_update = (
                            existing_shop.platform_id != shop_data['platform_id'] or
                            existing_shop.shop_name != shop_data['shop_name'] or
                            existing_shop.platform != shop_data['platform']
                        )
                        
                        if need_update:
                            # 只在数据真正改变时更新时间戳
                            shop_data['updated_at'] = current_time
                            
                            try:
                                for key, value in shop_data.items():
                                    setattr(existing_shop, key, value)
                                session.commit()
                                logger.info(f"店铺信息已更新: {shop_id}")
                            except Exception as e:
                                session.rollback()
                                logger.error(f"更新店铺信息失败: {str(e)}")
                                raise
                    else:
                        # 如果店铺不存在，创建新店铺
                        shop_data.update({
                            'created_at': current_time,
                            'updated_at': current_time
                        })
                        
                        try:
                            new_shop = Shop(**shop_data)
                            session.add(new_shop)
                            session.commit()
                            logger.info(f"新店铺已添加: {shop_id}")
                        except Exception as e:
                            session.rollback()
                            logger.error(f"添加新店铺失败: {str(e)}")
                            continue
                            
                except Exception as e:
                    logger.error(f"处理店铺时出错: {str(e)}")
                    session.rollback()
                    continue
            
            # 再次查询确认同步结果
            total_shops = session.query(Shop).count()
            logger.info(f"同步完成，数据库中共有 {total_shops} 个店铺")
            session.commit()
            return True
        except Exception as e:
            logger.error(f"同步店铺数据失败: {str(e)}")
            return False
        finally:
            session.close()

def test_db_connection():
    """测试数据库连接"""
    try:
        engine = get_db_engine()
        print("尝试建立连接...")
        with engine.connect() as conn:
            print("连接成功建立，执行版本查询...")
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"成功连接到 PostgreSQL！\n数据库版本: {version}")
            return True
    except SQLAlchemyError as e:
        print(f"SQLAlchemy错误: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        return False
    except Exception as e:
        print(f"未预期的错误: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        return False

if __name__ == "__main__":
    # 测试数据库连接
    if not test_db_connection():
        print("数据库连接失败，请检查配置")
        exit(1)
    
    # 初始化数据库管理器
    db_manager = DatabaseManager()
    
    # 删除并重新创建数据库表
    # db_manager.drop_tables()
    db_manager.init_db()
    
    try:
        # 从API获取店铺列表数据
        print("正在从API获取店铺列表...")
        api_data = GetData.get_seller_list()
        print(f"成功获取店铺数据，开始同步...")
        
        # 解析并打印店铺数据
        stores_info = GetData.extract_store_info_as_dict(api_data)
        print(f"提取到 {len(stores_info)} 条店铺信息")
        
        # 提取并打印店铺数据
        stores_info = GetData.extract_store_info_as_dict(api_data)
        print(f"提取到 {len(stores_info)} 条店铺信息")
        
        # 提取并打印店铺数据
        stores_info = GetData.extract_store_info_as_dict(api_data)
        print(f"提取到 {len(stores_info)} 条店铺信息")
        
        # 提取并打印店铺数据
        stores_info = GetData.extract_store_info_as_dict(api_data)
        print(f"提取到 {len(stores_info)} 条店铺信息")
        
        # 同步店铺数据到数据库
        success = GetData.sync_store_data(db_manager, api_data)
        if success:
            print("店铺数据同步成功！")
        else:
            print("店铺数据同步失败！程序终止")
            raise SystemExit(1)  # 如果店铺数据同步失败，终止程序
            exit(1)  # 如果店铺数据同步失败，终止程序
            # return  # 如果店铺数据同步失败，终止后续操作
            
        # 获取并同步汇率数据
        print("\n开始同步汇率数据...")
        # 获取昨天的日期
        yesterday = datetime.now().date() - timedelta(days=1)
        
        # 检查是否已存在昨天的汇率数据
        existing_rates = db_manager.get_exchange_rate("USD", yesterday)
        
        if not existing_rates:
            # 如果没有昨天的数据，则获取新数据
            print("正在获取汇率数据...")
            try:
                # 获取汇率数据
                currency_data = GetData.get_currency_rates()  # 使用默认值，会自动获取昨天月份的数据
                print(f"成功获取 {len(currency_data)} 个币种的汇率数据")
                
                # 同步汇率数据到数据库
                print("开始同步到数据库...")
                currency_success = GetData.sync_currency_data(db_manager, currency_data, yesterday)
                
                if currency_success:
                    print("汇率数据同步成功！")
                    # 打印部分汇率数据作为示例
                    for rate_data in currency_data[:3]:  # 只显示前3个作为示例
                        print(f"{rate_data.get('code', 'N/A')}: {rate_data.get('rate', 'N/A')}")
                else:
                    print("汇率数据同步失败！")
            except Exception as e:
                print(f"获取或同步汇率数据时出错: {str(e)}")
        else:
            print(f"已存在 {yesterday} 的汇率数据，无需更新")
            
        # 测试销售数据同步（使用新的方法）
        print("\n开始测试销售数据同步...")
        try:
            # 使用新的销售数据同步方法，默认获取昨天的数据
            sales_success = GetData.sync_sales_data_with_period(db_manager)
            if sales_success:
                print("销售数据同步成功！")
            else:
                print("销售数据同步失败！")
                
            # 测试指定时间区间的同步（可选）
            print("\n测试指定时间区间的销售数据同步...")
            from datetime import date
            
            # 测试同步最近3天的数据
            end_date = datetime.now().date() - timedelta(days=1)  # 昨天
            start_date = end_date - timedelta(days=2)  # 前天
            
            print(f"同步时间区间: {start_date} 到 {end_date}")
            period_success = GetData.sync_sales_data_with_period(db_manager, start_date, end_date)
            if period_success:
                print("指定时间区间销售数据同步成功！")
            else:
                print("指定时间区间销售数据同步失败！")
                
        except Exception as e:
            print(f"测试销售数据同步时出错: {str(e)}")
            
    except requests.RequestException as e:
        print(f"API请求失败: {str(e)}")
    except Exception as e:
        print(f"同步过程中出现错误: {str(e)}")