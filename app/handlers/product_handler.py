import json
from tornado.web import RequestHandler
from app.services.product_service import ProductService
from .base import BaseHandler

# 查询本地产品列表
class LocalProductListHandler(BaseHandler):
    async def post(self):
        """
        查询本地产品列表，支持查询产品列表，对应系统【产品】>【产品管理】数据
        
        API Path: /erp/sc/routing/data/local_inventory/productList
        请求方式: POST
        
        请求参数:
        - offset: 分页偏移量，默认0
        - length: 分页长度，默认1000
        - update_time_start: 更新时间开始，格式：YYYY-MM-DD HH:mm:ss
        - update_time_end: 更新时间结束，格式：YYYY-MM-DD HH:mm:ss
        - create_time_start: 创建时间开始，格式：YYYY-MM-DD HH:mm:ss
        - create_time_end: 创建时间结束，格式：YYYY-MM-DD HH:mm:ss
        - sku_list: SKU列表，数组格式
        - sku_identifier_list: SKU标识符列表，数组格式
        """
        try:
            # 处理空请求体的情况
            body = self.request.body.decode('utf-8').strip()
            if body:
                data = json.loads(body)
            else:
                data = {}
            
            # 获取请求参数
            offset = data.get('offset', 0)
            length = data.get('length', 1000)
            update_time_start = data.get('update_time_start')
            update_time_end = data.get('update_time_end')
            create_time_start = data.get('create_time_start')
            create_time_end = data.get('create_time_end')
            sku_list = data.get('sku_list')
            sku_identifier_list = data.get('sku_identifier_list')
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_local_product_list(
                self.access_token,
                offset=offset,
                length=length,
                update_time_start=update_time_start,
                update_time_end=update_time_end,
                create_time_start=create_time_start,
                create_time_end=create_time_end,
                sku_list=sku_list,
                sku_identifier_list=sku_identifier_list
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 查询捆绑产品关系列表
class BundledProductListHandler(BaseHandler):
    async def post(self):
        """
        查询捆绑产品关系列表
        
        API Path: /erp/sc/routing/data/local_inventory/bundledProductList
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - offset: 分页偏移量，默认0
        - length: 分页长度，默认1000，上限1000
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if body:
                data = json.loads(body)
            else:
                data = {}
            
            # 获取请求参数
            offset = data.get('offset', 0)
            length = data.get('length', 1000)
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_bundled_product_list(
                self.access_token,
                offset=offset,
                length=length
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 添加/编辑捆绑产品
class SetBundledProductHandler(BaseHandler):
    async def post(self):
        """
        添加/编辑捆绑产品
        
        API Path: /erp/sc/routing/storage/product/setBundled
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - sku: SKU（添加时必填）
        - product_name: 品名（添加时必填）
        - picture_list: 产品图片信息（可选）
        - model: 型号（可选）
        - unit: 单位（可选）
        - status: 状态（可选）
        - category_id: 分类id（可选）
        - category: 分类（可选）
        - brand_id: 品牌id（可选）
        - brand: 品牌（可选）
        - product_developer: 开发者名称（可选）
        - product_developer_uid: 开发者id（可选）
        - product_duty_uids: 负责人id（可选）
        - is_append_product_duty: 负责人是否追加创建人（可选）
        - product_creator_uid: 创建人ERP id（可选）
        - description: 商品描述（可选）
        - group_list: 组合商品列表（可选）
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            sku = data.get('sku')
            product_name = data.get('product_name')
            
            if not sku:
                self.set_status(400)
                self.write({'error': 'sku 参数不能为空'})
                return
                
            if not product_name:
                self.set_status(400)
                self.write({'error': 'product_name 参数不能为空'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.set_bundled_product(self.access_token, data)
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 查询产品辅料列表
class ProductAuxListHandler(BaseHandler):
    async def post(self):
        """
        查询产品辅料列表
        
        API Path: /erp/sc/routing/data/local_inventory/productAuxList
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - offset: 分页偏移量，默认0
        - length: 分页长度，默认1000，上限1000
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if body:
                data = json.loads(body)
            else:
                data = {}
            
            # 获取请求参数
            offset = data.get('offset', 0)
            length = data.get('length', 1000)
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_product_aux_list(
                self.access_token,
                offset=offset,
                length=length
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 添加/编辑辅料
class SetAuxProductHandler(BaseHandler):
    async def post(self):
        """
        添加/编辑辅料
        
        API Path: /erp/sc/routing/storage/product/setAux
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - sku: SKU（必填）
        - product_name: 品名（必填）
        - cg_price: 采购成本（可选）
        - cg_product_length: 单品规格-长（可选）
        - cg_product_width: 单品规格-宽（可选）
        - cg_product_height: 单品规格-高（可选）
        - cg_product_net_weight: 单品净重（可选）
        - supplier_quote: 供应商报价信息（可选）
        - remark: 辅料描述（必填）
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            sku = data.get('sku')
            product_name = data.get('product_name')
            remark = data.get('remark')
            
            if not sku:
                self.set_status(400)
                self.write({'error': 'sku 参数不能为空'})
                return
                
            if not product_name:
                self.set_status(400)
                self.write({'error': 'product_name 参数不能为空'})
                return
                
            if not remark:
                self.set_status(400)
                self.write({'error': 'remark 参数不能为空'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.set_aux_product(self.access_token, data)
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 查询产品品牌列表
class BrandListHandler(BaseHandler):
    async def post(self):
        """
        查询产品品牌列表
        支持查询本地产品品牌列表，对应系统【产品】>【品牌管理】数据
        
        API Path: /erp/sc/data/local_inventory/brand
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - offset: 分页偏移量，默认0
        - length: 分页长度，默认1000，上限1000
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if body:
                data = json.loads(body)
            else:
                data = {}
            
            # 获取请求参数
            offset = data.get('offset', 0)
            length = data.get('length', 1000)
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_brand_list(
                self.access_token,
                offset=offset,
                length=length
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 添加/编辑产品品牌
class SetBrandHandler(BaseHandler):
    async def post(self):
        """
        添加/编辑产品品牌
        支持添加/编辑本地产品品牌信息
        
        API Path: /erp/sc/storage/brand/set
        请求方式: POST
        令牌桶容量: 10
        
        请求参数:
        - data: 请求数据（必填）
          - id: 品牌id（可选，为空时表新增，不为空时表编辑）
          - title: 品牌名称（必填）
          - brand_code: 品牌简码（可选）
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            brand_data = data.get('data')
            
            if not brand_data:
                self.set_status(400)
                self.write({'error': 'data 参数不能为空'})
                return
                
            # 验证数组中每个元素的必填字段
            if isinstance(brand_data, list):
                for item in brand_data:
                    if not item.get('title'):
                        self.set_status(400)
                        self.write({'error': '品牌名称 title 不能为空'})
                        return
            else:
                self.set_status(400)
                self.write({'error': 'data 参数必须是数组格式'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.set_brand(self.access_token, data)
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 查询产品分类列表
class CategoryListHandler(BaseHandler):
    async def post(self):
        """
        查询产品分类列表
        支持查询本地产品的分类列表，对应【产品】>【产品分类】数据
        
        API Path: /erp/sc/routing/data/local_inventory/category
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - offset: 分页偏移量，默认0
        - length: 分页长度，默认1000，上限1000
        - data: 请求数据（可选）
          - ids: 分类ID数组（可选）
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if body:
                data = json.loads(body)
            else:
                data = {}
            
            # 获取请求参数
            offset = data.get('offset', 0)
            length = data.get('length', 1000)
            ids = None
            
            # 检查是否有分类ID过滤
            if 'data' in data and 'ids' in data['data']:
                ids = data['data']['ids']
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_category_list(
                self.access_token,
                offset=offset,
                length=length,
                ids=ids
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 添加/编辑产品分类
class SetCategoryHandler(BaseHandler):
    async def post(self):
        """
        添加/编辑产品分类
        支持添加/编辑本地产品分类
        
        API Path: /erp/sc/routing/storage/category/set
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - data: 请求数据（必填）
          - id: 分类id（可选，为空时新增，不为空时编辑）
          - parent_cid: 父级分类id（可选）
          - title: 分类名称（必填）
          - category_code: 分类简码（必填）
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            category_data = data.get('data')
            
            if not category_data:
                self.set_status(400)
                self.write({'error': 'data 参数不能为空'})
                return
                
            # 验证数组中每个元素的必填字段
            if isinstance(category_data, list):
                for item in category_data:
                    if not item.get('title'):
                        self.set_status(400)
                        self.write({'error': '分类名称 title 不能为空'})
                        return
                    if not item.get('category_code'):
                        self.set_status(400)
                        self.write({'error': '分类简码 category_code 不能为空'})
                        return
            else:
                self.set_status(400)
                self.write({'error': 'data 参数必须是数组格式'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.set_category(self.access_token, data)
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 上传本地产品图片
class UploadProductPicturesHandler(BaseHandler):
    async def post(self):
        """
        上传本地产品图片
        支持本地产品图片上传到领星ERP系统内
        
        API Path: /erp/sc/routing/storage/product/uploadPictures
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - sku: 本地产品SKU（必填）
        - picture_list: 产品图片信息（必填）
          - pic_url: 产品图片链接（必填）
          - is_primary: 是否产品主图：0 否，1 是（必填）
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            sku = data.get('sku')
            picture_list = data.get('picture_list')
            
            if not sku:
                self.set_status(400)
                self.write({'error': 'sku 参数不能为空'})
                return
                
            if not picture_list:
                self.set_status(400)
                self.write({'error': 'picture_list 参数不能为空'})
                return
                
            # 验证图片列表格式
            if isinstance(picture_list, list):
                for pic in picture_list:
                    if not pic.get('pic_url'):
                        self.set_status(400)
                        self.write({'error': '图片链接 pic_url 不能为空'})
                        return
                    if pic.get('is_primary') is None:
                        self.set_status(400)
                        self.write({'error': '是否主图 is_primary 不能为空'})
                        return
            else:
                self.set_status(400)
                self.write({'error': 'picture_list 参数必须是数组格式'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.upload_product_pictures(self.access_token, data)
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 查询产品标签
class ProductLabelListHandler(BaseHandler):
    async def get(self):
        """
        查询产品标签
        
        API Path: /label/operation/v1/label/product/list
        请求方式: GET
        令牌桶容量: 10
        
        返回结果:
        - code: 状态码，0 成功
        - message: 返回信息
        - request_id: 请求链路id
        - response_time: 响应时间
        - data: 响应数据
          - list: 列表数据
            - label_id: 标签id
            - label_name: 标签名称
            - gmt_created: 创建时间
          - total: 总数
        """
        try:
            # 调用产品服务
            service = ProductService()
            result = await service.get_product_label_list(self.access_token)
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 创建UPC编码
class UpcAddCommodityCodeHandler(BaseHandler):
    async def post(self):
        """
        创建UPC编码
        
        API Path: /listing/publish/api/upc/addCommodityCode
        请求方式: POST
        令牌桶容量: 10
        
        请求参数:
        - commodity_codes: 编码-最多支持两百个，数组格式
        - code_type: 编码类型：支持UPC、EAN、ISBN
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            commodity_codes = data.get('commodity_codes')
            code_type = data.get('code_type')
            
            if not commodity_codes:
                self.set_status(400)
                self.write({'error': 'commodity_codes 参数不能为空'})
                return
                
            if not code_type:
                self.set_status(400)
                self.write({'error': 'code_type 参数不能为空'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.add_commodity_code(
                self.access_token,
                commodity_codes=commodity_codes,
                code_type=code_type
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 获取UPC编码列表
class UpcListHandler(BaseHandler):
    async def post(self):
        """
        获取UPC编码列表
        
        API Path: /listing/publish/api/upc/upcList
        请求方式: POST
        令牌桶容量: 10
        
        请求参数:
        - offset: 分页偏移量，默认0
        - length: 分页长度，默认20
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if body:
                data = json.loads(body)
            else:
                data = {}
            
            # 获取请求参数
            offset = data.get('offset', 0)
            length = data.get('length', 20)
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_upc_list(
                self.access_token,
                offset=offset,
                length=length
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 查询本地产品详情
class LocalProductInfoHandler(BaseHandler):
    async def post(self):
        """
        查询本地产品详情
        支持查询本地产品详细信息，对应系统【产品】>【产品管理】数据
        
        API Path: /erp/sc/routing/data/local_inventory/productInfo
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - id: 产品id【产品id、产品SKU、SKU识别码 三选一必填】
        - sku: 产品SKU【产品id、产品SKU、SKU识别码 三选一必填】
        - sku_identifier: SKU识别码【产品id、产品SKU、SKU识别码 三选一必填】
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 获取请求参数
            product_id = data.get('id')
            sku = data.get('sku')
            sku_identifier = data.get('sku_identifier')
            
            # 验证至少有一个参数
            if not any([product_id, sku, sku_identifier]):
                self.set_status(400)
                self.write({'error': '产品id、产品SKU、SKU识别码 三选一必填'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_local_product_info(
                self.access_token,
                product_id=product_id,
                sku=sku,
                sku_identifier=sku_identifier
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 批量查询本地产品详情
class BatchGetProductInfoHandler(BaseHandler):
    async def post(self):
        """
        批量查询本地产品详情
        
        API Path: /erp/sc/routing/data/local_inventory/batchGetProductInfo
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - productIds: 产品id，上限100个【产品id、产品sku、SKU识别码 三选一必填】
        - skus: 产品SKU，上限100个【产品id、产品sku、SKU识别码 三选一必填】
        - sku_identifiers: SKU识别码，上限100个【产品id、产品sku、SKU识别码 三选一必填】
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 获取请求参数
            product_ids = data.get('productIds')
            skus = data.get('skus')
            sku_identifiers = data.get('sku_identifiers')
            
            # 验证至少有一个参数
            if not any([product_ids, skus, sku_identifiers]):
                self.set_status(400)
                self.write({'error': '产品id、产品sku、SKU识别码 三选一必填'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.batch_get_product_info(
                self.access_token,
                product_ids=product_ids,
                skus=skus,
                sku_identifiers=sku_identifiers
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 产品启用、禁用
class ProductOperateBatchHandler(BaseHandler):
    async def post(self):
        """
        产品启用、禁用
        
        API Path: /basicOpen/product/productManager/product/operate/batch
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - product_ids: 产品id数组
        - batch_status: 状态: Enable 启用, Disable 禁用
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            product_ids = data.get('product_ids')
            batch_status = data.get('batch_status')
            
            if not product_ids:
                self.set_status(400)
                self.write({'error': 'product_ids 参数不能为空'})
                return
                
            if not batch_status:
                self.set_status(400)
                self.write({'error': 'batch_status 参数不能为空'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.product_operate_batch(
                self.access_token,
                product_ids=product_ids,
                batch_status=batch_status
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 添加/编辑本地产品
class ProductSetHandler(BaseHandler):
    async def post(self):
        """
        添加/编辑本地产品
        支持添加/编辑系统本地产品信息
        
        API Path: /erp/sc/routing/storage/product/set
        请求方式: POST
        令牌桶容量: 10
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 调用产品服务
            service = ProductService()
            result = await service.set_product(self.access_token, data)
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 查询产品属性列表
class AttributeListHandler(BaseHandler):
    async def post(self):
        """
        查询产品属性列表
        
        API Path: /erp/sc/routing/storage/attribute/attributeList
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - offset: 分页偏移量
        - length: 分页长度，上限200
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            offset = data.get('offset')
            length = data.get('length')
            
            if offset is None:
                self.set_status(400)
                self.write({'error': 'offset 参数不能为空'})
                return
                
            if length is None:
                self.set_status(400)
                self.write({'error': 'length 参数不能为空'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_attribute_list(
                self.access_token,
                offset=offset,
                length=length
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 添加/编辑产品属性
class AttributeSetHandler(BaseHandler):
    async def post(self):
        """
        添加/编辑产品属性
        
        API Path: /erp/sc/routing/storage/attribute/set
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - pa_id: 领星属性id（可选）
        - attr_name: 属性名
        - attr_values: 属性值数组
          - pai_id: 领星属性值id（可选）
          - attr_value: 属性值名称
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            attr_name = data.get('attr_name')
            attr_values = data.get('attr_values')
            
            if not attr_name:
                self.set_status(400)
                self.write({'error': 'attr_name 参数不能为空'})
                return
                
            if not attr_values:
                self.set_status(400)
                self.write({'error': 'attr_values 参数不能为空'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.set_attribute(self.access_token, data)
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 查询多属性产品列表
class SpuListHandler(BaseHandler):
    async def post(self):
        """
        查询多属性产品列表
        
        API Path: /erp/sc/routing/storage/spu/spuList
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - offset: 分页偏移量
        - length: 分页长度，上限200
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            offset = data.get('offset')
            length = data.get('length')
            
            if offset is None:
                self.set_status(400)
                self.write({'error': 'offset 参数不能为空'})
                return
                
            if length is None:
                self.set_status(400)
                self.write({'error': 'length 参数不能为空'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_spu_list(
                self.access_token,
                offset=offset,
                length=length
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 查询多属性产品详情
class SpuInfoHandler(BaseHandler):
    async def post(self):
        """
        查询多属性产品详情
        
        API Path: /erp/sc/routing/storage/spu/info
        请求方式: POST
        令牌桶容量: 1
        
        请求参数:
        - ps_id: SPU唯一id【ps_id 与 spu二选一必填】
        - spu: SPU【ps_id 与 spu二选一必填】
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 获取请求参数
            ps_id = data.get('ps_id')
            spu = data.get('spu')
            
            # 验证至少有一个参数
            if not any([ps_id, spu]):
                self.set_status(400)
                self.write({'error': 'ps_id 与 spu 二选一必填'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.get_spu_info(
                self.access_token,
                ps_id=ps_id,
                spu=spu
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 创建产品标签
class CreateProductLabelHandler(BaseHandler):
    async def post(self):
        """
        创建产品标签
        
        API Path: /label/operation/v1/label/product/create
        请求方式: POST
        令牌桶容量: 10
        
        请求参数:
        - label: 标签名称，最长15个字符，中间不能有空格
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            label = data.get('label')
            
            if not label:
                self.set_status(400)
                self.write({'error': 'label 参数不能为空'})
                return
            
            # 验证标签名称长度和格式
            if len(label) > 15:
                self.set_status(400)
                self.write({'error': '标签名称最长15个字符'})
                return
                
            if ' ' in label:
                self.set_status(400)
                self.write({'error': '标签名称中间不能有空格'})
                return
            
            # 调用产品服务
            service = ProductService()
            result = await service.create_product_label(self.access_token, label)
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 标记产品标签
class MarkProductLabelHandler(BaseHandler):
    async def post(self):
        """
        标记产品标签
        
        API Path: /label/operation/v1/label/product/mark
        请求方式: POST
        令牌桶容量: 10
        
        请求参数:
        - type: 操作类型：1 追加，2 覆盖
        - detail_list: 标签信息，上限200
          - sku: 产品SKU
          - label_list: 标签名称，上限10
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            operation_type = data.get('type')
            detail_list = data.get('detail_list')
            
            if operation_type is None:
                self.set_status(400)
                self.write({'error': 'type 参数不能为空'})
                return
                
            if not detail_list:
                self.set_status(400)
                self.write({'error': 'detail_list 参数不能为空'})
                return
            
            # 验证操作类型
            if operation_type not in [1, 2]:
                self.set_status(400)
                self.write({'error': 'type 参数必须为 1（追加）或 2（覆盖）'})
                return
            
            # 验证detail_list长度
            if len(detail_list) > 200:
                self.set_status(400)
                self.write({'error': 'detail_list 上限200个'})
                return
            
            # 验证detail_list中的每个项目
            for item in detail_list:
                if not item.get('sku'):
                    self.set_status(400)
                    self.write({'error': 'detail_list中每个项目的sku不能为空'})
                    return
                    
                label_list = item.get('label_list', [])
                if len(label_list) > 10:
                    self.set_status(400)
                    self.write({'error': 'label_list 上限10个'})
                    return
            
            # 调用产品服务
            service = ProductService()
            result = await service.mark_product_label(
                self.access_token, 
                operation_type, 
                detail_list
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})


# 删除产品标签
class UnmarkProductLabelHandler(BaseHandler):
    async def post(self):
        """
        删除产品标签
        
        API Path: /label/operation/v1/label/product/unmarkLabel
        请求方式: POST
        令牌桶容量: 10
        
        请求参数:
        - type: 操作类型：
          1 删除SKU指定的标签
          2 删除SKU全部的标签【此类型下对应sku的label_list为空数组即可】
        - detail_list: 标签信息，上限200
          - sku: 本地产品sku
          - label_list: 标签名称，上限10
        """
        try:
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空'})
                return
                
            data = json.loads(body)
            
            # 验证必填参数
            operation_type = data.get('type')
            detail_list = data.get('detail_list')
            
            if operation_type is None:
                self.set_status(400)
                self.write({'error': 'type 参数不能为空'})
                return
                
            if not detail_list:
                self.set_status(400)
                self.write({'error': 'detail_list 参数不能为空'})
                return
            
            # 验证操作类型
            if operation_type not in [1, 2]:
                self.set_status(400)
                self.write({'error': 'type 参数必须为 1（删除指定标签）或 2（删除全部标签）'})
                return
            
            # 验证detail_list长度
            if len(detail_list) > 200:
                self.set_status(400)
                self.write({'error': 'detail_list 上限200个'})
                return
            
            # 验证detail_list中的每个项目
            for item in detail_list:
                if not item.get('sku'):
                    self.set_status(400)
                    self.write({'error': 'detail_list中每个项目的sku不能为空'})
                    return
                    
                label_list = item.get('label_list', [])
                if len(label_list) > 10:
                    self.set_status(400)
                    self.write({'error': 'label_list 上限10个'})
                    return
            
            # 调用产品服务
            service = ProductService()
            result = await service.unmark_product_label(
                self.access_token, 
                operation_type, 
                detail_list
            )
            
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
            
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})
