import pytest
import requests
import warnings
warnings.filterwarnings("ignore")

# 全局公共请求参数，统一复用
GLOBAL_ARGS = {"verify": False, "proxies": {}}


class TestFeedbackSubmit:
    url_path = "/wx/feedback/submit"

    # TC_FEEDBACK_001 合法参数正常提交建议类反馈
    def test_feedback_normal_suggest(self, base_url, auth_headers):
        full_url = base_url + self.url_path
        body = {
            "feedType": 0,
            "content": "建议优化登录页面加载速度",
            "mobile": "13800138000"
        }
        res = requests.post(url=full_url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        assert res.status_code == 200, f"接口状态码异常：{res.status_code}"
        assert data["errno"] == 0, f"正常提交反馈失败：{data}"

    # TC_FEEDBACK_005 未携带token直接提交反馈
    def test_feedback_no_token(self, base_url, public_headers):
        full_url = base_url + self.url_path
        body = {
            "feedType": 0,
            "content": "建议优化登录页面加载速度",
            "mobile": "13800138000"
        }
        res = requests.post(url=full_url, headers=public_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 501, f"未登录预期501，实际返回：{data}"

    # TC_FEEDBACK_007 缺失content必填参数
    def test_feedback_miss_content(self, base_url, auth_headers):
        full_url = base_url + self.url_path
        body = {"feedType": 0, "mobile": "13800138000"}
        res = requests.post(url=full_url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        assert data["errno"] == 401, f"缺失content参数预期401，实际返回：{data}"

    # TC_FEEDBACK_010 feedType非法值999
    def test_feedback_feedtype_illegal(self, base_url, auth_headers):
        full_url = base_url + self.url_path
        body = {"feedType": 999, "content": "测试内容", "mobile": "13800138000"}
        res = requests.post(url=full_url, headers=auth_headers, json=body,** GLOBAL_ARGS)
        data = res.json()
        # 后端无feedType范围校验，非法值可正常提交，返回errno=0
        assert data["errno"] == 0, f"非法feedType提交返回异常：{data}"

    # TC_FEEDBACK_021 content参数SQL注入
    def test_feedback_content_sql(self, base_url, auth_headers):
        full_url = base_url + self.url_path
        body = {"feedType": 0, "content": "'or 1=1 --", "mobile": "13800138000"}
        res = requests.post(url=full_url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        assert data["errno"] == 0, f"SQL注入场景提交异常：{data}"

    # TC_FEEDBACK_022 content参数XSS注入
    def test_feedback_content_xss(self, base_url, auth_headers):
        full_url = base_url + self.url_path
        body = {"feedType": 0, "content": "<script>alert('hack')</script>", "mobile": "13800138000"}
        res = requests.post(url=full_url, headers=auth_headers, json=body,** GLOBAL_ARGS)
        data = res.json()
        assert data["errno"] == 0, f"XSS注入场景提交异常：{data}"