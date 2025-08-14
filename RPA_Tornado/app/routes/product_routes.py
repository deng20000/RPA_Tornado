# 产品模块路由
# 负责注册产品相关的 API 路由

from app.handlers.product_handler import (
    LocalProductListHandler,                    # 查询本地产品列表
    UpcAddCommodityCodeHandler,                 # 创建UPC编码
    UpcListHandler,                             # 获取UPC编码列表
    LocalProductInfoHandler,                    # 查询本地产品详情
    BatchGetProductInfoHandler,                 # 批量查询本地产品详情
    ProductOperateBatchHandler,                 # 产品启用、禁用
    ProductSetHandler,                          # 添加/编辑本地产品
    AttributeListHandler,                       # 查询产品属性列表
    AttributeSetHandler,                        # 添加/编辑产品属性
    SpuListHandler,                             # 查询多属性产品列表
    SpuInfoHandler,                             # 查询多属性产品详情
    BundledProductListHandler,                  # 查询捆绑产品关系列表
    SetBundledProductHandler,                   # 添加/编辑捆绑产品
    ProductAuxListHandler,                      # 查询产品辅料列表
    SetAuxProductHandler,                       # 添加/编辑辅料
    BrandListHandler,                           # 查询产品品牌列表
    SetBrandHandler,                            # 添加/编辑产品品牌
    CategoryListHandler,                        # 查询产品分类列表
    SetCategoryHandler,                         # 添加/编辑产品分类
    UploadProductPicturesHandler,               # 上传本地产品图片
    ProductLabelListHandler,                    # 查询产品标签
    CreateProductLabelHandler,                  # 创建产品标签
    MarkProductLabelHandler,                    # 标记产品标签
    UnmarkProductLabelHandler,                  # 删除产品标签
)

product_routes = [
    # 本地产品相关接口
    ("/api/erp/sc/routing/data/local_inventory/productList", LocalProductListHandler),                  # 查询本地产品列表
    ("/api/erp/sc/routing/data/local_inventory/productInfo", LocalProductInfoHandler),                  # 查询本地产品详情
    ("/api/erp/sc/routing/data/local_inventory/batchGetProductInfo", BatchGetProductInfoHandler),       # 批量查询本地产品详情
    
    # UPC编码相关接口
    ("/api/listing/publish/api/upc/addCommodityCode", UpcAddCommodityCodeHandler),                      # 创建UPC编码
    ("/api/listing/publish/api/upc/upcList", UpcListHandler),                                           # 获取UPC编码列表
    
    # 产品管理接口
    ("/api/basicOpen/product/productManager/product/operate/batch", ProductOperateBatchHandler),       # 产品启用、禁用
    ("/api/erp/sc/routing/storage/product/set", ProductSetHandler),                                     # 添加/编辑本地产品
    
    # 产品属性管理接口
    ("/api/erp/sc/routing/storage/attribute/attributeList", AttributeListHandler),                      # 查询产品属性列表
    ("/api/erp/sc/routing/storage/attribute/set", AttributeSetHandler),                                 # 添加/编辑产品属性
    
    # 多属性产品管理接口
    ("/api/erp/sc/routing/storage/spu/spuList", SpuListHandler),                                        # 查询多属性产品列表
    ("/api/erp/sc/routing/storage/spu/info", SpuInfoHandler),                                           # 查询多属性产品详情
    
    # 捆绑产品相关接口
    ("/api/erp/sc/routing/data/local_inventory/bundledProductList", BundledProductListHandler),         # 查询捆绑产品关系列表
    ("/api/erp/sc/routing/storage/product/setBundled", SetBundledProductHandler),                       # 添加/编辑捆绑产品
    
    # 产品辅料相关接口
    ("/api/erp/sc/routing/data/local_inventory/productAuxList", ProductAuxListHandler),                 # 查询产品辅料列表
    ("/api/erp/sc/routing/storage/product/setAux", SetAuxProductHandler),                               # 添加/编辑辅料
    
    # 产品品牌相关接口
    ("/api/erp/sc/data/local_inventory/brand", BrandListHandler),                                       # 查询产品品牌列表
    ("/api/erp/sc/storage/brand/set", SetBrandHandler),                                                 # 添加/编辑产品品牌
    
    # 产品分类相关接口
    ("/api/erp/sc/routing/data/local_inventory/category", CategoryListHandler),                         # 查询产品分类列表
    ("/api/erp/sc/routing/storage/category/set", SetCategoryHandler),                                   # 添加/编辑产品分类
    
    # 产品图片相关接口
    ("/api/erp/sc/routing/storage/product/uploadPictures", UploadProductPicturesHandler),               # 上传本地产品图片
    
    # 产品标签相关接口
    ("/api/label/operation/v1/label/product/list", ProductLabelListHandler),                            # 查询产品标签
    ("/api/label/operation/v1/label/product/create", CreateProductLabelHandler),                        # 创建产品标签
    ("/api/label/operation/v1/label/product/mark", MarkProductLabelHandler),                            # 标记产品标签
    ("/api/label/operation/v1/label/product/unmarkLabel", UnmarkProductLabelHandler),                   # 删除产品标签
]
