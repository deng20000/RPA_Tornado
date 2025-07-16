from tornado.web import RequestHandler
from app.ecommerce_dashboard.services.stat_service import SalesService
import tornado.escape
from app.utils.time_utils import parse_time
from datetime import datetime, timedelta
import os
import json
from app.utils.log_utils import log_exception
from app.utils.currency_utils import get_exchange_rate
from collections import OrderedDict

# 指定顺序
STORE_ORDER = [
    'GL Tech', 'GL-iNet Overseas Store Store', 'GL.iNet_AU-AU', 'GL.iNet_EU&UK-BE', 'GL.iNet_EU&UK-DE', 'GL.iNet_EU&UK-ES', 'GL.iNet_EU&UK-FR', 'GL.iNet_EU&UK-IE', 'GL.iNet_EU&UK-IT', 'GL.iNet_EU&UK-NL', 'GL.iNet_EU&UK-PL', 'GL.iNet_EU&UK-SE', 'GL.iNet_EU&UK-UK', 'GL.iNet_JP-JP', 'GL.iNet_NA-CA', 'GL.iNet_NA-MX', 'GL.iNet_NA-US', 'MIC-DE-BE', 'MIC-DE-DE', 'MIC-DE-ES', 'MIC-DE-FR', 'MIC-DE-IT', 'MIC-DE-NL', 'MIC-DE-PL', 'MIC-DE-SE', 'MIC-DE-UK', 'MIC-US-CA', 'MIC-US-MX', 'MIC-US-US', 'VIXMINI-US', 'GL Tech MY', 'GL Tech PH', 'GL Tech SG', 'GL Tech TH', 'GL.iNet CA', 'GL.iNet EU', 'GL.iNet UK', 'GL.iNet US', 'gl-inet', 'Lafaer', 'TEMU-US', 'GL-iNetUS', 'GL Tech', 'Price.com', '香港合作零售商', 'Walk in'
]

def clean_sale_stat_3():
    """
    清洗 unprocessed_data 下最新 sale_stat_3 文件，提取所有店铺昨天日期及其 value。
    返回格式：[{店铺名: [日期, 值]}, ...]
    支持 date_collect 为 dict 或 list。
    """
    try:
        files = [f for f in os.listdir('unprocessed_data') if f.startswith('sale_stat_3_') and f.endswith('.json')]
        if not files:
            return {"error": "未找到 sale_stat_3 文件"}
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join('unprocessed_data', x)))
        file_path = os.path.join('unprocessed_data', latest_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
        except Exception as e:
            log_exception(e)
            return {"error": f"文件读取或解析失败: {file_path}, {e}"}
        # 校验结构
        data = raw.get('data')
        if not isinstance(data, dict):
            return {"error": "data 字段缺失或格式错误"}
        data_list = data.get('data')
        if not isinstance(data_list, list) or not data_list:
            return {"error": "data.data 字段缺失或为空"}
        # 昨天日期
        yesterday = (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d')
        result = {}
        for item in data_list:
            if not isinstance(item, dict):
                continue
            store_name = item.get('store_name')
            # 兼容 store_name 为 list 或 str
            if isinstance(store_name, list):
                store_name = store_name[0] if store_name else None
            if not store_name or not isinstance(store_name, str):
                continue
            date_collect = item.get('date_collect')
            value = None
            if isinstance(date_collect, dict):
                value = date_collect.get(yesterday)
            elif isinstance(date_collect, list):
                for d in date_collect:
                    if isinstance(d, dict) and d.get('date') == yesterday:
                        value = d.get('value')
                        break
            currency_code = item.get('currency_code', 'CNY')
            if value is not None:
                result[store_name] = [yesterday, value, currency_code]
        # 保存到 processed_data
        try:
            os.makedirs('processed_data', exist_ok=True)
            out_file = f"processed_data/cleaned_sale_stat_3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            # 写入 ordered_result，保证顺序
            ordered_result = OrderedDict()
            for store in STORE_ORDER:
                if store in result and isinstance(result[store], list) and len(result[store]) == 3:
                    ordered_result[store] = result[store]
                else:
                    ordered_result[store] = [yesterday, None, None]
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(ordered_result, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log_exception(e)
            # 只记录日志，不影响主流程
        return ordered_result
    except Exception as e:
        log_exception(e)
        return {"error": f"clean_sale_stat_3 处理异常: {e}"}

def process_to_usd_cleaned_sale_stat_3(cleaned_file_path, api_key, workers=10):
    """
    读取cleaned_sale_stat_3文件（dict结构），并发调用currency_utils.py进行货币转换，生成fin_cleaned_sale_stat_3_时间.json。
    """
    import time
    from concurrent.futures import ThreadPoolExecutor, as_completed
    try:
        with open(cleaned_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict) or not data:
            return {"error": "cleaned_sale_stat_3 文件内容格式错误"}
        fin_result = {}
        tasks = {}
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for store, values in data.items():
                if len(values) < 3:
                    continue
                date, value, from_currency = values[0], values[1], values[2]
                to_currency = 'USD'
                # 新增：如果 value、date、from_currency 有 None，直接补空
                if value is None or date is None or from_currency is None:
                    fin_result[store] = [date if date is not None else (datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d'), None, to_currency]
                    continue
                if from_currency == 'USD':
                    try:
                        usd_value = round(float(value), 2)
                    except Exception:
                        usd_value = None
                    if usd_value is not None:
                        fin_result[store] = [date, usd_value, to_currency]
                    else:
                        fin_result[store] = [date, None, to_currency]
                    continue
                # 提交汇率转换任务
                tasks[executor.submit(get_exchange_rate, from_currency, to_currency, date, date, api_key)] = (store, date, value, from_currency)
            for future in as_completed(tasks):
                store, date, value, from_currency = tasks[future]
                to_currency = 'USD'
                try:
                    rates = future.result()
                    rate = None
                    # 兼容 fastforex 新接口结构
                    if 'results' in rates and to_currency in rates['results'] and date in rates['results'][to_currency]:
                        rate = rates['results'][to_currency][date]
                    elif 'result' in rates and date in rates['result'] and to_currency in rates['result'][date]:
                        rate = rates['result'][date][to_currency]
                    if not rate:
                        continue
                    usd_value = round(float(value) * rate, 2)
                    fin_result[store] = [date, usd_value, to_currency]
                except Exception as e:
                    from app.utils.log_utils import log_exception
                    log_exception(e)
                    continue
        # 保存新文件
        out_file = f"processed_data/fin_cleaned_sale_stat_3_{time.strftime('%Y%m%d_%H%M%S')}.json"
        # 写入 ordered_fin_result，保证顺序
        ordered_fin_result = OrderedDict()
        for store in STORE_ORDER:
            if store in fin_result and isinstance(fin_result[store], list) and len(fin_result[store]) == 3:
                ordered_fin_result[store] = fin_result[store]
            else:
                # 这里也补昨天日期
                ordered_fin_result[store] = [(datetime.now().date() - timedelta(days=1)).strftime('%Y-%m-%d'), None, 'USD']
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(ordered_fin_result, f, ensure_ascii=False, indent=2)
        return {"file": out_file, "count": len(ordered_fin_result)}
    except Exception as e:
        from app.utils.log_utils import log_exception
        log_exception(e)
        return {"error": f"process_to_usd_cleaned_sale_stat_3 处理异常: {e}"}

class SaleStatHandler(RequestHandler):
    async def post(self):
        try:
            body = self.request.body.decode('utf-8')
            params = tornado.escape.json_decode(body) if body else {}
        except Exception as e:
            self.set_status(400)
            self.write({"code": 1, "msg": f"JSON解析失败: {e}"})
            return
        # 参数默认值
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        start_date = params.get("start_date") or yesterday.strftime("%Y-%m-%d")
        end_date = params.get("end_date") or today.strftime("%Y-%m-%d")
        page = int(params.get("page", 1))
        length = int(params.get("length", 20))
        result_type = params.get("result_type")
        # 组装参数
        query_params = {
            **params,
            "start_date": start_date,
            "end_date": end_date,
            "page": page,
            "length": length
        }
        try:
            if result_type == 3:
                print("[DEBUG] Tornado handler params:", params)
                data = await SalesService().get_daily_sales(query_params)
                output = {"code": 0, "msg": "success", "result_type": 3, "data": data}
                # 保存原始数据
                os.makedirs('unprocessed_data', exist_ok=True)
                filename = f"unprocessed_data/sale_stat_3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(output, f, ensure_ascii=False, indent=2)
                # 触发清洗
                cleaned = clean_sale_stat_3()
                # 自动生成 fin_cleaned 文件（不覆盖 cleaned 文件）
                cleaned_file_path = None
                processed_dir = 'processed_data'
                cleaned_files = [f for f in os.listdir(processed_dir) if f.startswith('cleaned_sale_stat_3_') and f.endswith('.json')]
                if cleaned_files:
                    cleaned_file_path = os.path.join(processed_dir, sorted(cleaned_files, reverse=True)[0])
                fin_result = None
                if cleaned_file_path:
                    api_key = params.get('api_key', '72605c5da4-7bd3977080-szgx30')
                    print("[DEBUG] process_to_usd_cleaned_sale_stat_3 api_key:", api_key)
                    fin_result = process_to_usd_cleaned_sale_stat_3(cleaned_file_path, api_key)
                self.write({"code": 0, "msg": "success", "result_type": 3, "data": data, "cleaned": cleaned, "fin_cleaned": fin_result})
            elif result_type == 1:
                data = await SalesService().get_hot_sku_sales(query_params)
                output = {"code": 0, "msg": "success", "result_type": 1, "data": data}
                os.makedirs('unprocessed_data', exist_ok=True)
                filename = f"unprocessed_data/sale_stat_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(output, f, ensure_ascii=False, indent=2)
                self.write(output)
            else:
                self.set_status(400)
                self.write({"code": 1, "msg": "参数错误或未指定result_type"})
                return
        except Exception as e:
            import traceback
            print("[SaleStatHandler] 业务处理异常:", e)
            traceback.print_exc()
            self.set_status(500)
            self.write({"code": 1, "msg": f"业务处理异常: {e}"}) 