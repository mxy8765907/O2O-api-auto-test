import requests

class TestIssueList:
    url_path = "/wx/issue/list"

    # TC_ISSUE_001 无筛选条件正常查询
    def test_issue_normal_no_param(self, base_url, public_headers):
        full_url = base_url + self.url_path
        res = requests.get(url=full_url, headers=public_headers, verify=False, proxies={})
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 0
        assert "list" in data["data"]

    # TC_ISSUE_002 关键词精准搜索
    def test_issue_search_keyword(self, base_url, public_headers):
        full_url = base_url + self.url_path
        params = {"question": "登录", "page": 1, "size": 10}
        res = requests.get(url=full_url, headers=public_headers, params=params, verify=False, proxies={})
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 0

    # TC_ISSUE_003 正常分页查询
    def test_issue_page_normal(self, base_url, public_headers):
        full_url = base_url + self.url_path
        params = {"page": 2, "size": 5}
        res = requests.get(url=full_url, headers=public_headers, params=params, verify=False, proxies={})
        assert res.status_code == 200

    # TC_ISSUE_005 无匹配关键词搜索
    def test_issue_search_no_match(self, base_url, public_headers):
        full_url = base_url + self.url_path
        params = {"question": "不存在的问题123456789", "page": 1, "size": 10}
        res = requests.get(url=full_url, headers=public_headers, params=params, verify=False, proxies={})
        data = res.json()
        assert data["data"]["list"] == []

    # TC_ISSUE_006 page=0边界最小值
    def test_issue_page_min_bound(self, base_url, public_headers):
        full_url = base_url + self.url_path
        params = {"page": 0, "size": 10}
        res = requests.get(url=full_url, headers=public_headers, params=params, verify=False, proxies={})
        assert res.status_code == 200

    # TC_ISSUE_010 size=0非法边界（后端无拦截，实际200）
    def test_issue_size_zero(self, base_url, public_headers):
        full_url = base_url + self.url_path
        params = {"page": 1, "size": 0}
        res = requests.get(url=full_url, headers=public_headers, params=params, verify=False, proxies={})
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 0

    # TC_ISSUE_014 page负数异常（后端无拦截，实际200）
    def test_issue_page_negative(self, base_url, public_headers):
        full_url = base_url + self.url_path
        params = {"page": -1, "size": 10}
        res = requests.get(url=full_url, headers=public_headers, params=params, verify=False, proxies={})
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 0

    # TC_ISSUE_017 SQL注入安全测试（无过滤，存在安全缺陷）
    def test_issue_sql_inject(self, base_url, public_headers):
        full_url = base_url + self.url_path
        params = {"question": "'or 1=1 --", "page": 1, "size": 10}
        res = requests.get(url=full_url, headers=public_headers, params=params, verify=False, proxies={})
        data = res.json()
        assert data["errno"] == 0

    # TC_ISSUE_018 XSS注入安全测试（无过滤，存在安全缺陷）
    def test_issue_xss_inject(self, base_url, public_headers):
        full_url = base_url + self.url_path
        params = {"question": "<script>alert(1)</script>", "page": 1, "size": 10}
        res = requests.get(url=full_url, headers=public_headers, params=params, verify=False, proxies={})
        data = res.json()
        assert data["errno"] == 0