# 产品领域处理器
# 处理产品相关的HTTP请求

import json
import logging
from typing import Any, Dict, Optional

from tornado.web import RequestHandler
from tornado.httpclient import HTTPError

from ...core.exceptions.base_exceptions import ValidationError, BusinessLogicError, NotFoundError
from ...schemas.product_schemas import (
    ProductListRequest,
    ProductListResponse,
    ProductDetailRequest,
    ProductDetailResponse,
    CreateProductRequest,
    CreateProductResponse,
    UpdateProductRequest,
    UpdateProductResponse,
    DeleteProductRequest,
    DeleteProductResponse,
    ProductInventoryRequest,
    ProductInventoryResponse,
    BatchProductRequest,
    BatchProductResponse
)
from .services import ProductService

# 配置日志
logger = logging.getLogger(__name__)


class BaseProductHandler(RequestHandler):
    """产品处理器基类"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ProductService()
    
    def set_default_headers(self):
        """设置默认响应头"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    
    async def options(self, *args):
        """处理OPTIONS请求"""
        self.set_status(204)
        await self.finish()
    
    def write_response(self, data: Any, status_code: int = 200):
        """写入响应数据"""
        self.set_status(status_code)
        if data is not None:
            self.write(json.dumps(data, ensure_ascii=False, default=str))
    
    def write_error_response(self, error_message: str, status_code: int = 400, error_code: str = None):
        """写入错误响应"""
        error_data = {
            "error": True,
            "message": error_message,
            "code": error_code or "UNKNOWN_ERROR"
        }
        self.write_response(error_data, status_code)
    
    async def parse_json_body(self) -> Dict[str, Any]:
        """解析JSON请求体"""
        try:
            if self.request.body:
                return json.loads(self.request.body.decode('utf-8'))
            return {}
        except json.JSONDecodeError as e:
            raise ValidationError(f"无效的JSON格式: {str(e)}")
    
    def get_query_params(self) -> Dict[str, Any]:
        """获取查询参数"""
        params = {}
        for key, values in self.request.arguments.items():
            if len(values) == 1:
                # 尝试转换数据类型
                value = values[0].decode('utf-8')
                if value.isdigit():
                    params[key] = int(value)
                elif value.lower() in ('true', 'false'):
                    params[key] = value.lower() == 'true'
                else:
                    params[key] = value
            else:
                params[key] = [v.decode('utf-8') for v in values]
        return params


class ProductListHandler(BaseProductHandler):
    """产品列表处理器"""
    
    async def get(self):
        """获取产品列表"""
        try:
            # 获取查询参数
            params = self.get_query_params()
            
            # 验证请求参数
            request_data = ProductListRequest(**params)
            
            # 调用服务获取数据
            result = await self.service.get_product_list(
                platform=request_data.platform,
                category=request_data.category,
                status=request_data.status,
                keyword=request_data.keyword,
                price_min=request_data.price_min,
                price_max=request_data.price_max,
                page=request_data.page,
                page_size=request_data.page_size
            )
            
            # 验证响应数据
            response_data = ProductListResponse(**result)
            
            # 返回响应
            self.write_response(response_data.dict())
            
        except ValidationError as e:
            logger.warning(f"产品列表请求参数验证失败: {str(e)}")
            self.write_error_response(str(e), 400, "VALIDATION_ERROR")
        except BusinessLogicError as e:
            logger.error(f"产品列表业务逻辑错误: {str(e)}")
            self.write_error_response(str(e), 422, "BUSINESS_LOGIC_ERROR")
        except Exception as e:
            logger.error(f"产品列表处理异常: {str(e)}")
            self.write_error_response("服务器内部错误", 500, "INTERNAL_ERROR")


class ProductDetailHandler(BaseProductHandler):
    """产品详情处理器"""
    
    async def get(self):
        """获取产品详情"""
        try:
            # 获取查询参数
            params = self.get_query_params()
            
            # 验证请求参数
            request_data = ProductDetailRequest(**params)
            
            # 调用服务获取数据
            result = await self.service.get_product_detail(
                product_id=request_data.product_id,
                platform=request_data.platform,
                include_variants=request_data.include_variants,
                include_inventory=request_data.include_inventory
            )
            
            # 验证响应数据
            response_data = ProductDetailResponse(**result)
            
            # 返回响应
            self.write_response(response_data.dict())
            
        except ValidationError as e:
            logger.warning(f"产品详情请求参数验证失败: {str(e)}")
            self.write_error_response(str(e), 400, "VALIDATION_ERROR")
        except NotFoundError as e:
            logger.warning(f"产品未找到: {str(e)}")
            self.write_error_response(str(e), 404, "NOT_FOUND")
        except BusinessLogicError as e:
            logger.error(f"产品详情业务逻辑错误: {str(e)}")
            self.write_error_response(str(e), 422, "BUSINESS_LOGIC_ERROR")
        except Exception as e:
            logger.error(f"产品详情处理异常: {str(e)}")
            self.write_error_response("服务器内部错误", 500, "INTERNAL_ERROR")


class CreateProductHandler(BaseProductHandler):
    """创建产品处理器"""
    
    async def post(self):
        """创建产品"""
        try:
            # 解析请求体
            body_data = await self.parse_json_body()
            
            # 验证请求参数
            request_data = CreateProductRequest(**body_data)
            
            # 调用服务创建产品
            result = await self.service.create_product(
                title=request_data.title,
                description=request_data.description,
                price=request_data.price,
                category=request_data.category,
                platform=request_data.platform,
                sku=request_data.sku,
                inventory=request_data.inventory,
                images=request_data.images,
                attributes=request_data.attributes,
                variants=request_data.variants
            )
            
            # 验证响应数据
            response_data = CreateProductResponse(**result)
            
            # 返回响应
            self.write_response(response_data.dict(), 201)
            
        except ValidationError as e:
            logger.warning(f"创建产品请求参数验证失败: {str(e)}")
            self.write_error_response(str(e), 400, "VALIDATION_ERROR")
        except BusinessLogicError as e:
            logger.error(f"创建产品业务逻辑错误: {str(e)}")
            self.write_error_response(str(e), 422, "BUSINESS_LOGIC_ERROR")
        except Exception as e:
            logger.error(f"创建产品处理异常: {str(e)}")
            self.write_error_response("服务器内部错误", 500, "INTERNAL_ERROR")


class UpdateProductHandler(BaseProductHandler):
    """更新产品处理器"""
    
    async def put(self):
        """更新产品"""
        try:
            # 解析请求体
            body_data = await self.parse_json_body()
            
            # 验证请求参数
            request_data = UpdateProductRequest(**body_data)
            
            # 调用服务更新产品
            result = await self.service.update_product(
                product_id=request_data.product_id,
                platform=request_data.platform,
                title=request_data.title,
                description=request_data.description,
                price=request_data.price,
                category=request_data.category,
                sku=request_data.sku,
                inventory=request_data.inventory,
                images=request_data.images,
                attributes=request_data.attributes,
                variants=request_data.variants,
                status=request_data.status
            )
            
            # 验证响应数据
            response_data = UpdateProductResponse(**result)
            
            # 返回响应
            self.write_response(response_data.dict())
            
        except ValidationError as e:
            logger.warning(f"更新产品请求参数验证失败: {str(e)}")
            self.write_error_response(str(e), 400, "VALIDATION_ERROR")
        except NotFoundError as e:
            logger.warning(f"产品未找到: {str(e)}")
            self.write_error_response(str(e), 404, "NOT_FOUND")
        except BusinessLogicError as e:
            logger.error(f"更新产品业务逻辑错误: {str(e)}")
            self.write_error_response(str(e), 422, "BUSINESS_LOGIC_ERROR")
        except Exception as e:
            logger.error(f"更新产品处理异常: {str(e)}")
            self.write_error_response("服务器内部错误", 500, "INTERNAL_ERROR")


class DeleteProductHandler(BaseProductHandler):
    """删除产品处理器"""
    
    async def delete(self):
        """删除产品"""
        try:
            # 解析请求体
            body_data = await self.parse_json_body()
            
            # 验证请求参数
            request_data = DeleteProductRequest(**body_data)
            
            # 调用服务删除产品
            result = await self.service.delete_product(
                product_id=request_data.product_id,
                platform=request_data.platform,
                force_delete=request_data.force_delete
            )
            
            # 验证响应数据
            response_data = DeleteProductResponse(**result)
            
            # 返回响应
            self.write_response(response_data.dict())
            
        except ValidationError as e:
            logger.warning(f"删除产品请求参数验证失败: {str(e)}")
            self.write_error_response(str(e), 400, "VALIDATION_ERROR")
        except NotFoundError as e:
            logger.warning(f"产品未找到: {str(e)}")
            self.write_error_response(str(e), 404, "NOT_FOUND")
        except BusinessLogicError as e:
            logger.error(f"删除产品业务逻辑错误: {str(e)}")
            self.write_error_response(str(e), 422, "BUSINESS_LOGIC_ERROR")
        except Exception as e:
            logger.error(f"删除产品处理异常: {str(e)}")
            self.write_error_response("服务器内部错误", 500, "INTERNAL_ERROR")


class ProductInventoryHandler(BaseProductHandler):
    """产品库存处理器"""
    
    async def get(self):
        """获取产品库存"""
        try:
            # 获取查询参数
            params = self.get_query_params()
            
            # 验证请求参数
            request_data = ProductInventoryRequest(**params)
            
            # 调用服务获取数据
            result = await self.service.get_product_inventory(
                product_id=request_data.product_id,
                platform=request_data.platform,
                warehouse=request_data.warehouse,
                include_reserved=request_data.include_reserved
            )
            
            # 验证响应数据
            response_data = ProductInventoryResponse(**result)
            
            # 返回响应
            self.write_response(response_data.dict())
            
        except ValidationError as e:
            logger.warning(f"产品库存请求参数验证失败: {str(e)}")
            self.write_error_response(str(e), 400, "VALIDATION_ERROR")
        except NotFoundError as e:
            logger.warning(f"产品未找到: {str(e)}")
            self.write_error_response(str(e), 404, "NOT_FOUND")
        except BusinessLogicError as e:
            logger.error(f"产品库存业务逻辑错误: {str(e)}")
            self.write_error_response(str(e), 422, "BUSINESS_LOGIC_ERROR")
        except Exception as e:
            logger.error(f"产品库存处理异常: {str(e)}")
            self.write_error_response("服务器内部错误", 500, "INTERNAL_ERROR")


class BatchProductHandler(BaseProductHandler):
    """批量产品操作处理器"""
    
    async def post(self):
        """批量产品操作"""
        try:
            # 解析请求体
            body_data = await self.parse_json_body()
            
            # 验证请求参数
            request_data = BatchProductRequest(**body_data)
            
            # 调用服务执行批量操作
            result = await self.service.batch_product_operation(
                operation=request_data.operation,
                product_ids=request_data.product_ids,
                platform=request_data.platform,
                operation_data=request_data.operation_data
            )
            
            # 验证响应数据
            response_data = BatchProductResponse(**result)
            
            # 返回响应
            self.write_response(response_data.dict())
            
        except ValidationError as e:
            logger.warning(f"批量产品操作请求参数验证失败: {str(e)}")
            self.write_error_response(str(e), 400, "VALIDATION_ERROR")
        except BusinessLogicError as e:
            logger.error(f"批量产品操作业务逻辑错误: {str(e)}")
            self.write_error_response(str(e), 422, "BUSINESS_LOGIC_ERROR")
        except Exception as e:
            logger.error(f"批量产品操作处理异常: {str(e)}")
            self.write_error_response("服务器内部错误", 500, "INTERNAL_ERROR")