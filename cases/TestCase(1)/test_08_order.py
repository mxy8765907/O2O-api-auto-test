from idlelib.format import get_comment_header
from multiprocessing.connection import deliver_challenge

import requests
import pytest


#====================================购物车自动加商品=====================

@pytest.fixture(scope="function")
def cart_data(auth_headers, base_url):
    """每次用例执行前校验购物车，自动加商品到购物车里头"""
    cart_url = f"{base_url}/wx/cart/index"
    resp = requests.get(url=cart_url, headers=auth_headers, verify=False)
    res = resp.json()
    assert res["errno"] == 0, f"查询购物车失败：{res}"
    cart_list = res["data"]["cartList"]

    # 空购物车加商品
    if len(cart_list) == 0:
        add_cart_url = f"{base_url}/wx/cart/add"
        add_params = {
            "goodsId":1023003,
            "number": 1,
            "productId": 32
        }
        requests.post(url=add_cart_url, json=add_params, headers=auth_headers, verify=False)
        # 重新拉取购物车数据
        resp = requests.get(url=cart_url, headers=auth_headers, verify=False)
        res = resp.json()
        cart_list = res["data"]["cartList"]

    assert len(cart_list) > 0, "购物车自动添加商品失败"
    return res["data"]

@pytest.fixture(scope="function")
def cart_id(cart_data):
    # 取购物车第一条商品的ID
    return cart_data["cartList"][0]["id"]






#==========================================商品订单参数化========================================

# 1. ==========五种状态订单===========
# 6条待付款订单
# 待付款订单30分钟未支付会自动关闭失效，需经常更新

unpaid_order_1 = {"orderId": 12391, "goodsId": 24170, "desc": "unpaid_order_1 未付款单个商品订单"}
unpaid_order_2 = {"orderId": 12390, "goodsId": 24169, "desc": "unpaid_order_2 未付款单个商品订单"}
unpaid_order_3 = {"orderId": 12389, "goodsId": 24168, "desc": "unpaid_order_3 未付款单个商品订单"}
unpaid_order_4 = {"orderId": 12388, "goodsId": 24167, "desc": "unpaid_order_4 未付款单个商品订单"}
unpaid_order_5 = {"orderId": 12387, "goodsId": 24166, "desc": "unpaid_order_5 未付款单个商品订单"}
unpaid_order_6 = {"orderId": 12386, "goodsId": 24165, "desc": "unpaid_order_6 未付款单个商品订单"}

# 全部待付款订单集合
all_unpaid_orders = [
    unpaid_order_1,
    unpaid_order_2,
    unpaid_order_3,
    unpaid_order_4,
    unpaid_order_5,
    unpaid_order_6
]
# 已付款订单
paid_order_1 = {"orderId": 11266, "goodsId": 23013, "desc": "paid_order_1 已付款订单，支持仅退款售后"}
paid_order_2 = {"orderId": 11265, "goodsId": 23012, "desc": "paid_order_2 已付款订单，支持仅退款售后"}
paid_order_3 = {"orderId": 11264, "goodsId": 23011, "desc": "paid_order_3 已付款订单，支持仅退款售后"}
paid_order_4 = {"orderId": 11263, "goodsId": 23010, "desc": "paid_order_4 已付款订单，支持仅退款售后"}

all_paid_orders = [
    paid_order_1,
    paid_order_2,
    paid_order_3,
    paid_order_4
]

#已发货，待收货订单
delivered_order_1 = {"orderId": 12264, "goodsId": 1181129, "desc": "已发货待收货订单1，可确认收货"}
delivered_order_2 = {"orderId": 12029, "goodsId": 1181129, "desc": "已发货待收货订单2，可确认收货"}
delivered_order_3 = {"orderId": 11900, "goodsId": 1181129, "desc": "已发货待收货订单3，可确认收货"}
delivered_order_4 = {"orderId": 11393, "goodsId": 1181129, "desc": "已发货待收货订单4，可确认收货"}

all_delivered_orders = [
    delivered_order_1,
    delivered_order_2,
    delivered_order_3,
    delivered_order_4
]


#已退款
refunded_order = {"orderId": 12383, "goodsId": 1181129, "desc": "Refunded, after-sale unavailable"}
refunded_order = {"orderId": 12382, "goodsId": 1181129, "desc": "Refunded, after-sale unavailable"}
refunded_order = {"orderId": 12381, "goodsId": 1181129, "desc": "Refunded, after-sale unavailable"}




#待评论
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

# 2. ========已完成+未付款+已付款+退款
all_orders = [all_completed_orders, all_unpaid_orders, all_paid_orders,all_delivered_orders,refunded_order]




# --订单列表接口 --
def test_order_001(auth_headers, base_url):
    """TC_ORDER_001：正常查询全部订单列表"""
    url = f"{base_url}/wx/order/list"
    resp = requests.get(
        url=url,
        params={"showType": 0},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("正常查询全部订单返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0




def test_order_002(auth_headers, base_url):
    """TC_ORDER_002：查询待付款订单（showType=1）"""
    url = f"{base_url}/wx/order/list"
    resp = requests.get(
        url=url,
        params={"showType": 1},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("查询待付款订单返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0


def test_order_003(auth_headers, base_url):
    """TC_ORDER_003：showType传99非法值，后端未做参数校验，实际返回0"""
    url = f"{base_url}/wx/order/list"
    resp = requests.get(
        url=url,
        params={"showType":111199},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("showType传非法值99返回：", res)
    assert resp.status_code == 200
    # bug 实际执行返回errno=0
    assert res["errno"] == 402


def test_order_004(public_headers, base_url):
    """TC_ORDER_004：未登录无token访问订单列表，鉴权失败实际返回501"""
    url = f"{base_url}/wx/order/list"
    resp = requests.get(
        url=url,
        params={"showType": 0},
        headers=public_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("未登录访问订单列表返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 501


# -订单详情接口 -
def test_order_005(auth_headers, base_url):
    """TC_ORDER_005：查询本人已完成订单详情"""
    url = f"{base_url}/wx/order/detail"
    order_id = completed_order_1
    resp = requests.get(
        url=url,
        params={"orderId": completed_order_3["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print(f"查询已完成订单{order_id}详情返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0


def test_order_006(auth_headers, base_url):
    """TC_ORDER_006：订单ID不存在，返回402"""
    url = f"{base_url}/wx/order/detail"
    resp = requests.get(
        url=url,
        params={"orderId": 9999999999},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("订单ID不存在返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402


# - 提交订单接口 -
def test_order_007(auth_headers, base_url, usable_coupon,cart_id):
    """TC_ORDER_007：使用优惠券下单"""
    url = f"{base_url}/wx/order/submit"
    resp = requests.post(
        url=url,
        json={
            "addressId": 1122,
            "cartId": cart_id,
            "couponId":usable_coupon["couponId"],
            "grouponLinkId": 0,
            "grouponRulesId": 0,
            "message": "尽快发货",
            "userCouponId": usable_coupon["userCouponId"]
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("使用优惠券正常提交订单返回：", res)
    assert resp.status_code == 200
    # 优惠券失效预期402
    assert res["errno"] == 402


def test_order_008(auth_headers, base_url, usable_coupon,cart_id):
    """TC_ORDER_008：不使用优惠券提交订单"""
    url = f"{base_url}/wx/order/submit"
    resp = requests.post(
        url=url,
        json={
            "cartId": cart_id,
            "addressId": 1122,
            "couponId": 0,
            "grouponLinkId": 0,
            "grouponRulesId": 0,
            "message": "",
            "userCouponId": 0
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("不使用优惠券提交订单返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0


def test_order_009(auth_headers, base_url,cart_id):
    """TC_ORDER_009：缺失addressId收货地址，实际返回401"""
    url = f"{base_url}/wx/order/submit"
    resp = requests.post(
        url=url,
        json={
            "cartId": cart_id,
            "couponId": -1,
            "message": ""
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("缺失收货地址返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 401


def test_order_010(auth_headers, base_url,cart_id):
    """TC_ORDER_010：优惠券ID不存在（couponId=11），返回402"""
    url = f"{base_url}/wx/order/submit"
    resp = requests.post(
        url=url,
        json={
            "cartId": cart_id,
            "addressId": 1122,
            "couponId": 11,
            "message": ""
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("优惠券不存在返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402


def test_order_011(auth_headers, base_url,cart_id):
    """TC_ORDER_011：并发提交订单"""
    url = f"{base_url}/wx/order/submit"
    results = []
    for i in range(100):
        resp = requests.post(
            url=url,
            json={
                "cartId": cart_id,
                "addressId": 1122,
                "couponId": -1,
                "message": f"并发测试{i}"
            },
            headers=auth_headers,
            verify=False,
            proxies={}
        )
        results.append(resp.json())

    print("并发提交订单结果统计：")
    success_count = sum(1 for r in results if r["errno"] == 0)
    fail_count = sum(1 for r in results if r["errno"] != 0)
    print(f"成功：{success_count} 次，失败：{fail_count} 次")
    print("最后一次请求返回：", results[-1])

    assert resp.status_code == 200
    assert results[-1]["errno"] == 502

#-取消订单接口 -
def test_order_012(auth_headers, base_url):
    """TC_ORDER_012：待付款订单正常取消"""
    url = f"{base_url}/wx/order/cancel"
    resp = requests.post(
        url=url,
        json={"orderId": unpaid_order_2["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("取消待付款订单返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0


def test_order_013(auth_headers, base_url):
    """TC_ORDER_013：订单ID为空数组，参数错误返回402"""
    url = f"{base_url}/wx/order/cancel"
    resp = requests.post(
        url=url,
        json={"orderId": []},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("订单ID为空返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402



# --预支付--
def test_order_014(auth_headers, base_url):
    """TC_ORDER_014：待付款订单生成支付单"""
    url = f"{base_url}/wx/order/prepay"
    resp = requests.post(
        url=url,
        json={"orderId": unpaid_order_2["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("待付款订单生成支付单返回：", res)
    assert resp.status_code == 200

    # assert res["errno"] == 0


def test_order_015(auth_headers, base_url):
    """TC_ORDER_015：已支付订单重复预支付"""
    url = f"{base_url}/wx/order/prepay"
    # 先正常预支付
    requests.post(url=url, json={"orderId":completed_order_1}, headers=auth_headers, verify=False, proxies={})
    # 重复调用
    resp = requests.post(
        url=url,
        json={"orderId": completed_order_2["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("已支付订单重复预支付返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 725






#--模拟支付--
def test_order_017(auth_headers, base_url):
    """TC_ORDER_017：待付款订单模拟支付成功"""
    url = f"{base_url}/wx/order/simulation-pay"
    resp = requests.post(
        url=url,
        json={"orderId":unpaid_order_3["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("待付款订单模拟支付成功返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0


def test_order_018(auth_headers, base_url):
    """TC_ORDER_018：取消订单支付，返回725"""
    url = f"{base_url}/wx/order/simulation-pay"
    resp = requests.post(
        url=url,
        #这个订单没有参数化，演示的时候必须手动取消获得取消的订单ID
        json={"orderId":12587},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("已取消订单支付返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 725


def test_order_019(auth_headers, base_url):
    """TC_ORDER_019：同一订单重复支付验证"""
    url = f"{base_url}/wx/order/simulation-pay"
    requests.post(url=url, json={"orderId": completed_order_1["orderId"]}, headers=auth_headers, verify=False, proxies={})
    resp = requests.post(
        url=url,
        json={"orderId":completed_order_2["orderId"] },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("同一订单重复支付返回：", res)
    assert resp.status_code == 200
    ##没有做已支付订单重复支付的拦截
    assert res["errno"] == 725


def test_order_020(auth_headers, base_url):
    """TC_ORDER_020：篡改未付款订单金额参数，系统异常502"""
    url = f"{base_url}/wx/order/simulation-pay-notify"
    resp = requests.post(
        url=url,
        json={
            "orderId": unpaid_order_4["orderId"],
            "payAmount": 0.01,
            "payStatus": 1
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("篡改订单金额回调返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 502


# --申请退款接口--
def test_order_021(auth_headers, base_url):
    """TC_ORDER_021：待发货订单正常退款"""
    url = f"{base_url}/wx/order/refund"
    order_id = paid_order_1["orderId"]
    resp = requests.post(
        url=url,
        json={"orderId": paid_order_1["orderId"], "refundReason": "商品不满意"},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print(f"待发货订单{order_id}正常退款返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0





def test_order_022(auth_headers, base_url):
    """TC_ORDER_022：重复提交退款申请"""
    url = f"{base_url}/wx/order/refund"
    requests.post(url=url, json={"orderId": refunded_order["orderId"], }, headers=auth_headers, verify=False, proxies={})
    resp = requests.post(
        url=url,
        json={"orderId": refunded_order["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("重复提交退款申请返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 725


#--确认收货--
def test_order_023(auth_headers, base_url):
    """TC_ORDER_023：已发货订单确认收货"""
    url = f"{base_url}/wx/order/confirm"
    resp = requests.post(
        url=url,
        json={"orderId":delivered_order_2["orderId"] },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("已发货订单确认收货返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0


def test_order_024(auth_headers, base_url,):
    """TC_ORDER_024：待付款订单确认收货，业务异常725"""
    url = f"{base_url}/wx/order/confirm"
    resp = requests.post(
        url=url,
        #待付款ID
        json={"orderId":unpaid_order_5["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("待付款订单确认收货返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 725


def test_order_025(auth_headers, base_url):
    """TC_ORDER_025：已收货订单重复确认幂等验证"""
    url = f"{base_url}/wx/order/confirm"
    requests.post(url=url, json={"orderId": completed_order_1["orderId"]}, headers=auth_headers, verify=False, proxies={})
    resp = requests.post(
        url=url,
        json={"orderId": completed_order_2["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("已收货订单重复确认返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 725


#--删除订单接口--
def test_order_026(auth_headers, base_url,):
    """TC_ORDER_026：已完成可删除订单"""
    url = f"{base_url}/wx/order/delete"
    resp = requests.post(
        url=url,
        json={"orderId": completed_order_2["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("已完成订单删除返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0



def test_order_027(auth_headers, base_url ):
    """TC_ORDER_027：待付款订单删除"""
    url = f"{base_url}/wx/order/delete"
    resp = requests.post(
        url=url,
        json={"orderId":12586},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("待付款订单删除返回：", res)
    assert resp.status_code == 200
    #bug:待付款订单只能取消订单，不能删除。
    assert res["errno"] == 0


def test_order_028(auth_headers, base_url):
    """TC_ORDER_028：已发货待收货订单不可删除"""
    url = f"{base_url}/wx/order/delete"
    resp = requests.post(
        url=url,
        json={"orderId":delivered_order_1 ["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("已发货待收货订单删除返回：", res)
    assert resp.status_code == 200
    #bug返回0
    assert res["errno"] == 401


#--待评价商品--
def test_order_029(auth_headers, base_url):
    """TC_ORDER_029 查询待评论订单商品列表"""
    url = f"{base_url}/wx/order/list"
    get_headers = auth_headers.copy()
    if "Content-Type" in get_headers:
        del get_headers["Content-Type"]

    resp = requests.get(
        url=url,
        headers=get_headers,
        verify=False,
        proxies={"http": None, "https": None}
    )
    res = resp.json()
    print("用户订单列表返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0
    # 校验订单列表为数组
    assert isinstance(res["data"]["list"], list)


def test_order_030(auth_headers, base_url):
    """TC_ORDER_030：未收货订单查询待评价商品"""
    url = f"{base_url}/wx/order/goods"
    resp = requests.get(
        url=url,
        params={"orderId":paid_order_1["orderId"]},
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("未收货订单查询待评价商品返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402


# -- 订单评价接口  --
def test_order_031(auth_headers, base_url):
    """TC_ORDER_031：查询某款商品评论列表"""
    url = f"{base_url}/wx/comment/list"
    headers = auth_headers.copy()
    if "Content-Type" in headers:
        del headers["Content-Type"]
    # 入参说明
    # type：0=商品评论，1=订单评论
    # valueId：商品ID/订单ID
    # showType：0=全部 1=好评 2=中评 3=差评
    params = {
        "type": 1,
        "valueId":completed_order_1["goodsId"],
        "showType": 0,
    }
    resp = requests.get(
        url=url,
        params=params,
        headers=headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("商品评论列表返回结果：", res)

    # 基础断言
    assert resp.status_code == 200
    assert res["errno"] == 0
    # 校验返回列表为数组格式
    assert isinstance(res["data"]["list"], list)



# -- 订单评价接口  --
#获得待评价商品valueId
def test_get_detail(auth_headers, base_url):
    url = f"{base_url}/wx/order/detail"
    params = {"orderId": 12265}
    resp = requests.get(url, params=params, headers=auth_headers, verify=False)
    print(resp.json())

def test_order_032(auth_headers, base_url):
    """TC_ORDER_035：正常五星评价"""
    url = f"{base_url}/wx/comment/post"
    resp = requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "content": "商品质量很好，物流很快，推荐购买",
            "star": 5,
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("订单五星评价返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 0


def test_order_033(auth_headers, base_url):
    """TC_ORDER_033：star=0非法星级，参数值异常场景"""
    url = f"{base_url}/wx/comment/post"
    resp = requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "star": 0,
            "content": "商品不错",
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("star=0非法星级评价返回：", res)
    assert resp.status_code == 200
    # bug:star=0也能成功评价，实际返回0
    assert res["errno"] == 402


def test_order_034(auth_headers, base_url):
    """TC_ORDER_034：重复评价同一商品，预期返回参数值错误402"""
    url = f"{base_url}/wx/comment/post"
    # 第一次正常提交评价
    requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "star": 5,
            "content": "第一次评价",
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    # 第二次重复提交同一商品评价
    resp = requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "star": 4,
            "content": "重复评价",
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("重复评价同一商品返回：", res)
    assert resp.status_code == 200
    # bug:重复评价属于业务参数值非法，实际断言错误码0
    assert res["errno"] == 402

def test_order_035(auth_headers, base_url):
    """TC_ORDER_035：评价内容SQL注入场景测试，非法内容预期参数错误402"""
    url = f"{base_url}/wx/comment/post"
    resp = requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "star": 5,
            "content": "1' or 1=1;delete from user;--",
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("评价内容SQL注入返回：", res)
    assert resp.status_code == 200
    #bug:  sql注入成功，预期:402,实际:0
    assert res["errno"] == 402


def test_order_036(public_headers, base_url):
    """TC_ORDER_036：未登录状态提交商品评价，预期未登录错误码501"""
    url = f"{base_url}/wx/comment/post"
    resp = requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "star": 5,
            "content": "未登录测试评价",
            "hasPicture": False,
            "picUrls": []
        },
        headers=public_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("未登录评价返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 501

def test_order_037(auth_headers, base_url):
    """TC_ORDER_037：star=6超上限非法星级（参数值非法，预期402）"""
    url = f"{base_url}/wx/comment/post"
    resp = requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "star": 6,
            "content": "五星好评测试",
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("star=6超上限评价返回：", res)
    assert resp.status_code == 200
    # 星级数值超出合法范围，属于参数值错误，断言402
    assert res["errno"] == 402


def test_order_038(auth_headers, base_url,):
    """TC_ORDER_038：content为空白（参数值非法，预期402）"""
    url = f"{base_url}/wx/comment/post"
    resp = requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "star": 5,
            "content": "",
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("评价内容为空返回：", res)
    assert resp.status_code == 200
    # 评论内容不能为空，参数值非法
    assert res["errno"] == 401


def test_order_039(auth_headers, base_url):
    """TC_ORDER_039：图片参数非法数组（参数类型错误，预期401）"""
    url = f"{base_url}/wx/comment/post"
    resp = requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "star": 5,
            "content": "好评",
            "hasPicture": True,
            "picUrls": "非法字符串不是数组"
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("图片参数非法数组返回：", res)
    assert resp.status_code == 200
    # 参数类型不符合接口要求（要求数组传入字符串），断言401
    assert res["errno"] == 502


def test_order_040(auth_headers, base_url):
    """TC_ORDER_040：他人订单/不存在valueId越权评价（数据不存在，预期404）"""
    url = f"{base_url}/wx/comment/post"
    resp = requests.post(
        url=url,
        json={
            "valueId": 9999999,
            "type": 0,
            "star": 5,
            "content": "越权评价他人订单",
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("他人订单越权评价返回：", res)
    assert resp.status_code == 200
    assert res["errno"] == 402


def test_order_041(auth_headers, base_url):
    """TC_ORDER_041：待付款未确认收货订单评价（业务状态非法，预期402）"""
    url = f"{base_url}/wx/comment/post"
    resp = requests.post(
        url=url,
        json={
            "valueId": unpaid_order_5["goodsId"],
            "type": 0,
            "star": 5,
            "content": "待付款订单评价测试",
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("待付款订单评价返回：", res)
    assert resp.status_code == 200
    # 订单状态不支持评价，属于业务参数值非法
    assert res["errno"] == 402


def test_order_042(auth_headers, base_url):
    """TC_ORDER_042：超长评论500以上（参数值超长非法，预期402）"""
    url = f"{base_url}/wx/comment/post"
    long_content = "商品很好，非常满意，物流速度很快，客服态度也很好。" * 60
    resp = requests.post(
        url=url,
        json={
            "valueId": 1181129,
            "type": 0,
            "star": 5,
            "content": long_content,
            "hasPicture": False,
            "picUrls": []
        },
        headers=auth_headers,
        verify=False,
        proxies={}
    )
    res = resp.json()
    print("超长评论评价返回：", res)
    assert resp.status_code == 200
    # 评论内容超出长度限制，参数值非法
    assert res["errno"] == 502