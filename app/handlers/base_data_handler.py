import json
from tornado.web import RequestHandler
from app.services.base_data_service import BaseDataService
from .base import BaseHandler

# 汇率查询接口
class CurrencyExchangeRateHandler(BaseHandler):
    async def get(self):
        """
        查询汇率，支持传递 date 参数（格式 YYYY-MM），不传则默认昨天所在月份。
        """
        try:
            date = self.get_argument('date', None)
            service = BaseDataService()
            result = await service.get_currency_exchange_rate(self.access_token, date=date)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

    async def post(self):
        """
        查询汇率，支持传递 date 参数（格式 YYYY-MM），不传则默认昨天所在月份。
        """
        try:
            # 处理空请求体的情况
            body = self.request.body.decode('utf-8').strip()
            if body:
                data = json.loads(body)
                date = data.get('date', None)
            else:
                date = None
            
            service = BaseDataService()
            result = await service.get_currency_exchange_rate(self.access_token, date=date)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

# 查询亚马逊店铺列表
class AmazonSellerListHandler(BaseHandler):
    async def get(self):
        """
        查询企业已授权到领星ERP的全部亚马逊店铺信息。
        """
        try:
            print("[DEBUG] AmazonSellerListHandler: 开始调用 service")
            service = BaseDataService()
            print("[DEBUG] AmazonSellerListHandler: 创建 service 实例成功")
            result = await service.get_amazon_seller_list(self.access_token)
            print("[DEBUG] AmazonSellerListHandler: service 调用完成")
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            print(f"[DEBUG] AmazonSellerListHandler: 发生异常: {str(e)}")
            self.set_status(500)
            self.write({'error': str(e)})

# 查询亚马逊市场列表
class AmazonMarketplaceListHandler(BaseHandler):
    async def get(self):
        """
        查询亚马逊所有市场列表数据。
        """
        try:
            service = BaseDataService()
            result = await service.get_amazon_marketplace_list(self.access_token)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

# 查询世界州/省列表
class WorldStateListHandler(BaseHandler):
    async def post(self):
        """
        根据国家 code 查询对应的州/省列表，参数 country_code 必填。
        """
        try:
            # 处理空请求体的情况
            body = self.request.body.decode('utf-8').strip()
            if not body:
                self.set_status(400)
                self.write({'error': '请求体不能为空，需要提供 country_code 参数'})
                return
            
            data = json.loads(body)
            country_code = data.get('country_code')
            
            if not country_code:
                self.set_status(400)
                self.write({'error': 'country_code 参数不能为空'})
                return
            
            service = BaseDataService()
            result = await service.get_world_state_list(self.access_token, country_code=country_code)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except json.JSONDecodeError as e:
            self.set_status(400)
            self.write({'error': f'JSON 格式错误: {str(e)}'})
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

# 下载产品附件
class FileAttachmentDownloadHandler(BaseHandler):
    async def post(self):
        """
        下载产品附件，参数 file_id 必填。
        """
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            file_id = data.get('file_id')
            service = BaseDataService()
            result = await service.download_file_attachment(self.access_token, file_id=file_id)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

# 定制化附件下载
class CustomizedFileDownloadHandler(BaseHandler):
    async def post(self):
        """
        定制化附件下载，参数 file_id 必填。
        """
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            file_id = data.get('file_id')
            service = BaseDataService()
            result = await service.download_customized_file(self.access_token, file_id=file_id)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

# 查询ERP用户信息列表
class ErpUserListHandler(BaseHandler):
    async def get(self):
        """
        查询企业开启的全部ERP账号数据。
        """
        try:
            service = BaseDataService()
            result = await service.get_erp_user_list()
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)})

# 批量修改店铺名称
class BatchEditSellerNameHandler(BaseHandler):
    async def post(self):
        """
        批量修改店铺名称，参数 sid_name_list 必填，为包含 sid 和 name 的字典数组。
        """
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            sid_name_list = data.get('sid_name_list')
            service = BaseDataService()
            result = await service.batch_edit_seller_name(self.access_token, sid_name_list=sid_name_list)
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(result, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.write({'error': str(e)}) 