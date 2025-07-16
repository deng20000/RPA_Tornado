# RPA_Tornado 项目说明

## 一、项目结构

- app/ecommerce_dashboard/handlers/stat_handler.py  # 电商数据看板主接口
- app/ecommerce_dashboard/services/stat_service.py  # 电商数据看板主业务逻辑
- app/ecommerce_dashboard/services/common.py        # 通用API请求工具
- app/ecommerce_dashboard/routes.py                 # 路由注册
- main.py                                          # 启动入口，统一管理所有接口

## 二、依赖安装

建议使用虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt  # 如有requirements.txt
```

## 三、环境配置

请在 app/config.py 中配置 API HOST、APP_ID、APP_SECRET 等参数。

## 四、项目启动

在项目根目录下执行：

```bash
python RPA_Tornado/main.py
```

启动后访问接口如：
- POST http://127.0.0.1:8888/api/ecommerce/sale_stat

## 五、接口说明

### 统一接口：/api/ecommerce/sale_stat

- **每日电商总销售额**
  - 参数：
    - result_type: 3
    - date_unit: 4
    - data_type: 6
    - 其他可选参数
- **热门SKU销量查看**
  - 参数：
    - result_type: 1
    - date_unit: 4
    - data_type: 6
    - 其他可选参数

请求示例：
```json
{
  "result_type": 3,
  "date_unit": 4,
  "data_type": 6
}
```

返回示例：
```json
{
  "code": 0,
  "data": { ... }
}
```

## 六、测试

运行测试用例：
```bash
pytest RPA_Tornado/tests/test_ecommerce_dashboard.py -s
```

---
如有更多子项目或接口需求，建议仿照本结构扩展即可。 