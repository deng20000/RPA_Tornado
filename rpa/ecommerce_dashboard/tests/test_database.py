from datetime import date
import logging
from typing import Optional
from manage_data import DatabaseManager, Base, Shop, Sale, ExchangeRate

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_database():
    """测试数据库连接和基本操作"""
    try:
        pass
        # # 创建数据库管理器
        # db = DatabaseManager()
        
        # # 删除已存在的表
        # engine = db.engine
        # Base.metadata.drop_all(engine)
        
        # # 初始化数据库表
        # db.init_db()
        
        # # 测试添加店铺
        # # shop = db.add_shop(
        # #     shop_id="TEST001",
        # #     platform_id="taobao_12345",
        # #     platform="淘宝"
        # # )
        # if shop:
        #     logger.info(f"添加店铺成功: {shop.shop_id}")
        # else:
        #     raise Exception("店铺添加失败")
        
        # # 测试添加销售记录
        # sale_data = {
        #     'sale_id': 1,
        #     'shop_id': "TEST001",
        #     'sale_date': date.today(),
        #     'cny_amount': 100.00,
        #     'usd_amount': 15.00
        # }
        # sale = db.add_sale(sale_data)
        # if sale:
        #     logger.info(f"添加销售记录成功: {sale.sale_id}")
        # else:
        #     raise Exception("销售记录添加失败")
        
        # # 测试添加汇率
        # rate_data = {
        #     'date': date.today(),
        #     'currency_code': 'USD',
        #     'currency_icon': '$',
        #     'currency_name': '美元',
        #     'user_rate': 6.5000000000,
        #     'org_rate': 6.4800000000
        # }
        # rate = db.add_exchange_rate(rate_data)
        # if rate:
        #     logger.info(f"添加汇率记录成功: {rate.id}")
        # else:
        #     raise Exception("汇率记录添加失败")
        
        # # 测试查询功能
        # sales = db.get_shop_sales("TEST001", date.today(), date.today())
        # logger.info(f"查询到 {len(sales)} 条销售记录")
        
        # # 测试更新功能
        # db.update_shop(
        #     shop_id="TEST001",
        #     new_data={"platform": "天猫"}
        # )
        # logger.info("更新店铺信息成功")
        
        # # 测试删除功能
        # db.delete_sale(1)
        # logger.info("删除销售记录成功")
        
        # return True
        
    except Exception as e:
        logger.error(f"测试过程中出现错误: {str(e)}")
        return False

def main():
    """主函数"""
    success = test_database()
    if success:
        logger.info("所有测试用例执行成功!")
    else:
        logger.error("测试执行失败，请检查日志获取详细信息。")

if __name__ == "__main__":
    main()
