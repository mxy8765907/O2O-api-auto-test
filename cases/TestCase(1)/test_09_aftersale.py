import pytest
import requests

from conftest import public_headers

#=======订单参数============
#已完成/待评论/已收货订单，可以正常发起售后
completed_order_1 = {"orderId": 12139, "goodsId": 1181129, "desc": "已完成订单1，可评价、可售后、可再次购买、可删除"}
completed_order_2 = {"orderId": 12030, "goodsId": 1181129, "desc": "已完成订单2，可评价、可售后、可再次购买、可删除"}
completed_order_3 = {"orderId": 11907, "goodsId": 1181129, "desc": "已完成订单3，可评价、可售后、可再次购买、可删除"}
completed_order_4 = {"orderId": 11397, "goodsId": 1181129, "desc": "已完成订单4，可评价、可售后、可再次购买、可删除"}

all_completed_orders = [
    completed_order_1,
    completed_order_2,
    completed_order_3,
    completed_order_4
]

#====================售后列表模块====================
def test_after_001_empty(auth_headers,base_url):
    """tc_after_001 登录用户查询本人售后列表-空列表"""
    url=f"{base_url}/wx/aftersale/list"
    get_headers= auth_headers.copy()
    get_headers.pop("Content-Type", None)

    params = {
        "page": 1,
        "limit": 10
    }

    resp=requests.get(
        url=url,
        headers=get_headers,
        params=params,
        proxies={},
        verify=False
    )
    res=resp.json()
    print("登录后查看全部售后单",res)

    assert resp.status_code == 200
    #bug:售后列表接口本身异常，无法正常查询数据,错误码402
    assert res["errno"] == 0
    # 断言返回列表为空
    assert len(res["data"]["list"]) == 0


def test_after_002 (public_headers,base_url):
    """tc_after_002 游客未登录查询售后列表，预期鉴权失败返回402"""
    url=f"{base_url}/wx/aftersale/list"
    get_headers = public_headers.copy()
    get_headers.pop("Content-Type", None)

    params = {
        "page": 1,
        "limit": 10
    }
    resp=requests.get(
        url=url,
        headers=get_headers,
        params=params,
        verify=False,
        proxies={}
    )
    res=resp.json()
    print("游客查询全部售后订单",res)
    assert resp.status_code == 200
    assert res["errno"] == 402
    assert res["errmsg"] == "参数值不对"


def test_after_003(auth_headers,base_url):
    """tc_after_003 Token传空字符串查询售后列表，非法Token预期402"""
    url=f"{base_url}/wx/aftersale/list"
    get_headers = auth_headers.copy()
    get_headers.pop("Content-Type", None)
    empty_token_headers = {**get_headers, "Sgave-Mall-Token": ""}

    params = {
        "page": 1,
        "limit": 10
    }
    resp=requests.get(
        url=url,
        headers=empty_token_headers,
        params=params,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("空Token查询售后结果：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402



#====================提交售后模块====================
def test_after_apply_004(auth_headers,base_url):
    """tc_after_apply_004 提交售后申请：错误使用GoodsId非法参数，预期参数错误401"""
    url=f"{base_url}/wx/aftersale/submit"

    resp=requests.post(
        url=url,
        headers=auth_headers,
        json={
            "goodsId": 1001,
            "type": 0,
            "reason": "不想要了",
            "amount": 99.00,
            "pictures": []
        },
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("提交售后申请返回数据：", res)
    assert resp.status_code == 200
    assert res["errno"] == 401
    assert res["errmsg"] == "参数不对"


def test_after_apply_005(auth_headers, base_url):
    """tc_after_apply_005 正向用例：登录用户查询本人售后列表"""
    url = f"{base_url}/wx/aftersale/list"
    get_headers = auth_headers.copy()
    get_headers.pop("Content-Type", None)

    params = {
        "page": 1,
        "limit": 10
    }
    resp = requests.get(
        url=url,
        headers=get_headers,
        params=params,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("本人售后单列表返回数据：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0
    # bug:数据错误，返回401


def test_after_apply_006(auth_headers, base_url):
    """tc_after_apply_006 异常用例：查询不存在的售后ID，预期参数值错误402"""
    aftersale_id = 999999
    url = f"{base_url}/wx/aftersale/detail?id={aftersale_id}"
    get_headers = auth_headers.copy()
    get_headers.pop("Content-Type", None)

    resp = requests.get(
        url=url,
        headers=get_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("查询不存在售后ID返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402
    assert res["errmsg"] == "arg1不能为null"


def test_after_apply_007(auth_headers, base_url):
    """tc_after_apply_007 异常用例：越权-查看他人售后单，预期无权限参数值错误402"""
    other_aftersale_id = 12308
    url = f"{base_url}/wx/aftersale/detail?id={other_aftersale_id}"
    get_headers = auth_headers.copy()
    get_headers.pop("Content-Type", None)

    resp = requests.get(
        url=url,
        headers=get_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("越权查询他人售后单返回数据：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402
    assert res["errmsg"] == "arg1不能为null"


def test_after_apply_008(auth_headers, base_url):
    """tc_after_apply_008 异常用例：orderId参数为空提交售后申请，参数缺失预期401"""
    url = f"{base_url}/wx/aftersale/submit"
    req_body = {
        "orderId": "",
        "goodsId": completed_order_1["goodsId"],
        "type": 0,
        "reason": "不想要了",
        "amount": 199.00,
        "pictures": []
    }
    resp = requests.post(
        url=url,
        headers=auth_headers,
        json=req_body,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("orderId为空提交售后返回结果：", res)
    assert resp.status_code == 200
    assert res["errno"] == 401
    assert res["errmsg"] == "参数不对"

def test_after_apply_009(auth_headers, base_url):
    """tc_after_apply_009 正向用例：正常提交售后申请，生成待审核售后单"""
    url = f"{base_url}/wx/aftersale/submit"
    req_body = {
        "orderId": completed_order_2["orderId"],
        "goodsId": completed_order_2["goodsId"],
        "type": 0,
        "reason": "不想要了",
        "amount": 26.00,
        "pictures": []
    }
    resp = requests.post(
        url=url,
        headers=auth_headers,
        json=req_body,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("提交售后申请返回结果：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0



def test_after_apply_010(auth_headers, base_url):
    """tc_after_apply_010 正向用例：待审核售后单正常撤销"""
    url = f"{base_url}/wx/aftersale/cancel"
    req_body = {
        "afterSaleId": 13
    }
    resp = requests.post(
        url=url,
        headers=auth_headers,
        json=req_body,
        verify=False,
        proxies={}
    )
    res = resp.json()
    # bug:无法撤回待审核售后单，返回错误码401
    print(f"待审核售后单{req_body['afterSaleId']}撤销返回结果：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0

def test_after_apply_011(auth_headers, base_url):
    """tc_after_apply_011 异常用例：aftersaleId参数为空撤销售后，参数非法预期401"""
    url = f"{base_url}/wx/aftersale/cancel"
    req_body = {
        "aftersaleId": ""
    }
    resp = requests.post(
        url=url,
        headers=auth_headers,
        json=req_body,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("售后ID为空撤销返回结果：", res)
    assert resp.status_code == 200
    assert res["errno"] == 401
    assert res["errmsg"] == "参数不对"