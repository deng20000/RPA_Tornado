# 产品模块数据传输对象模式
# 定义产品相关的请求和响应数据结构

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

from .base_schemas import BaseRequest, BaseResponse, PaginationRequest, DateRangeRequest
from ..shared.enums.business_enums import ProductStatus, Platform


@dataclass
class ProductRequest(BaseRequest):
    """产品请求模式"""
    sid: Optional[str] = None  # 店铺ID
    asin: Optional[str] = None  # ASIN
    sku: Optional[str] = None   # SKU
    marketplace: Optional[str] = None  # 市场
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        return errors


@dataclass
class ProductResponse(BaseResponse):
    """产品响应模式"""
    data: Any = None


@dataclass
class ProductListRequest(PaginationRequest):
    """产品列表请求模式"""
    sid: str = ''  # 店铺ID
    marketplace: Optional[str] = None  # 市场
    category: Optional[str] = None     # 分类
    status: Optional[int] = None       # 状态
    keyword: Optional[str] = None      # 关键词搜索
    price_min: Optional[float] = None  # 最低价格
    price_max: Optional[float] = None  # 最高价格
    sort_by: str = 'created_time'      # 排序字段
    sort_order: str = 'desc'           # 排序方向
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if self.status is not None and self.status not in [ProductStatus.DELETED, ProductStatus.INACTIVE, ProductStatus.ACTIVE]:
            errors.append("产品状态无效")
            
        if self.price_min is not None and self.price_min < 0:
            errors.append("最低价格不能小于0")
            
        if self.price_max is not None and self.price_max < 0:
            errors.append("最高价格不能小于0")
            
        if self.price_min is not None and self.price_max is not None and self.price_min > self.price_max:
            errors.append("最低价格不能大于最高价格")
            
        valid_sort_fields = ['created_time', 'updated_time', 'price', 'sales_rank', 'title']
        if self.sort_by not in valid_sort_fields:
            errors.append(f"排序字段只能是: {', '.join(valid_sort_fields)}")
            
        if self.sort_order not in ['asc', 'desc']:
            errors.append("排序方向只能是 asc 或 desc")
            
        return errors


@dataclass
class ProductInfo:
    """产品信息"""
    asin: str = ''
    sku: str = ''
    title: str = ''
    marketplace: str = ''
    category: str = ''
    price: float = 0.0
    currency: str = 'USD'
    status: int = 0
    sales_rank: Optional[int] = None
    review_count: int = 0
    review_rating: float = 0.0
    image_url: Optional[str] = None
    created_time: Optional[str] = None
    updated_time: Optional[str] = None
    
    # 库存信息
    inventory_quantity: Optional[int] = None
    reserved_quantity: Optional[int] = None
    available_quantity: Optional[int] = None
    
    # 销售信息
    total_sales: Optional[float] = None
    total_orders: Optional[int] = None
    last_sale_date: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'asin': self.asin,
            'sku': self.sku,
            'title': self.title,
            'marketplace': self.marketplace,
            'category': self.category,
            'price': self.price,
            'currency': self.currency,
            'status': self.status,
            'status_name': ProductStatus.get_description(self.status),
            'sales_rank': self.sales_rank,
            'review_count': self.review_count,
            'review_rating': self.review_rating,
            'image_url': self.image_url,
            'created_time': self.created_time,
            'updated_time': self.updated_time
        }
        
        # 添加可选字段
        if self.inventory_quantity is not None:
            result['inventory_quantity'] = self.inventory_quantity
        if self.reserved_quantity is not None:
            result['reserved_quantity'] = self.reserved_quantity
        if self.available_quantity is not None:
            result['available_quantity'] = self.available_quantity
        if self.total_sales is not None:
            result['total_sales'] = self.total_sales
        if self.total_orders is not None:
            result['total_orders'] = self.total_orders
        if self.last_sale_date is not None:
            result['last_sale_date'] = self.last_sale_date
            
        return result


@dataclass
class ProductListResponse(BaseResponse):
    """产品列表响应模式"""
    data: List[ProductInfo] = field(default_factory=list)
    total: int = 0
    summary: Optional[Dict[str, Any]] = None


@dataclass
class ProductDetailRequest(ProductRequest):
    """产品详情请求模式"""
    include_inventory: bool = False  # 是否包含库存信息
    include_sales: bool = False      # 是否包含销售信息
    include_reviews: bool = False    # 是否包含评论信息
    include_images: bool = False     # 是否包含图片信息


@dataclass
class ProductDetailInfo(ProductInfo):
    """产品详情信息"""
    description: Optional[str] = None
    features: List[str] = field(default_factory=list)
    dimensions: Optional[Dict[str, Any]] = None
    weight: Optional[float] = None
    brand: Optional[str] = None
    manufacturer: Optional[str] = None
    
    # 扩展图片信息
    images: List[str] = field(default_factory=list)
    
    # 扩展评论信息
    recent_reviews: List[Dict[str, Any]] = field(default_factory=list)
    
    # 扩展销售信息
    sales_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        
        # 添加详情字段
        result.update({
            'description': self.description,
            'features': self.features,
            'dimensions': self.dimensions,
            'weight': self.weight,
            'brand': self.brand,
            'manufacturer': self.manufacturer,
            'images': self.images,
            'recent_reviews': self.recent_reviews,
            'sales_history': self.sales_history
        })
        
        return result


@dataclass
class ProductDetailResponse(BaseResponse):
    """产品详情响应模式"""
    data: Optional[ProductDetailInfo] = None


@dataclass
class CreateProductRequest(BaseRequest):
    """创建产品请求模式"""
    sid: str = ''
    sku: str = ''
    title: str = ''
    marketplace: str = ''
    category: str = ''
    price: float = 0.0
    currency: str = 'USD'
    description: Optional[str] = None
    features: List[str] = field(default_factory=list)
    dimensions: Optional[Dict[str, Any]] = None
    weight: Optional[float] = None
    brand: Optional[str] = None
    manufacturer: Optional[str] = None
    images: List[str] = field(default_factory=list)
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.sku:
            errors.append("SKU不能为空")
            
        if not self.title:
            errors.append("产品标题不能为空")
            
        if not self.marketplace:
            errors.append("市场不能为空")
            
        if not self.category:
            errors.append("分类不能为空")
            
        if self.price <= 0:
            errors.append("价格必须大于0")
            
        if len(self.title) > 200:
            errors.append("产品标题不能超过200个字符")
            
        if self.description and len(self.description) > 2000:
            errors.append("产品描述不能超过2000个字符")
            
        if len(self.images) > 10:
            errors.append("图片数量不能超过10张")
            
        return errors


@dataclass
class CreateProductResponse(BaseResponse):
    """创建产品响应模式"""
    data: Optional[Dict[str, Any]] = None
    message: str = "产品创建成功"


@dataclass
class UpdateProductRequest(BaseRequest):
    """更新产品请求模式"""
    sid: str = ''
    asin: str = ''
    title: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    features: Optional[List[str]] = None
    status: Optional[int] = None
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.asin:
            errors.append("ASIN不能为空")
            
        if self.price is not None and self.price <= 0:
            errors.append("价格必须大于0")
            
        if self.title and len(self.title) > 200:
            errors.append("产品标题不能超过200个字符")
            
        if self.description and len(self.description) > 2000:
            errors.append("产品描述不能超过2000个字符")
            
        if self.status is not None and self.status not in [ProductStatus.DELETED, ProductStatus.INACTIVE, ProductStatus.ACTIVE]:
            errors.append("产品状态无效")
            
        # 至少需要更新一个字段
        if not any([
            self.title,
            self.price is not None,
            self.description,
            self.features,
            self.status is not None
        ]):
            errors.append("至少需要更新一个字段")
            
        return errors


@dataclass
class UpdateProductResponse(BaseResponse):
    """更新产品响应模式"""
    message: str = "产品更新成功"


@dataclass
class DeleteProductRequest(BaseRequest):
    """删除产品请求模式"""
    sid: str = ''
    asin: str = ''
    force_delete: bool = False  # 是否强制删除
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.asin:
            errors.append("ASIN不能为空")
            
        return errors


@dataclass
class DeleteProductResponse(BaseResponse):
    """删除产品响应模式"""
    message: str = "产品删除成功"


@dataclass
class ProductInventoryRequest(BaseRequest):
    """产品库存请求模式"""
    sid: str = ''
    asin: Optional[str] = None
    sku: Optional[str] = None
    marketplace: Optional[str] = None
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.asin and not self.sku:
            errors.append("ASIN或SKU至少需要提供一个")
            
        return errors


@dataclass
class ProductInventoryInfo:
    """产品库存信息"""
    asin: str = ''
    sku: str = ''
    marketplace: str = ''
    total_quantity: int = 0
    available_quantity: int = 0
    reserved_quantity: int = 0
    inbound_quantity: int = 0
    last_updated: str = ''
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'asin': self.asin,
            'sku': self.sku,
            'marketplace': self.marketplace,
            'total_quantity': self.total_quantity,
            'available_quantity': self.available_quantity,
            'reserved_quantity': self.reserved_quantity,
            'inbound_quantity': self.inbound_quantity,
            'last_updated': self.last_updated
        }


@dataclass
class ProductInventoryResponse(BaseResponse):
    """产品库存响应模式"""
    data: Optional[ProductInventoryInfo] = None


@dataclass
class BatchProductRequest(BaseRequest):
    """批量产品操作请求模式"""
    sid: str = ''
    operation: str = ''  # 操作类型: update_status, update_price, delete
    asins: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)  # 操作参数
    
    def validate(self) -> List[str]:
        """验证请求参数"""
        errors = super().validate()
        
        if not self.sid:
            errors.append("店铺ID(sid)不能为空")
            
        if not self.asins:
            errors.append("ASIN列表不能为空")
            
        if len(self.asins) > 100:
            errors.append("批量操作的ASIN数量不能超过100个")
            
        valid_operations = ['update_status', 'update_price', 'delete']
        if self.operation not in valid_operations:
            errors.append(f"操作类型只能是: {', '.join(valid_operations)}")
            
        # 根据操作类型验证参数
        if self.operation == 'update_status':
            if 'status' not in self.params:
                errors.append("更新状态操作需要提供status参数")
            elif self.params['status'] not in [ProductStatus.DELETED, ProductStatus.INACTIVE, ProductStatus.ACTIVE]:
                errors.append("状态值无效")
                
        elif self.operation == 'update_price':
            if 'price' not in self.params:
                errors.append("更新价格操作需要提供price参数")
            elif self.params['price'] <= 0:
                errors.append("价格必须大于0")
                
        return errors


@dataclass
class BatchProductResponse(BaseResponse):
    """批量产品响应模式"""
    data: Dict[str, Any] = field(default_factory=dict)
    message: str = "批量操作完成"