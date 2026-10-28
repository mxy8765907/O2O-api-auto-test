import pytest
import requests
import warnings
warnings.filterwarnings("ignore")

GLOBAL_ARGS = {"verify": False, "proxies": {}}


class TestSearch:
    # GET /wx/search/index 搜索页面信息（无需鉴权）
    def test_search_index(self, base_url, public_headers):
        """TC_SEARCH_001 访问搜索首页，无需登录"""
        url = f"{base_url}/wx/search/index"
        resp = requests.get(url, headers=public_headers, **GLOBAL_ARGS)
        assert resp.status_code == 200
        res = resp.json()
        assert res["errno"] == 0, f"搜索首页异常：{res}"

    # GET /wx/search/helper?keyword=xxx 关键字提醒（搜索建议）（无需鉴权）
    def test_search_helper_normal(self, base_url, public_headers):
        """TC_SEARCH_002 正常关键词获取搜索联想"""
        url = f"{base_url}/wx/search/helper"
        params = {"keyword": "零食"}
        resp = requests.get(url, headers=public_headers, params=params, **GLOBAL_ARGS)
        res = resp.json()
        assert res["errno"] == 0, f"正常关键词联想异常：{res}"

    def test_search_helper_empty_keyword(self, base_url, public_headers):
        """TC_SEARCH_003 空关键词查询搜索建议，参数非法返回402"""
        url = f"{base_url}/wx/search/helper"
        params = {"keyword": ""}
        resp = requests.get(url, headers=public_headers, params=params, **GLOBAL_ARGS)
        res = resp.json()
        # 空参数校验失败，预期错误码402
        assert res["errno"] == 402, f"空关键词预期402，实际返回：{res}"
        assert res["errmsg"] == "arg0不能为空"

    # POST /wx/search/clearhistory 清除用户搜索历史（需鉴权）
    def test_search_clear_history_login(self, base_url, auth_headers):
        """TC_SEARCH_004 登录后清除个人搜索历史"""
        url = f"{base_url}/wx/search/clearhistory"
        resp = requests.post(url, headers=auth_headers, **GLOBAL_ARGS)
        res = resp.json()
        assert res["errno"] == 0, f"登录清除历史失败：{res}"

    def test_search_clear_history_no_token(self, base_url, public_headers):
        """TC_SEARCH_005 未登录清除历史，鉴权失败返回501"""
        url = f"{base_url}/wx/search/clearhistory"
        resp = requests.post(url, headers=public_headers, **GLOBAL_ARGS)
        res = resp.json()
        # 项目统一未登录错误码501
        assert res["errno"] == 501, f"未登录预期501，实际返回：{res}"