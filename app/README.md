# 业务服务层（Service Layer）说明文档

## 目录结构

`services/` 目录下，每个文件对应一个业务领域的 Service 类，负责该领域的所有业务逻辑处理。
所有 Service 均为异步类，便于与 Tornado、异步数据库、异步API等集成。

---

## 各 Service 文件说明

| 文件名                              | 类名                        | 业务领域/模块         | 主要职责举例                      |
|-------------------------------------|-----------------------------|----------------------|-----------------------------------|
| base_data_service.py                | BaseDataService             | 基础数据              | 获取基础数据、数据同步等           |
| sales_service.py                    | SalesService                | 销售                  | 获取销售报表、销售数据分析等       |
| fba_service.py                      | FBAService                  | FBA                   | 获取FBA库存、FBA订单等            |
| replenish_suggestion_service.py     | ReplenishSuggestionService  | 补货建议              | 获取补货建议、智能补货等           |
| replenish_limit_service.py          | ReplenishLimitService       | 补货限制              | 获取补货限制、限制规则管理等       |
| product_service.py                  | ProductService              | 产品                  | 获取产品列表、产品信息管理等       |
| purchase_service.py                 | PurchaseService             | 采购                  | 获取采购订单、采购流程等           |
| warehouse_service.py                | WarehouseService            | 仓库                  | 获取仓库列表、仓库管理等           |
| logistics_service.py                | LogisticsService            | 物流                  | 获取物流信息、物流跟踪等           |
| ad_service.py                       | AdService                   | 新广告                | 获取广告数据、广告投放等           |
| finance_service.py                  | FinanceService              | 财务                  | 获取财务报表、财务分析等           |
| customer_service.py                 | CustomerService             | 客服                  | 获取客服信息、客服工单等           |
| tools_service.py                    | ToolsService                | 工具                  | 各类工具型功能，如批量导入等       |
| statistics_service.py               | StatisticsService           | 统计                  | 获取统计数据、数据分析等           |
| target_service.py                   | TargetService               | 目标管理              | 获取目标数据、目标进度等           |
| multi_platform_service.py           | MultiPlatformService        | 多平台                | 获取多平台数据、平台对接等         |
| vc_service.py                       | VCService                   | VC                    | VC相关业务，如VC账号管理等         |
| amazon_table_service.py             | AmazonTableService          | 亚马逊源表数据         | 获取亚马逊原始表、数据同步等       |

---

## 设计原则

1. **单一职责**：每个 Service 只负责一个业务领域的逻辑处理。
2. **解耦**：Service 不处理 HTTP 请求/响应，仅专注于业务。
3. **可复用**：Service 可被多个 Handler 或其他 Service 调用。
4. **易扩展**：新增业务只需新增 Service 文件和类即可。

---

## 使用方式

- **Handler 层调用 Service 层**  
  例如，在 Handler 中调用销售服务：

  ```python
  from app.services.sales_service import SalesService

  class SalesReportHandler(RequestHandler):
      async def post(self):
          params = self.get_json_body()
          result = await SalesService().get_sales_report(params)
          self.write({"code": 0, "data": result})
  ```

- **Service 层可调用 utils 工具**  
  如日志、重试、时间处理等通用逻辑，直接 import utils 使用。

---

## 扩展说明

- 若某业务领域接口较多，可在 Service 类中增加多个方法，每个方法对应一个具体业务接口。
- 若有跨领域复用逻辑，可单独抽象为 utils 或 base_service.py。

---

## 结语

本目录结构和分层设计，旨在提升项目的可维护性、可扩展性和团队协作效率。
如需新增业务领域，只需仿照现有 Service 文件新建即可。

如有疑问或建议，欢迎随时补充！ 

## 汇率API并发与限流说明

本项目在处理销售数据时，调用 fastforex 汇率API进行多线程并发请求以提升效率。若遇到如下报错：

```
requests.exceptions.SSLError: HTTPSConnectionPool(host='api.fastforex.io', port=443): Max retries exceeded with url: ... (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] ...')))
```

通常是由于 API 请求频次或并发数过高，被 fastforex 服务器限流或主动断开连接。此时建议：

- 适当调小 `process_to_usd_cleaned_sale_stat_3` 的 `workers` 参数（如 3~5），降低并发数。
- 或在 `get_exchange_rate` 函数中增加 `time.sleep(0.1~0.5)`，人为延迟每次请求。
- 如需更高频率支持，请联系 fastforex 升级套餐。

相关参数可在 `stat_handler.py` 中调整。 