# product_service.py
# 产品相关的业务逻辑服务
from app.auth.openapi import OpenApiBase
from app.config import settings
from typing import Optional, Dict, Any, List
from datetime import datetime
import json as _json

class ProductService:
    """产品服务类 - 处理产品相关的业务逻辑"""
    
    def __init__(self):
        self.api = OpenApiBase(settings.LLX_API_HOST, settings.LLX_APP_ID, settings.LLX_APP_SECRET)

    async def get_local_product_list(self, access_token: str, offset=0, length=1000, 
                                   update_time_start=None, update_time_end=None,
                                   create_time_start=None, create_time_end=None,
                                   sku_list=None, sku_identifier_list=None) -> Dict[str, Any]:
        """
        查询本地产品列表
        支持查询产品列表，对应系统【产品】>【产品管理】数据
        
        Args:
            access_token: 访问令牌
            offset: 分页偏移量，默认0
            length: 分页长度，默认1000
            update_time_start: 更新时间开始，格式：YYYY-MM-DD HH:mm:ss
            update_time_end: 更新时间结束，格式：YYYY-MM-DD HH:mm:ss
            create_time_start: 创建时间开始，格式：YYYY-MM-DD HH:mm:ss
            create_time_end: 创建时间结束，格式：YYYY-MM-DD HH:mm:ss
            sku_list: SKU列表，数组格式
            sku_identifier_list: SKU标识符列表，数组格式
        Returns:
            dict: 产品列表数据
        """
        # 构建请求参数
        query_data = {
            "offset": offset,
            "length": length
        }
        
        # 添加可选参数
        if update_time_start:
            query_data["update_time_start"] = update_time_start
        if update_time_end:
            query_data["update_time_end"] = update_time_end
        if create_time_start:
            query_data["create_time_start"] = create_time_start
        if create_time_end:
            query_data["create_time_end"] = create_time_end
        if sku_list:
            query_data["sku_list"] = sku_list
        if sku_identifier_list:
            query_data["sku_identifier_list"] = sku_identifier_list

        print(f"[RPA_Tornado] 查询本地产品列表 - 请求参数: {query_data}")

        try:
            # 调用API获取本地产品列表
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/data/local_inventory/productList",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            # 保存请求和响应信息用于调试
            compare_info = {
                "access_token": access_token,
                "query_data": query_data,
                "response": resp_data,
                "timestamp": datetime.now().isoformat()
            }

            # 检查API响应状态
            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 本地产品列表查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def add_commodity_code(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建UPC编码
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: 创建结果
        """
        print(f"[RPA_Tornado] 创建UPC编码 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/listing/publish/api/upc/addCommodityCode",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] UPC编码创建成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_upc_list(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取UPC编码列表
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: UPC编码列表数据
        """
        print(f"[RPA_Tornado] 获取UPC编码列表 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/listing/publish/api/upc/upcList",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] UPC编码列表查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_product_info(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询本地产品详情
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: 产品详情数据
        """
        print(f"[RPA_Tornado] 查询本地产品详情 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/data/local_inventory/productInfo",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 本地产品详情查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def batch_get_product_info(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        批量查询本地产品详情
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: 批量产品详情数据
        """
        print(f"[RPA_Tornado] 批量查询本地产品详情 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/data/local_inventory/batchGetProductInfo",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 批量本地产品详情查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def batch_operate_product(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        产品启用、禁用
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: 操作结果
        """
        print(f"[RPA_Tornado] 产品启用/禁用操作 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/basicOpen/product/productManager/product/operate/batch",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品启用/禁用操作成功")
            return resp_data

        except Exception as e:
            raise e

    async def set_product(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加/编辑本地产品
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: 操作结果
        """
        print(f"[RPA_Tornado] 添加/编辑本地产品 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/storage/product/set",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 本地产品添加/编辑成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_attribute_list(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询产品属性列表
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: 产品属性列表数据
        """
        print(f"[RPA_Tornado] 查询产品属性列表 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/storage/attribute/attributeList",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品属性列表查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def set_attribute(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加/编辑产品属性
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: 操作结果
        """
        print(f"[RPA_Tornado] 添加/编辑产品属性 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/storage/attribute/set",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品属性添加/编辑成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_spu_list(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询多属性产品列表
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: 多属性产品列表数据
        """
        print(f"[RPA_Tornado] 查询多属性产品列表 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/storage/spu/spuList",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 多属性产品列表查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_spu_info(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        查询多属性产品详情
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据
        Returns:
            dict: 多属性产品详情数据
        """
        print(f"[RPA_Tornado] 查询多属性产品详情 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/storage/spu/info",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 多属性产品详情查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_bundled_product_list(self, access_token: str, offset=0, length=1000) -> Dict[str, Any]:
        """
        查询捆绑产品关系列表
        
        Args:
            access_token: 访问令牌
            offset: 分页偏移量，默认0
            length: 分页长度，默认1000，上限1000
        Returns:
            dict: 捆绑产品关系列表数据
        """
        query_data = {
            "offset": offset,
            "length": length
        }
        
        print(f"[RPA_Tornado] 查询捆绑产品关系列表 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/data/local_inventory/bundledProductList",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 捆绑产品关系列表查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def set_bundled_product(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加/编辑捆绑产品
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据，包含SKU、产品名称、图片信息、组合商品列表等
        Returns:
            dict: 操作结果
        """
        print(f"[RPA_Tornado] 添加/编辑捆绑产品 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/storage/product/setBundled",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 捆绑产品添加/编辑成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_product_aux_list(self, access_token: str, offset=0, length=1000) -> Dict[str, Any]:
        """
        查询产品辅料列表
        
        Args:
            access_token: 访问令牌
            offset: 分页偏移量，默认0
            length: 分页长度，默认1000，上限1000
        Returns:
            dict: 产品辅料列表数据
        """
        query_data = {
            "offset": offset,
            "length": length
        }
        
        print(f"[RPA_Tornado] 查询产品辅料列表 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/data/local_inventory/productAuxList",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品辅料列表查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def set_aux_product(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加/编辑辅料
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据，包含SKU、产品名称、采购信息、供应商报价等
        Returns:
            dict: 操作结果
        """
        print(f"[RPA_Tornado] 添加/编辑辅料 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/storage/product/setAux",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 辅料添加/编辑成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_brand_list(self, access_token: str, offset=0, length=1000) -> Dict[str, Any]:
        """
        查询产品品牌列表
        支持查询本地产品品牌列表，对应系统【产品】>【品牌管理】数据
        
        Args:
            access_token: 访问令牌
            offset: 分页偏移量，默认0
            length: 分页长度，默认1000，上限1000
        Returns:
            dict: 产品品牌列表数据
        """
        query_data = {
            "offset": offset,
            "length": length
        }
        
        print(f"[RPA_Tornado] 查询产品品牌列表 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/data/local_inventory/brand",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品品牌列表查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def set_brand(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加/编辑产品品牌
        支持添加/编辑本地产品品牌信息
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据，包含品牌信息数组
        Returns:
            dict: 操作结果
        """
        print(f"[RPA_Tornado] 添加/编辑产品品牌 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/storage/brand/set",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品品牌添加/编辑成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_category_list(self, access_token: str, offset=0, length=1000, ids=None) -> Dict[str, Any]:
        """
        查询产品分类列表
        支持查询本地产品的分类列表，对应【产品】>【产品分类】数据
        
        Args:
            access_token: 访问令牌
            offset: 分页偏移量，默认0
            length: 分页长度，默认1000，上限1000
            ids: 分类ID数组，可选
        Returns:
            dict: 产品分类列表数据
        """
        query_data = {
            "offset": offset,
            "length": length
        }
        
        if ids:
            query_data["data"] = {"ids": ids}
        
        print(f"[RPA_Tornado] 查询产品分类列表 - 请求参数: {query_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/data/local_inventory/category",
                method="POST",
                req_body=query_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品分类列表查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def set_category(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        添加/编辑产品分类
        支持添加/编辑本地产品分类
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据，包含分类信息数组
        Returns:
            dict: 操作结果
        """
        print(f"[RPA_Tornado] 添加/编辑产品分类 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/storage/category/set",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品分类添加/编辑成功")
            return resp_data

        except Exception as e:
            raise e

    async def upload_product_pictures(self, access_token: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        上传本地产品图片
        支持本地产品图片上传到领星ERP系统内
        
        Args:
            access_token: 访问令牌
            request_data: 请求数据，包含SKU和图片信息
        Returns:
            dict: 操作结果
        """
        print(f"[RPA_Tornado] 上传本地产品图片 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/erp/sc/routing/storage/product/uploadPictures",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 本地产品图片上传成功")
            return resp_data

        except Exception as e:
            raise e

    async def get_product_label_list(self, access_token: str) -> Dict[str, Any]:
        """
        查询产品标签
        
        Args:
            access_token: 访问令牌
        Returns:
            dict: 产品标签列表数据
        """
        print(f"[RPA_Tornado] 查询产品标签")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/label/operation/v1/label/product/list",
                method="GET",
                req_body={}
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品标签查询成功")
            return resp_data

        except Exception as e:
            raise e

    async def create_product_label(self, access_token: str, label: str) -> Dict[str, Any]:
        """
        创建产品标签
        
        Args:
            access_token: 访问令牌
            label: 标签名称，最长15个字符，中间不能有空格
        Returns:
            dict: 创建结果，包含标签ID和标签名称
        """
        request_data = {
            "label": label
        }
        
        print(f"[RPA_Tornado] 创建产品标签 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/label/operation/v1/label/product/create",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品标签创建成功 - 标签ID: {resp_data.get('data', {}).get('label_id')}")
            return resp_data

        except Exception as e:
            raise e

    async def mark_product_label(self, access_token: str, operation_type: int, detail_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        标记产品标签
        
        Args:
            access_token: 访问令牌
            operation_type: 操作类型：1 追加，2 覆盖
            detail_list: 标签信息列表，上限200个
                - sku: 产品SKU
                - label_list: 标签名称列表，上限10个
        Returns:
            dict: 操作结果
        """
        request_data = {
            "type": operation_type,
            "detail_list": detail_list
        }
        
        print(f"[RPA_Tornado] 标记产品标签 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/label/operation/v1/label/product/mark",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品标签标记成功")
            return resp_data

        except Exception as e:
            raise e

    async def unmark_product_label(self, access_token: str, operation_type: int, detail_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        删除产品标签
        
        Args:
            access_token: 访问令牌
            operation_type: 操作类型：
                1 删除SKU指定的标签
                2 删除SKU全部的标签（此类型下对应sku的label_list为空数组即可）
            detail_list: 标签信息列表，上限200个
                - sku: 本地产品SKU
                - label_list: 标签名称列表，上限10个
        Returns:
            dict: 操作结果
        """
        request_data = {
            "type": operation_type,
            "detail_list": detail_list
        }
        
        print(f"[RPA_Tornado] 删除产品标签 - 请求参数: {request_data}")

        try:
            resp = await self.api.request(
                access_token=access_token,
                route_name="/label/operation/v1/label/product/unmarkLabel",
                method="POST",
                req_body=request_data
            )
            resp_data = resp.model_dump()

            if resp_data.get("code") != 0:
                raise Exception(f"API Error: code={resp_data.get('code')}, msg={resp_data.get('message')}")

            print(f"[RPA_Tornado] 产品标签删除成功")
            return resp_data

        except Exception as e:
            raise e