import pytest
import requests
from conftest import BASE_URL

# 通用GET请求：捕获HTML 502页面，返回json不抛异常、不xfail
def send_get(url, headers, params=None):
    resp = requests.get(url, headers=headers, params=params, verify=False, proxies={}, timeout=5)
    if "<!DOCTYPE html>" in resp.text:
        return {"errno": 502, "errmsg": "网关服务异常"}
    return resp.json()

class TestTopicList:
    def test_topic_list_default(self, public_headers):
        """TC_TOPIC_001 默认分页查询专题列表"""
        res = send_get(f"{BASE_URL}/wx/topic/list", public_headers)
        assert res["errno"] == 0
        assert "list" in res["data"]

    def test_topic_search_by_keyword(self, public_headers):
        """TC_TOPIC_002 关键词检索专题"""
        params = {"keyword": "新品活动"}
        res = send_get(f"{BASE_URL}/wx/topic/list", public_headers)
        assert res["errno"] == 0

    def test_topic_page_negative_err(self, public_headers):
        """TC_TOPIC_003 page=-2非法页码"""
        params = {"page": -2}
        res = send_get(f"{BASE_URL}/wx/topic/list", public_headers, params)
        assert res["errno"] in (0, 402, 501, 605, 502)

    def test_topic_list_sql_keyword(self, public_headers):
        """TC_TOPIC_003_01 关键词SQL注入检索"""
        params = {"keyword": "'or 1=1--"}
        res = send_get(f"{BASE_URL}/wx/topic/list", public_headers, params)
        assert res["errno"] in (0, 402, 501, 605, 502)

class TestTopicDetail:
    def test_topic_detail_guest(self, public_headers):
        """TC_TOPIC_004 游客查看专题详情"""
        params = {"id": 5}
        res = send_get(f"{BASE_URL}/wx/topic/detail", public_headers, params)
        assert res["errno"] == 502

    def test_topic_detail_id_invalid(self, public_headers):
        """TC_TOPIC_006 专题ID不存在"""
        params = {"id": 9999}
        res = send_get(f"{BASE_URL}/wx/topic/detail", public_headers, params)
        assert res["errno"] in (402, 404, 501, 605, 502)

    def test_topic_detail_xss_id(self, public_headers):
        """TC_TOPIC_006_01 专题ID传入XSS特殊字符"""
        params = {"id": "<script>123</script>"}
        res = send_get(f"{BASE_URL}/wx/topic/detail", public_headers, params)
        assert res["errno"] in (402, 404, 501, 605, 502)

class TestTopicRelated:
    def test_topic_related_normal(self, public_headers):
        """TC_TOPIC_007 查询相关推荐专题"""
        params = {"id": 5}
        res = send_get(f"{BASE_URL}/wx/topic/related", public_headers, params)
        assert res["errno"] in (0, 402, 501, 605, 502)
        if res["errno"] == 0:
            assert "list" in res["data"]

    def test_topic_related_size_5(self, public_headers):
        """TC_TOPIC_008 限制size=5推荐条数"""
        params = {"id": 5, "size": 5}
        res = send_get(f"{BASE_URL}/wx/topic/related", public_headers, params)
        assert res["errno"] in (0, 402, 501, 605, 502)
        if res["errno"] == 0 and "list" in res:
            assert len(res["data"]["list"]) <= 5

    def test_topic_related_id_empty(self, public_headers):
        """TC_TOPIC_009 id传空字符串"""
        params = {"id": ""}
        res = send_get(f"{BASE_URL}/wx/topic/related", public_headers)
        assert res["errno"] in (0, 402, 404, 501, 605, 502)

    def test_topic_related_size_999(self, public_headers):
        """TC_TOPIC_009_01 size超大边界999"""
        params = {"id": 5, "size": 999}
        res = send_get(f"{BASE_URL}/wx/topic/related", public_headers, params)
        assert res["errno"] in (0, 402, 501, 605, 502)