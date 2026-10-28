
import requests
import pytest
# import Allure

def test_cart_001(auth_headers, base_url):
    """TC_CART_001 登录后正常查看购物车"""
    url = f"{base_url}/wx/cart/index"
    resp = requests.get(
        url=url,
        headers=auth_headers,
        verify=False,
        proxies={"http": None, "https": None}
    )
    res = resp.json()
    print("登录后购物车返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0
    # 校验返回是数组格式
    assert isinstance(res["data"]["cartList"], list)


def test_cart_002(public_headers, base_url):
        """TC_CART_002 未登录游客查看空购物车"""
        url = f"{base_url}/wx/cart/index"
        resp = requests.get(
            url=url,
            headers=public_headers,
            verify=False,
            json={},
            proxies={}
        )
        res = resp.json()
        print("游客访问购物车返回：", res)
        assert resp.status_code == 200
        assert res["errno"] == 501

def test_cart_003(base_url, auth_headers):
    """TC_CART_003 非法token访问购物车列表"""
    url = f"{base_url}/wx/cart/index"
    resp = requests.get(
        url=url,
        headers={**auth_headers, "Sgave-Mall-Token": "123456invalid"},
        verify=False,

        proxies={}
    )
    res = resp.json()
    print("非法token接口返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 501





 #--购物车商品--
def test_cart_004(auth_headers, base_url):
    """TC_CART_004 登录后查看购物车商品数量"""
    url = f"{base_url}/wx/cart/goodscount"
    resp = requests.get(
        url=url,
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("登录后购物车返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0



def test_cart_005(public_headers, base_url):
    """TC_CART_005 游客未登录查询购物车商品总数"""
    url = f"{base_url}/wx/cart/goodscount"
    resp = requests.get(
        url=url,
        headers=public_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("游客未登录查询购物车返回：", res)
    assert resp.status_code == 200
    #bug未登录游客不允许查询购物车，这个断言=0
    assert res["errno"] == 401



def test_cart_006(auth_headers, base_url):
    """TC_CART_006 过期token访问"""
    url = f"{base_url}//wx/cart/goodscount"
    resp = requests.get(
        url=url,
        headers={**auth_headers, "Sgave-Mall-Token": "expired_token909090909090"},
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("过期token接口返回：", res)
    assert resp.status_code == 200
    #bug 过期Token应该不能登录查看
    assert res["errno"] == 401






#--添加购物车--
def test_cart_007(auth_headers, base_url):
    """TC_CART_007 合法参数正常加入购物车"""
    url = f"{base_url}/wx/cart/add"
    resp = requests.post(
        url=url,
        json={"goodsId": 1116032,"number": 6,"productId": 170
},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("添加购物车返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0

##2
def test_cart_007_1(auth_headers, base_url):
    """TC_CART_007 合法参数正常加入购物车"""
    url = f"{base_url}/wx/cart/add"
    resp = requests.post(
        url=url,
        json={"goodsId": 1030003,"number": 6,"productId": 42
},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("添加购物车返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0



def test_cart_008(auth_headers, base_url):
    """TC_CART_008 number=0非法数量"""
    url = f"{base_url}/wx/cart/add"
    resp = requests.post(
        url=url,
        json={"goodsId": 1030003,"number": 0,"productId": 42
},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("添加购物车商品数量为空：", res)
    assert resp.status_code == 200
    #断言
    assert res["errno"] == 401
    assert res["errmsg"] == "参数不对"

def test_cart_009(auth_headers, base_url):
    """TC_CART_009 number=999超大值"""
    url = f"{base_url}/wx/cart/add"
    resp = requests.post(
        url=url,
        json={"goodsId": 1030003,"number": 99999,"productId": 42}
    )
    res = resp.json()
    print("添加购物车-购买数量传入超大值99999返回结果：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402
    assert res["errmsg"] == "参数值不对"

def test_cart_010(auth_headers, base_url):
    """TC_CART_010 缺失goodsId必填参数"""
    url = f"{base_url}/wx/cart/add"
    resp = requests.post(
        headers=auth_headers,
        url=url,
        json={"number": 2,"productId": 170}
    )
    res = resp.json()
    print("添加购物车-缺失goodsId必填参数返回结果：", res)
    assert resp.status_code == 200
    assert res["errno"] == 401
    assert res["errmsg"] == "参数不对"

def test_cart_011(auth_headers, base_url):
    """TC_CART_011 SQL注入goodsId参数"""
    url = f"{base_url}/wx/cart/add"
    resp = requests.post(
        url=url,
        json={"goodsId": "1' or 1=1;--","number": 2,"productId": 170}
    )
    res = resp.json()
    print("添加购物车-SQL注入goodsId参数返回结果：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402
    assert res["errmsg"] == "参数值不对"

# --删除购物车--
def test_cart_012(auth_headers, base_url):
    """TC_CART_012 删除购物车商品"""
    url = f"{base_url}/wx/cart/delete"
    resp = requests.post(
        headers=auth_headers,
        url=url,
        json={"productIds": [170]}
    )
    res = resp.json()
    print("删除购物车商品返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0




#--修改购物车数量--
def test_cart_013(auth_headers, base_url):
    """TC_CART_013 购物车中商品id不存在"""
    url = f"{base_url}/wx/cart/update"
    resp = requests.post(
        headers=auth_headers,
        url=url,
        json={"goodsId": 123456789,"number": 2,"productId": 170}
    )

    res = resp.json()
    print("修改购物车数量-购物车中商品id不存在返回结果：", res)
    assert resp.status_code == 200
    #断言
    assert res["errno"] == 401



def test_cart_014(auth_headers, base_url):
    """TC_CART_014 number空值"""
    url = f"{base_url}/wx/cart/update"
    resp = requests.post(
        headers=auth_headers,
        url=url,
        json={"goodsId": 1030003,"number": "","productId": 42}
    )
    res = resp.json()
    print("修改购物车数量-number空值返回结果：", res)
    assert resp.status_code == 200
    # 用例预期
    assert res["errno"] == 502
    assert res["errmsg"] == "系统内部错误"





#--选中商品--
def test_cart_015(auth_headers, base_url):
    """TC_CART_015 批量勾选商品"""
    url = f"{base_url}/wx/cart/checked"
    # 取消勾选
    resp_cancel = requests.post(
        headers=auth_headers,
        url=url,
        json={"cartIds": [7265, 7264], "isChecked": 0}
    )
    res_cancel = resp_cancel.json()
    assert resp_cancel.status_code == 200
    assert res_cancel["errno"] == 0

    #批量勾选
    resp = requests.post(
        headers=auth_headers,
        url=url,
        json={"cartIds": [7265, 7264], "isChecked": 1}
    )
    res = resp.json()
    print("批量勾选商品返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0


def test_cart_016(auth_headers, base_url):
    """TC_CART_016 goodsId传空数值"""
    url = f"{base_url}/wx/cart/checked"
    resp = requests.post(
        headers=auth_headers,
        url=url,
        json={"goodsId": [],"isChecked": 1}
    )
    res = resp.json()
    print("批量勾选商品-goodsId传空数值返回结果：", res)
    assert resp.status_code == 200
    # 用例预期
    assert res["errno"] == 401
    assert res["errmsg"] == "参数不对"


def test_cart_017(auth_headers, base_url):
    """TC_CART_017 isChecked传非0/1值"""
    url = f"{base_url}/wx/cart/checked"
    resp = requests.post(
        headers=auth_headers,
        url=url,
        json={"goodsId": [1116032,1030003],"isChecked": 2}
    )
    res = resp.json()
    print("批量勾选商品-isChecked传非0/1值返回结果：", res)
    assert resp.status_code == 200
    # 用例预期
    assert res["errno"] == 401





#--结算预览--
def test_cart_018(auth_headers, base_url):
    """TC_CART_018 获取结算信息"""
    url = f"{base_url}/wx/cart/checkout"
    resp = requests.get(
        url=url,
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("获取结算信息返回：", res)
    assert resp.status_code == 200
    #bug实际断言502
    assert res["errno"] == 0

def test_cart_019(public_headers, base_url):
    """TC_CART_019 获取结算信息-未登录"""
    url = f"{base_url}/wx/cart/checkout"
    resp = requests.get(
        headers=public_headers,
        url=url,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("获取结算信息-未登录返回结果：", res)
    assert resp.status_code == 200
    #预期断言
    assert res["errno"] == 501


def test_cart_020(auth_headers, base_url):
    """TC_CART_020 获取结算信息-购物车无商品"""
    url = f"{base_url}/wx/cart/checkout"
    resp = requests.get(
        url=url,
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("获取结算信息-商品不存在返回结果：", res)
    assert resp.status_code == 200
    assert res["errno"] == 502
    assert res["errmsg"] == "系统内部错误"

