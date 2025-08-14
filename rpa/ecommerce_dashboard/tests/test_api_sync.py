from api_client import ApiClient
from manage_data import DatabaseManager, GetData
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_api_sync():
    """测试API同步功能"""
    try:
        # 创建API客户端
        api_client = ApiClient()
        
        # 创建数据库管理器
        db_manager = DatabaseManager()
        
        # 确保数据库表存在
        db_manager.init_db()
        
        # 从API获取数据
        api_data = api_client.get_seller_list()
        if api_data is None:
            logger.error("无法从API获取数据")
            return False
            
        # 同步数据到数据库
        success = GetData.sync_store_data(db_manager, api_data)
        
        if success:
            logger.info("店铺数据同步成功")
        else:
            logger.error("店铺数据同步失败")
            
        return success
        
    except Exception as e:
        logger.error(f"测试过程中出现错误: {str(e)}")
        return False

if __name__ == "__main__":
    test_api_sync()
