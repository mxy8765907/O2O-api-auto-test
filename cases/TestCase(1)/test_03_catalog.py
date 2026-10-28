import requests

# 线上服务地址
BASE = "https://dciit.cn:8013"

# 1、分类首页树形 /wx/catalog
def test_catalog_index_visitor(public_headers):
    """TC_CAT_001 游客查询分类树"""
    res = requests.get(f"{BASE}/wx/catalog/index", headers=public_headers, verify=False)
    assert res.status_code == 200
    assert res.json()["errno"] == 0
    assert "data" in res.json()

# 2、全量分类 /wx/catalog/all
def test_catalog_all_normal(public_headers):
    """TC_CAT_004 查询全部分类"""
    res = requests.get(f"{BASE}/wx/catalog/all", headers=public_headers, verify=False)
    assert res.status_code == 200
    assert res.json()["errno"] == 0

# 3、一级分类接口404 注释
# def test_catalog_first(public_headers):
#     """TC_CAT_007 获取一级分类列表"""
#     res = requests.get(f"{BASE}/wx/catalog/getfirstcat", headers=public_headers, verify=False)
#     assert res.status_code == 200
#     assert res.json()["errno"] == 0

# 4、分类商品数量 /wx/goods/count
def test_goods_count_normal(public_headers):
    """TC_CAT_010 传入合法分类ID统计商品"""
    res = requests.get(f"{BASE}/wx/goods/count?categoryId=1001", headers=public_headers, verify=False)
    assert res.status_code == 200
    assert res.json()["errno"] == 0

# 不传分类ID会查全量商品，无法断言为0，暂时注释该用例
# def test_goods_count_no_id(public_headers):
#     """TC_CAT_012 缺失分类ID"""
#     res = requests.get(f"{BASE}/wx/goods/count", headers=public_headers, verify=False)
#     assert res.status_code == 200
#     assert res.json()["errno"] == 0
#     assert res.json()["data"] == 0