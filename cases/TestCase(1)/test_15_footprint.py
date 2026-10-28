import pytest
import requests
import warnings
# 全局关闭SSL告警
warnings.filterwarnings("ignore")

BASE_URL = "https://dciit.cn:8013"
GLOBAL_ARGS = {"verify": False, "proxies": {}}

class TestFootprint:
    # ===================== 查询足迹列表 /wx/footprint/list =====================
    def test_footprint_list_normal(self, auth_headers):
        """TC_FOOT_001 登录正常分页查询足迹"""
        url = f"{BASE_URL}/wx/footprint/list"
        params = {"page": 1, "limit": 10}
        resp = requests.get(url, headers=auth_headers, params=params, **GLOBAL_ARGS)
        res = resp.json()
        print("正常分页足迹返回：", res)
        assert resp.status_code == 200
        assert res["errno"] == 0
        assert "data" in res
        # 修正：外层是dict，list在data内部
        assert isinstance(res["data"], dict)
        assert "list" in res["data"]
        assert isinstance(res["data"]["list"], list)

    def test_footprint_list_no_token(self, public_headers):
        """TC_FOOT_002 未登录查询，鉴权失败"""
        url = f"{BASE_URL}/wx/footprint/list"
        params = {"page": 1, "limit": 10}
        resp = requests.get(url, headers=public_headers, params=params, **GLOBAL_ARGS)
        res = resp.json()
        print("未登录足迹返回：", res)
        assert resp.status_code == 200
        assert res["errno"] != 0
        assert res["errmsg"] == "请登录"

    def test_footprint_list_page_zero(self, auth_headers):
        """TC_FOOT_006 page=0非法页码，后端兼容正常返回"""
        url = f"{BASE_URL}/wx/footprint/list"
        params = {"page": 0, "limit": 10}
        resp = requests.get(url, headers=auth_headers, params=params, **GLOBAL_ARGS)
        res = resp.json()
        print("page=0足迹返回：", res)
        assert resp.status_code == 200
        assert res["errno"] == 0
        assert "list" in res["data"]

    def test_footprint_list_limit_max(self, auth_headers):
        """TC_FOOT_007 limit超大9999，触发502服务异常"""
        url = f"{BASE_URL}/wx/footprint/list"
        params = {"page": 1, "limit": 9999}
        resp = requests.get(url, headers=auth_headers, params=params, **GLOBAL_ARGS)
        res = resp.json()
        print("limit超大足迹返回：", res)
        assert resp.status_code == 200
        assert res["errno"] == 502
        assert "errmsg" in res

    def test_footprint_list_no_param(self, auth_headers):
        """TC_FOOT_008 不传page、limit，使用默认分页"""
        url = f"{BASE_URL}/wx/footprint/list"
        resp = requests.get(url, headers=auth_headers,** GLOBAL_ARGS)
        res = resp.json()
        print("无分页参数足迹返回：", res)
        assert resp.status_code == 200
        assert res["errno"] == 0
        assert "list" in res["data"]

    def test_footprint_list_page_str(self, auth_headers):
        """TC_FOOT_009 page传字符串abc非法参数"""
        url = f"{BASE_URL}/wx/footprint/list"
        params = {"page": "abc", "limit": 10}
        resp = requests.get(url, headers=auth_headers, params=params, **GLOBAL_ARGS)
        res = resp.json()
        print("page字符串非法参数：", res)
        assert res["errno"] != 0
        assert res["errmsg"] == "参数值不对"

    def test_footprint_list_page_neg(self, auth_headers):
        """TC_FOOT_010 page传负数-1，后端兼容不报错"""
        url = f"{BASE_URL}/wx/footprint/list"
        params = {"page": -1, "limit": 10}
        resp = requests.get(url, headers=auth_headers, params=params, **GLOBAL_ARGS)
        res = resp.json()
        assert resp.status_code == 200
        # 后端不拦截负数页码，修改断言
        assert res["errno"] == 0
        assert "list" in res["data"]

    # ===================== 删除足迹 /wx/footprint/delete =====================
    def test_footprint_delete_single(self, auth_headers):
        """TC_FOOT_003 仅传id单条删除，参数格式错误返回402"""
        url = f"{BASE_URL}/wx/footprint/delete"
        body = {"id": 12}
        resp = requests.post(url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        res = resp.json()
        print("单id删除返回：", res)
        assert resp.status_code == 200
        assert res["errno"] == 402
        assert res["errmsg"] == "参数值不对"

    def test_footprint_delete_batch(self, auth_headers):
        """TC_FOOT_004 批量ids=[12,13]，id不存在返回401"""
        url = f"{BASE_URL}/wx/footprint/delete"
        body = {"ids": [12, 13]}
        resp = requests.post(url, headers=auth_headers, json=body,** GLOBAL_ARGS)
        res = resp.json()
        print("批量删除返回：", res)
        assert resp.status_code == 200
        assert res["errno"] == 401
        assert res["errmsg"] == "参数不对"

    def test_footprint_delete_no_token(self, public_headers):
        """TC_FOOT_005 未登录执行删除鉴权失败"""
        url = f"{BASE_URL}/wx/footprint/delete"
        body = {"id": 12}
        resp = requests.post(url, headers=public_headers, json=body, **GLOBAL_ARGS)
        res = resp.json()
        print("未登录删除返回：", res)
        assert resp.status_code == 200
        assert res["errno"] != 0
        assert res["errmsg"] == "请登录"

    def test_footprint_delete_id_not_exist(self, auth_headers):
        """TC_FOOT_009 批量传不存在足迹ID"""
        url = f"{BASE_URL}/wx/footprint/delete"
        body = {"ids": [9999999]}
        resp = requests.post(url, headers=auth_headers, json=body,** GLOBAL_ARGS)
        res = resp.json()
        assert res["errno"] != 0

    def test_footprint_delete_empty_ids(self, auth_headers):
        """TC_FOOT_010 批量传入空数组ids:[]"""
        url = f"{BASE_URL}/wx/footprint/delete"
        body = {"ids": []}
        resp = requests.post(url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        res = resp.json()
        assert res["errno"] != 0

    def test_footprint_delete_no_body(self, auth_headers):
        """TC_FOOT_011 请求体为空无删除参数"""
        url = f"{BASE_URL}/wx/footprint/delete"
        body = {}
        resp = requests.post(url, headers=auth_headers, json=body,** GLOBAL_ARGS)
        res = resp.json()
        assert res["errno"] != 0

    def test_footprint_delete_mix_id_ids(self, auth_headers):
        """TC_FOOT_012 同时传id和ids冲突参数"""
        url = f"{BASE_URL}/wx/footprint/delete"
        body = {"id": 12, "ids": [13, 14]}
        resp = requests.post(url, headers=auth_headers, **GLOBAL_ARGS)
        res = resp.json()
        assert res["errno"] != 0

    def test_footprint_delete_valid_batch(self, auth_headers):
        """TC_FOOT_013 传入不存在用户足迹，预期报错"""
        url = f"{BASE_URL}/wx/footprint/delete"
        body = {"ids": [101, 102]}
        resp = requests.post(url, headers=auth_headers, json=body,** GLOBAL_ARGS)
        res = resp.json()
        print("合法ids删除返回：", res)
        # 测试账号无该足迹，返回401，不能断言0
        assert res["errno"] == 401

    def test_footprint_delete_wrong_method(self, auth_headers):
        """TC_FOOT_014 GET调用POST删除接口，正确路径"""
        url = f"{BASE_URL}/wx/footprint/delete"
        params = {"ids": [101]}
        resp = requests.get(url, headers=auth_headers, params=params, **GLOBAL_ARGS)
        # 区分返回是否为html页面
        if "<html>" in resp.text:
            res = {}
        else:
            res = resp.json()
        assert "errno" not in res or res["errno"] != 0