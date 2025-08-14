# 产品领域服务
# 处理产品相关的业务逻辑

import asyncio
import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime
from decimal import Decimal

from ...core.exceptions.base_exceptions import ValidationError, BusinessLogicError, NotFoundError
from ...shared.enums.business_enums import Platform, ProductStatus
from ...shared.constants.business_constants import (
    DEFAULT_BATCH_SIZE,
    MAX_BATCH_SIZE,
    SUPPORTED_PLATFORMS
)

# 导入原有的服务（临时兼容）
try:
    from ...services.product_service import ProductService as OriginalProductService
except ImportError:
    OriginalProductService = None


class ProductService:
    """产品服务"""
    
    def __init__(self):
        # 临时兼容原有服务
        self._original_service = OriginalProductService() if OriginalProductService else None
    
    async def get_product_list(
        self,
        platform: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        keyword: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """获取产品列表
        
        Args:
            platform: 平台
            category: 分类
            status: 状态
            keyword: 关键词
            price_min: 最低价格
            price_max: 最高价格
            page: 页码
            page_size: 每页大小
            
        Returns:
            产品列表数据
        """
        try:
            # 参数验证
            if page < 1:
                raise ValidationError("页码必须大于0")
            
            if page_size < 1 or page_size > MAX_BATCH_SIZE:
                raise ValidationError(f"每页大小必须在1-{MAX_BATCH_SIZE}之间")
            
            if platform and platform not in SUPPORTED_PLATFORMS:
                raise ValidationError(f"不支持的平台: {platform}")
            
            if price_min is not None and price_min < 0:
                raise ValidationError("最低价格不能小于0")
            
            if price_max is not None and price_max < 0:
                raise ValidationError("最高价格不能小于0")
            
            if price_min is not None and price_max is not None and price_min > price_max:
                raise ValidationError("最低价格不能大于最高价格")
            
            # 如果有原有服务，优先使用
            if self._original_service:
                try:
                    if hasattr(self._original_service, 'get_product_list'):
                        result = await self._call_original_service(
                            'get_product_list',
                            {
                                'platform': platform,
                                'category': category,
                                'status': status,
                                'keyword': keyword,
                                'price_min': price_min,
                                'price_max': price_max,
                                'page': page,
                                'page_size': page_size
                            }
                        )
                        return result
                except Exception as e:
                    print(f"调用原有服务失败: {e}")
            
            # 新的业务逻辑实现
            return await self._get_product_list_new(
                platform, category, status, keyword, price_min, price_max, page, page_size
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"获取产品列表失败: {str(e)}")
    
    async def get_product_detail(
        self,
        product_id: str,
        platform: Optional[str] = None,
        include_variants: bool = False,
        include_inventory: bool = False
    ) -> Dict[str, Any]:
        """获取产品详情
        
        Args:
            product_id: 产品ID
            platform: 平台
            include_variants: 是否包含变体
            include_inventory: 是否包含库存
            
        Returns:
            产品详情数据
        """
        try:
            # 参数验证
            if not product_id:
                raise ValidationError("产品ID不能为空")
            
            if platform and platform not in SUPPORTED_PLATFORMS:
                raise ValidationError(f"不支持的平台: {platform}")
            
            # 如果有原有服务，优先使用
            if self._original_service:
                try:
                    if hasattr(self._original_service, 'get_product_detail'):
                        result = await self._call_original_service(
                            'get_product_detail',
                            {
                                'product_id': product_id,
                                'platform': platform,
                                'include_variants': include_variants,
                                'include_inventory': include_inventory
                            }
                        )
                        return result
                except Exception as e:
                    print(f"调用原有服务失败: {e}")
            
            # 新的业务逻辑实现
            return await self._get_product_detail_new(
                product_id, platform, include_variants, include_inventory
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"获取产品详情失败: {str(e)}")
    
    async def create_product(
        self,
        title: str,
        description: Optional[str] = None,
        price: float = 0.0,
        category: Optional[str] = None,
        platform: Optional[str] = None,
        sku: Optional[str] = None,
        inventory: int = 0,
        images: Optional[List[str]] = None,
        attributes: Optional[Dict[str, Any]] = None,
        variants: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """创建产品
        
        Args:
            title: 产品标题
            description: 产品描述
            price: 价格
            category: 分类
            platform: 平台
            sku: SKU
            inventory: 库存
            images: 图片列表
            attributes: 属性
            variants: 变体列表
            
        Returns:
            创建结果
        """
        try:
            # 参数验证
            if not title or len(title.strip()) == 0:
                raise ValidationError("产品标题不能为空")
            
            if len(title) > 200:
                raise ValidationError("产品标题不能超过200个字符")
            
            if price < 0:
                raise ValidationError("价格不能小于0")
            
            if inventory < 0:
                raise ValidationError("库存不能小于0")
            
            if platform and platform not in SUPPORTED_PLATFORMS:
                raise ValidationError(f"不支持的平台: {platform}")
            
            if description and len(description) > 5000:
                raise ValidationError("产品描述不能超过5000个字符")
            
            # 新的业务逻辑实现
            return await self._create_product_new(
                title, description, price, category, platform, sku, inventory, images, attributes, variants
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"创建产品失败: {str(e)}")
    
    async def update_product(
        self,
        product_id: str,
        platform: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        category: Optional[str] = None,
        sku: Optional[str] = None,
        inventory: Optional[int] = None,
        images: Optional[List[str]] = None,
        attributes: Optional[Dict[str, Any]] = None,
        variants: Optional[List[Dict[str, Any]]] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """更新产品
        
        Args:
            product_id: 产品ID
            platform: 平台
            title: 产品标题
            description: 产品描述
            price: 价格
            category: 分类
            sku: SKU
            inventory: 库存
            images: 图片列表
            attributes: 属性
            variants: 变体列表
            status: 状态
            
        Returns:
            更新结果
        """
        try:
            # 参数验证
            if not product_id:
                raise ValidationError("产品ID不能为空")
            
            if platform and platform not in SUPPORTED_PLATFORMS:
                raise ValidationError(f"不支持的平台: {platform}")
            
            if title is not None:
                if not title or len(title.strip()) == 0:
                    raise ValidationError("产品标题不能为空")
                if len(title) > 200:
                    raise ValidationError("产品标题不能超过200个字符")
            
            if price is not None and price < 0:
                raise ValidationError("价格不能小于0")
            
            if inventory is not None and inventory < 0:
                raise ValidationError("库存不能小于0")
            
            if description is not None and len(description) > 5000:
                raise ValidationError("产品描述不能超过5000个字符")
            
            # 新的业务逻辑实现
            return await self._update_product_new(
                product_id, platform, title, description, price, category, sku, 
                inventory, images, attributes, variants, status
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"更新产品失败: {str(e)}")
    
    async def delete_product(
        self,
        product_id: str,
        platform: Optional[str] = None,
        force_delete: bool = False
    ) -> Dict[str, Any]:
        """删除产品
        
        Args:
            product_id: 产品ID
            platform: 平台
            force_delete: 是否强制删除
            
        Returns:
            删除结果
        """
        try:
            # 参数验证
            if not product_id:
                raise ValidationError("产品ID不能为空")
            
            if platform and platform not in SUPPORTED_PLATFORMS:
                raise ValidationError(f"不支持的平台: {platform}")
            
            # 新的业务逻辑实现
            return await self._delete_product_new(product_id, platform, force_delete)
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"删除产品失败: {str(e)}")
    
    async def get_product_inventory(
        self,
        product_id: str,
        platform: Optional[str] = None,
        warehouse: Optional[str] = None,
        include_reserved: bool = False
    ) -> Dict[str, Any]:
        """获取产品库存
        
        Args:
            product_id: 产品ID
            platform: 平台
            warehouse: 仓库
            include_reserved: 是否包含预留库存
            
        Returns:
            库存数据
        """
        try:
            # 参数验证
            if not product_id:
                raise ValidationError("产品ID不能为空")
            
            if platform and platform not in SUPPORTED_PLATFORMS:
                raise ValidationError(f"不支持的平台: {platform}")
            
            # 新的业务逻辑实现
            return await self._get_product_inventory_new(
                product_id, platform, warehouse, include_reserved
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"获取产品库存失败: {str(e)}")
    
    async def batch_product_operation(
        self,
        operation: str,
        product_ids: List[str],
        platform: Optional[str] = None,
        operation_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """批量产品操作
        
        Args:
            operation: 操作类型
            product_ids: 产品ID列表
            platform: 平台
            operation_data: 操作数据
            
        Returns:
            操作结果
        """
        try:
            # 参数验证
            if not operation:
                raise ValidationError("操作类型不能为空")
            
            if operation not in ['update_price', 'update_inventory', 'update_status', 'delete']:
                raise ValidationError("不支持的操作类型")
            
            if not product_ids:
                raise ValidationError("产品ID列表不能为空")
            
            if len(product_ids) > MAX_BATCH_SIZE:
                raise ValidationError(f"批量操作产品数量不能超过{MAX_BATCH_SIZE}")
            
            if platform and platform not in SUPPORTED_PLATFORMS:
                raise ValidationError(f"不支持的平台: {platform}")
            
            # 新的业务逻辑实现
            return await self._batch_product_operation_new(
                operation, product_ids, platform, operation_data
            )
            
        except ValidationError:
            raise
        except Exception as e:
            raise BusinessLogicError(f"批量产品操作失败: {str(e)}")
    
    async def _call_original_service(self, method_name: str, params: Dict[str, Any]) -> Any:
        """调用原有服务方法"""
        if not self._original_service:
            raise BusinessLogicError("原有服务不可用")
        
        method = getattr(self._original_service, method_name, None)
        if not method:
            raise BusinessLogicError(f"方法 {method_name} 不存在")
        
        # 如果是异步方法
        if asyncio.iscoroutinefunction(method):
            return await method(**params)
        else:
            # 如果是同步方法，在线程池中执行
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: method(**params))
    
    async def _get_product_list_new(
        self, platform: Optional[str], category: Optional[str], status: Optional[str],
        keyword: Optional[str], price_min: Optional[float], price_max: Optional[float],
        page: int, page_size: int
    ) -> Dict[str, Any]:
        """新的获取产品列表实现"""
        # TODO: 实现新的产品列表逻辑
        
        # 模拟数据
        mock_products = [
            {
                'product_id': 'PROD001',
                'title': '测试产品1',
                'description': '这是一个测试产品',
                'price': 29.99,
                'category': 'Electronics',
                'platform': platform or 'amazon',
                'sku': 'SKU001',
                'inventory': 100,
                'status': 'active',
                'images': ['https://example.com/image1.jpg'],
                'created_at': '2024-01-01 00:00:00',
                'updated_at': '2024-01-01 00:00:00'
            },
            {
                'product_id': 'PROD002',
                'title': '测试产品2',
                'description': '这是另一个测试产品',
                'price': 49.99,
                'category': 'Home',
                'platform': platform or 'amazon',
                'sku': 'SKU002',
                'inventory': 50,
                'status': 'active',
                'images': ['https://example.com/image2.jpg'],
                'created_at': '2024-01-02 00:00:00',
                'updated_at': '2024-01-02 00:00:00'
            }
        ]
        
        # 筛选逻辑
        filtered_products = mock_products
        
        if category:
            filtered_products = [p for p in filtered_products if p['category'] == category]
        
        if status:
            filtered_products = [p for p in filtered_products if p['status'] == status]
        
        if keyword:
            filtered_products = [p for p in filtered_products if keyword.lower() in p['title'].lower()]
        
        if price_min is not None:
            filtered_products = [p for p in filtered_products if p['price'] >= price_min]
        
        if price_max is not None:
            filtered_products = [p for p in filtered_products if p['price'] <= price_max]
        
        # 分页处理
        total = len(filtered_products)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_products = filtered_products[start_idx:end_idx]
        
        return {
            'data': paginated_products,
            'total': total
        }
    
    async def _get_product_detail_new(
        self, product_id: str, platform: Optional[str], 
        include_variants: bool, include_inventory: bool
    ) -> Dict[str, Any]:
        """新的获取产品详情实现"""
        # TODO: 实现新的产品详情逻辑
        
        # 模拟查找产品
        if product_id not in ['PROD001', 'PROD002']:
            raise NotFoundError(f"产品 {product_id} 不存在")
        
        # 模拟产品详情数据
        product_detail = {
            'product_id': product_id,
            'title': f'测试产品 {product_id}',
            'description': '这是一个详细的产品描述',
            'price': 29.99,
            'category': 'Electronics',
            'platform': platform or 'amazon',
            'sku': f'SKU{product_id[-3:]}',
            'inventory': 100,
            'status': 'active',
            'images': [f'https://example.com/{product_id.lower()}.jpg'],
            'attributes': {
                'brand': 'TestBrand',
                'color': 'Black',
                'size': 'Medium'
            },
            'created_at': '2024-01-01 00:00:00',
            'updated_at': '2024-01-01 00:00:00'
        }
        
        # 包含变体信息
        if include_variants:
            product_detail['variants'] = [
                {
                    'variant_id': f'{product_id}_V1',
                    'sku': f'SKU{product_id[-3:]}_V1',
                    'price': 29.99,
                    'inventory': 50,
                    'attributes': {'color': 'Black', 'size': 'Small'}
                },
                {
                    'variant_id': f'{product_id}_V2',
                    'sku': f'SKU{product_id[-3:]}_V2',
                    'price': 34.99,
                    'inventory': 30,
                    'attributes': {'color': 'White', 'size': 'Large'}
                }
            ]
        
        # 包含库存信息
        if include_inventory:
            product_detail['inventory_details'] = {
                'total_inventory': 100,
                'available_inventory': 80,
                'reserved_inventory': 20,
                'warehouses': [
                    {
                        'warehouse_id': 'WH001',
                        'warehouse_name': '主仓库',
                        'inventory': 60
                    },
                    {
                        'warehouse_id': 'WH002',
                        'warehouse_name': '备用仓库',
                        'inventory': 40
                    }
                ]
            }
        
        return {'product': product_detail}
    
    async def _create_product_new(
        self, title: str, description: Optional[str], price: float, category: Optional[str],
        platform: Optional[str], sku: Optional[str], inventory: int, images: Optional[List[str]],
        attributes: Optional[Dict[str, Any]], variants: Optional[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:
        """新的创建产品实现"""
        # TODO: 实现新的创建产品逻辑
        
        # 生成产品ID
        product_id = f"PROD{str(uuid.uuid4())[:8].upper()}"
        
        # 创建产品数据
        product_data = {
            'product_id': product_id,
            'title': title,
            'description': description,
            'price': price,
            'category': category,
            'platform': platform or 'amazon',
            'sku': sku or f"SKU{product_id[-8:]}",
            'inventory': inventory,
            'status': 'active',
            'images': images or [],
            'attributes': attributes or {},
            'variants': variants or [],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return {
            'product': product_data,
            'success': True,
            'message': '产品创建成功'
        }
    
    async def _update_product_new(
        self, product_id: str, platform: Optional[str], title: Optional[str],
        description: Optional[str], price: Optional[float], category: Optional[str],
        sku: Optional[str], inventory: Optional[int], images: Optional[List[str]],
        attributes: Optional[Dict[str, Any]], variants: Optional[List[Dict[str, Any]]],
        status: Optional[str]
    ) -> Dict[str, Any]:
        """新的更新产品实现"""
        # TODO: 实现新的更新产品逻辑
        
        # 模拟查找产品
        if product_id not in ['PROD001', 'PROD002']:
            raise NotFoundError(f"产品 {product_id} 不存在")
        
        # 模拟更新产品数据
        updated_product = {
            'product_id': product_id,
            'title': title or f'更新的产品 {product_id}',
            'description': description or '更新的产品描述',
            'price': price or 39.99,
            'category': category or 'Electronics',
            'platform': platform or 'amazon',
            'sku': sku or f'SKU{product_id[-3:]}',
            'inventory': inventory or 150,
            'status': status or 'active',
            'images': images or [f'https://example.com/{product_id.lower()}_updated.jpg'],
            'attributes': attributes or {'updated': True},
            'variants': variants or [],
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return {
            'product': updated_product,
            'success': True,
            'message': '产品更新成功'
        }
    
    async def _delete_product_new(
        self, product_id: str, platform: Optional[str], force_delete: bool
    ) -> Dict[str, Any]:
        """新的删除产品实现"""
        # TODO: 实现新的删除产品逻辑
        
        # 模拟查找产品
        if product_id not in ['PROD001', 'PROD002']:
            raise NotFoundError(f"产品 {product_id} 不存在")
        
        # 模拟删除检查
        if not force_delete:
            # 检查是否有关联订单等
            pass
        
        return {
            'product_id': product_id,
            'success': True,
            'message': '产品删除成功',
            'force_delete': force_delete
        }
    
    async def _get_product_inventory_new(
        self, product_id: str, platform: Optional[str], warehouse: Optional[str], include_reserved: bool
    ) -> Dict[str, Any]:
        """新的获取产品库存实现"""
        # TODO: 实现新的产品库存逻辑
        
        # 模拟查找产品
        if product_id not in ['PROD001', 'PROD002']:
            raise NotFoundError(f"产品 {product_id} 不存在")
        
        # 模拟库存数据
        inventory_data = {
            'product_id': product_id,
            'platform': platform or 'amazon',
            'total_inventory': 100,
            'available_inventory': 80,
            'warehouses': [
                {
                    'warehouse_id': 'WH001',
                    'warehouse_name': '主仓库',
                    'inventory': 60,
                    'available': 50,
                    'reserved': 10 if include_reserved else None
                },
                {
                    'warehouse_id': 'WH002',
                    'warehouse_name': '备用仓库',
                    'inventory': 40,
                    'available': 30,
                    'reserved': 10 if include_reserved else None
                }
            ],
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 筛选仓库
        if warehouse:
            inventory_data['warehouses'] = [
                w for w in inventory_data['warehouses'] if w['warehouse_id'] == warehouse
            ]
        
        return {'inventory': inventory_data}
    
    async def _batch_product_operation_new(
        self, operation: str, product_ids: List[str], platform: Optional[str], operation_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """新的批量产品操作实现"""
        # TODO: 实现新的批量产品操作逻辑
        
        # 模拟批量操作结果
        results = []
        for product_id in product_ids:
            if product_id in ['PROD001', 'PROD002']:
                results.append({
                    'product_id': product_id,
                    'success': True,
                    'message': f'{operation} 操作成功'
                })
            else:
                results.append({
                    'product_id': product_id,
                    'success': False,
                    'message': f'产品 {product_id} 不存在'
                })
        
        success_count = sum(1 for r in results if r['success'])
        
        return {
            'operation': operation,
            'total_count': len(product_ids),
            'success_count': success_count,
            'failed_count': len(product_ids) - success_count,
            'results': results,
            'operation_data': operation_data
        }