import pytest
import requests

BASE_URL = "https://dciit.cn:8013"
GLOBAL_ARGS = {"verify": False, "proxies": {}}

class TestUser:
    # GET /wx/user/index 个人中心数据（订单统计）（需鉴权）
    def test_user_index_login(self, auth_headers):
        """TC_USER_001 登录获取个人中心订单统计数据"""
        url = f"{BASE_URL}/wx/user/index"
        resp = requests.get(url, headers=auth_headers, **GLOBAL_ARGS)
        assert resp.status_code == 200
        res = resp.json()
        assert res["errno"] == 0
        assert "data" in res
        data = res["data"]
        assert "order" in data
        assert isinstance(data["order"], dict)
        # 按接口真实返回字段校验
        order_info = data["order"]
        assert "unpaid" in order_info
        assert "unship" in order_info
        assert "unrecv" in order_info
        assert "c_all" in order_info
        assert isinstance(order_info["unpaid"], int)
        assert isinstance(order_info["unship"], int)

    def test_user_index_no_token(self, public_headers):
        """TC_USER_002 未登录访问个人中心鉴权失败"""
        url = f"{BASE_URL}/wx/user/index"
        resp = requests.get(url, headers=public_headers, **GLOBAL_ARGS)
        assert resp.status_code == 200
        res = resp.json()
        assert res["errno"] != 0
        assert "errmsg" in res
        assert res["errmsg"] == "请登录"

    def test_user_index_empty_token(self, public_headers):
        """TC_USER_003 请求头Sgave-Mall-Token传空字符串，鉴权失败"""
        url = f"{BASE_URL}/wx/user/index"
        headers = public_headers.copy()
        # 正确token头部字段 Sgave-Mall-Token，不是token
        headers["Sgave-Mall-Token"] = ""
        resp = requests.get(url, headers=headers, **GLOBAL_ARGS)
        res = resp.json()
        assert res["errno"] != 0
        assert res["errmsg"] == "请登录"

    def test_user_index_invalid_token(self, public_headers):
        """TC_USER_004 传入随机非法token，鉴权失败"""
        url = f"{BASE_URL}/wx/user/index"
        headers = public_headers.copy()
        headers["Sgave-Mall-Token"] = "abc123456invalidtoken"
        resp = requests.get(url, headers=headers, **GLOBAL_ARGS)
        res = resp.json()
        assert res["errno"] != 0
        assert res["errmsg"] == "请登录"

    def test_user_index_expire_token(self, public_headers):
        """TC_USER_005 传入过期token，统一返回请登录"""
        url = f"{BASE_URL}/wx/user/index"
        headers = public_headers.copy()
        headers["Sgave-Mall-Token"] = "expire_token_000000"
        resp = requests.get(url, headers=headers, **GLOBAL_ARGS)
        res = resp.json()
        assert res["errno"] != 0
        assert res["errmsg"] == "请登录"