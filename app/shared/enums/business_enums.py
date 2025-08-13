# 业务相关枚举类型
# 定义业务逻辑相关的枚举

from enum import Enum, IntEnum


class AsinType(IntEnum):
    """ASIN类型枚举"""
    ASIN = 1  # 按ASIN查询
    MSKU = 2  # 按MSKU查询
    
    @classmethod
    def get_description(cls, value: int) -> str:
        """获取类型描述"""
        descriptions = {
            cls.ASIN: 'ASIN',
            cls.MSKU: 'MSKU'
        }
        return descriptions.get(value, '未知类型')


class ReportType(IntEnum):
    """报表类型枚举"""
    SALES = 1      # 销售额
    QUANTITY = 2   # 销量
    ORDERS = 3     # 订单量
    
    @classmethod
    def get_description(cls, value: int) -> str:
        """获取类型描述"""
        descriptions = {
            cls.SALES: '销售额',
            cls.QUANTITY: '销量',
            cls.ORDERS: '订单量'
        }
        return descriptions.get(value, '未知类型')


class SellerStatus(IntEnum):
    """店铺状态枚举"""
    SUSPENDED = -1  # 暂停
    INACTIVE = 0    # 非活跃
    ACTIVE = 1      # 活跃
    
    @classmethod
    def get_description(cls, value: int) -> str:
        """获取状态描述"""
        descriptions = {
            cls.SUSPENDED: '暂停',
            cls.INACTIVE: '非活跃',
            cls.ACTIVE: '活跃'
        }
        return descriptions.get(value, '未知状态')


class ProductStatus(IntEnum):
    """产品状态枚举"""
    DELETED = -1    # 已删除
    INACTIVE = 0    # 禁用
    ACTIVE = 1      # 启用
    
    @classmethod
    def get_description(cls, value: int) -> str:
        """获取状态描述"""
        descriptions = {
            cls.DELETED: '已删除',
            cls.INACTIVE: '禁用',
            cls.ACTIVE: '启用'
        }
        return descriptions.get(value, '未知状态')


class Platform(Enum):
    """平台类型枚举"""
    AMAZON = 'amazon'
    EBAY = 'ebay'
    WALMART = 'walmart'
    SHOPIFY = 'shopify'
    ALIEXPRESS = 'aliexpress'
    WISH = 'wish'
    
    @classmethod
    def get_description(cls, value: str) -> str:
        """获取平台描述"""
        descriptions = {
            cls.AMAZON.value: '亚马逊',
            cls.EBAY.value: 'eBay',
            cls.WALMART.value: '沃尔玛',
            cls.SHOPIFY.value: 'Shopify',
            cls.ALIEXPRESS.value: '速卖通',
            cls.WISH.value: 'Wish'
        }
        return descriptions.get(value, '未知平台')


class Currency(Enum):
    """货币类型枚举"""
    USD = 'USD'  # 美元
    EUR = 'EUR'  # 欧元
    GBP = 'GBP'  # 英镑
    JPY = 'JPY'  # 日元
    CNY = 'CNY'  # 人民币
    CAD = 'CAD'  # 加拿大元
    AUD = 'AUD'  # 澳大利亚元
    
    @classmethod
    def get_description(cls, value: str) -> str:
        """获取货币描述"""
        descriptions = {
            cls.USD.value: '美元',
            cls.EUR.value: '欧元',
            cls.GBP.value: '英镑',
            cls.JPY.value: '日元',
            cls.CNY.value: '人民币',
            cls.CAD.value: '加拿大元',
            cls.AUD.value: '澳大利亚元'
        }
        return descriptions.get(value, '未知货币')


class Market(Enum):
    """市场类型枚举"""
    US = 'US'    # 美国
    UK = 'UK'    # 英国
    DE = 'DE'    # 德国
    FR = 'FR'    # 法国
    IT = 'IT'    # 意大利
    ES = 'ES'    # 西班牙
    JP = 'JP'    # 日本
    CA = 'CA'    # 加拿大
    AU = 'AU'    # 澳大利亚
    
    @classmethod
    def get_description(cls, value: str) -> str:
        """获取市场描述"""
        descriptions = {
            cls.US.value: '美国',
            cls.UK.value: '英国',
            cls.DE.value: '德国',
            cls.FR.value: '法国',
            cls.IT.value: '意大利',
            cls.ES.value: '西班牙',
            cls.JP.value: '日本',
            cls.CA.value: '加拿大',
            cls.AU.value: '澳大利亚'
        }
        return descriptions.get(value, '未知市场')


class FileType(Enum):
    """文件类型枚举"""
    EXCEL = 'excel'
    CSV = 'csv'
    PDF = 'pdf'
    JSON = 'json'
    XML = 'xml'
    TXT = 'txt'
    
    @classmethod
    def get_description(cls, value: str) -> str:
        """获取文件类型描述"""
        descriptions = {
            cls.EXCEL.value: 'Excel文件',
            cls.CSV.value: 'CSV文件',
            cls.PDF.value: 'PDF文件',
            cls.JSON.value: 'JSON文件',
            cls.XML.value: 'XML文件',
            cls.TXT.value: '文本文件'
        }
        return descriptions.get(value, '未知文件类型')


class OperationType(Enum):
    """操作类型枚举"""
    CREATE = 'create'    # 创建
    UPDATE = 'update'    # 更新
    DELETE = 'delete'    # 删除
    QUERY = 'query'      # 查询
    EXPORT = 'export'    # 导出
    IMPORT = 'import'    # 导入
    SYNC = 'sync'        # 同步
    
    @classmethod
    def get_description(cls, value: str) -> str:
        """获取操作类型描述"""
        descriptions = {
            cls.CREATE.value: '创建',
            cls.UPDATE.value: '更新',
            cls.DELETE.value: '删除',
            cls.QUERY.value: '查询',
            cls.EXPORT.value: '导出',
            cls.IMPORT.value: '导入',
            cls.SYNC.value: '同步'
        }
        return descriptions.get(value, '未知操作')