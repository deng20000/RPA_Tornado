# -*- coding: utf-8 -*-
"""
电商数据看板数据模型
定义电商数据看板相关的数据库模型
"""

from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text, Index, UniqueConstraint, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import logging

# 配置日志记录器
logger = logging.getLogger(__name__)

# 创建基础模型类
Base = declarative_base()


class Shop(Base):
    """店铺模型
    
    存储电商平台店铺的基本信息
    """
    __tablename__ = 'shops'
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    
    # 店铺基本信息
    shop_id = Column(String(50), nullable=False, comment='店铺ID')
    shop_name = Column(String(200), nullable=False, comment='店铺名称')
    platform_id = Column(String(20), nullable=False, comment='平台ID')
    platform = Column(String(50), nullable=False, comment='平台名称')
    
    # 店铺状态和配置
    status = Column(String(20), default='active', comment='店铺状态：active-活跃，inactive-非活跃')
    currency = Column(String(10), default='CNY', comment='店铺主要货币')
    timezone = Column(String(50), default='Asia/Shanghai', comment='店铺时区')
    
    # 扩展信息
    description = Column(Text, comment='店铺描述')
    settings = Column(Text, comment='店铺配置信息（JSON格式）')
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关系定义
    sales = relationship('Sale', back_populates='shop', cascade='all, delete-orphan')
    
    # 索引定义
    __table_args__ = (
        Index('idx_shop_id', 'shop_id'),
        Index('idx_platform_id', 'platform_id'),
        Index('idx_platform', 'platform'),
        Index('idx_status', 'status'),
        Index('idx_created_at', 'created_at'),
        UniqueConstraint('shop_id', 'platform_id', name='uk_shop_platform'),
        {'comment': '店铺信息表'}
    )
    
    def __repr__(self):
        return f"<Shop(id={self.id}, shop_id='{self.shop_id}', shop_name='{self.shop_name}', platform='{self.platform}')>"
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'shop_id': self.shop_id,
            'shop_name': self.shop_name,
            'platform_id': self.platform_id,
            'platform': self.platform,
            'status': self.status,
            'currency': self.currency,
            'timezone': self.timezone,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Sale(Base):
    """销售记录模型
    
    存储电商平台的销售数据
    """
    __tablename__ = 'sales'
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    
    # 关联店铺
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False, comment='店铺ID')
    
    # 销售基本信息
    sale_date = Column(DateTime, nullable=False, comment='销售日期')
    order_id = Column(String(100), comment='订单ID')
    product_id = Column(String(100), comment='产品ID')
    product_name = Column(String(500), comment='产品名称')
    
    # 销售金额信息
    original_amount = Column(Numeric(15, 4), nullable=False, comment='原始金额')
    original_currency = Column(String(10), nullable=False, comment='原始货币')
    cny_amount = Column(Numeric(15, 4), nullable=False, comment='人民币金额')
    usd_amount = Column(Numeric(15, 4), comment='美元金额')
    
    # 销售数量和单价
    quantity = Column(Integer, default=1, comment='销售数量')
    unit_price = Column(Numeric(15, 4), comment='单价')
    
    # 费用信息
    commission = Column(Numeric(15, 4), default=0, comment='佣金')
    shipping_fee = Column(Numeric(15, 4), default=0, comment='运费')
    tax = Column(Numeric(15, 4), default=0, comment='税费')
    
    # 汇率信息
    exchange_rate = Column(Numeric(10, 6), comment='使用的汇率')
    exchange_rate_date = Column(DateTime, comment='汇率日期')
    
    # 扩展信息
    category = Column(String(100), comment='产品类别')
    region = Column(String(50), comment='销售地区')
    notes = Column(Text, comment='备注信息')
    raw_data = Column(Text, comment='原始数据（JSON格式）')
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关系定义
    shop = relationship('Shop', back_populates='sales')
    
    # 索引定义
    __table_args__ = (
        Index('idx_shop_id', 'shop_id'),
        Index('idx_sale_date', 'sale_date'),
        Index('idx_order_id', 'order_id'),
        Index('idx_product_id', 'product_id'),
        Index('idx_original_currency', 'original_currency'),
        Index('idx_category', 'category'),
        Index('idx_region', 'region'),
        Index('idx_created_at', 'created_at'),
        Index('idx_shop_date', 'shop_id', 'sale_date'),
        UniqueConstraint('shop_id', 'order_id', 'product_id', 'sale_date', name='uk_sale_record'),
        {'comment': '销售记录表'}
    )
    
    def __repr__(self):
        return f"<Sale(id={self.id}, shop_id={self.shop_id}, sale_date='{self.sale_date}', cny_amount={self.cny_amount})>"
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'shop_id': self.shop_id,
            'sale_date': self.sale_date.isoformat() if self.sale_date else None,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'original_amount': str(self.original_amount) if self.original_amount else None,
            'original_currency': self.original_currency,
            'cny_amount': str(self.cny_amount) if self.cny_amount else None,
            'usd_amount': str(self.usd_amount) if self.usd_amount else None,
            'quantity': self.quantity,
            'unit_price': str(self.unit_price) if self.unit_price else None,
            'commission': str(self.commission) if self.commission else None,
            'shipping_fee': str(self.shipping_fee) if self.shipping_fee else None,
            'tax': str(self.tax) if self.tax else None,
            'exchange_rate': str(self.exchange_rate) if self.exchange_rate else None,
            'exchange_rate_date': self.exchange_rate_date.isoformat() if self.exchange_rate_date else None,
            'category': self.category,
            'region': self.region,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ExchangeRate(Base):
    """汇率模型
    
    存储各种货币的汇率信息
    """
    __tablename__ = 'exchange_rates'
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    
    # 汇率基本信息
    currency_code = Column(String(10), nullable=False, comment='货币代码（如USD、EUR）')
    currency_name = Column(String(50), comment='货币名称')
    base_currency = Column(String(10), default='CNY', comment='基准货币（默认人民币）')
    
    # 汇率值
    rate = Column(Numeric(15, 8), nullable=False, comment='汇率值')
    user_rate = Column(Numeric(15, 8), comment='用户自定义汇率')
    
    # 汇率日期和有效期
    rate_date = Column(DateTime, nullable=False, comment='汇率日期')
    effective_date = Column(DateTime, comment='生效日期')
    expiry_date = Column(DateTime, comment='失效日期')
    
    # 汇率来源和状态
    source = Column(String(50), default='api', comment='汇率来源：api-接口获取，manual-手动设置')
    status = Column(String(20), default='active', comment='状态：active-有效，inactive-无效')
    
    # 汇率变化信息
    previous_rate = Column(Numeric(15, 8), comment='前一次汇率')
    change_rate = Column(Numeric(10, 6), comment='变化率')
    change_amount = Column(Numeric(15, 8), comment='变化金额')
    
    # 扩展信息
    description = Column(Text, comment='汇率描述')
    meta_data = Column(Text, comment='元数据（JSON格式）')
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 索引定义
    __table_args__ = (
        Index('idx_currency_code', 'currency_code'),
        Index('idx_base_currency', 'base_currency'),
        Index('idx_rate_date', 'rate_date'),
        Index('idx_effective_date', 'effective_date'),
        Index('idx_status', 'status'),
        Index('idx_source', 'source'),
        Index('idx_created_at', 'created_at'),
        Index('idx_currency_date', 'currency_code', 'rate_date'),
        UniqueConstraint('currency_code', 'base_currency', 'rate_date', name='uk_exchange_rate'),
        {'comment': '汇率信息表'}
    )
    
    def __repr__(self):
        return f"<ExchangeRate(id={self.id}, currency_code='{self.currency_code}', rate={self.rate}, rate_date='{self.rate_date}')>"
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'currency_code': self.currency_code,
            'currency_name': self.currency_name,
            'base_currency': self.base_currency,
            'rate': str(self.rate) if self.rate else None,
            'user_rate': str(self.user_rate) if self.user_rate else None,
            'rate_date': self.rate_date.isoformat() if self.rate_date else None,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'source': self.source,
            'status': self.status,
            'previous_rate': str(self.previous_rate) if self.previous_rate else None,
            'change_rate': str(self.change_rate) if self.change_rate else None,
            'change_amount': str(self.change_amount) if self.change_amount else None,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_latest_rate(cls, session, currency_code: str, base_currency: str = 'CNY'):
        """获取最新汇率
        
        Args:
            session: 数据库会话
            currency_code: 货币代码
            base_currency: 基准货币
            
        Returns:
            最新的汇率记录
        """
        return session.query(cls).filter(
            cls.currency_code == currency_code,
            cls.base_currency == base_currency,
            cls.status == 'active'
        ).order_by(cls.rate_date.desc()).first()
    
    @classmethod
    def get_rate_by_date(cls, session, currency_code: str, rate_date: datetime, base_currency: str = 'CNY'):
        """根据日期获取汇率
        
        Args:
            session: 数据库会话
            currency_code: 货币代码
            rate_date: 汇率日期
            base_currency: 基准货币
            
        Returns:
            指定日期的汇率记录
        """
        return session.query(cls).filter(
            cls.currency_code == currency_code,
            cls.base_currency == base_currency,
            cls.rate_date <= rate_date,
            cls.status == 'active'
        ).order_by(cls.rate_date.desc()).first()


# 导出所有模型
__all__ = ['Base', 'Shop', 'Sale', 'ExchangeRate']