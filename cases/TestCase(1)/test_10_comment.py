import pytest
import requests
import warnings
warnings.filterwarnings("ignore")

# 全局统一请求参数，全项目复用
GLOBAL_ARGS = {"verify": False, "proxies": {}}


class TestComment:
    url_list = "/wx/comment/list"
    url_count = "/wx/comment/count"
    url_post = "/wx/comment/post"

    # TC_COMMENT_001 游客正常查询商品评论列表
    def test_comment_list_normal_guest(self, base_url, public_headers):
        full_url = base_url + self.url_list
        params = {"type": 0, "valueId": 1001, "page": 1, "limit": 10, "showType": 0}
        res = requests.get(url=full_url, headers=public_headers, params=params, **GLOBAL_ARGS)
        data = res.json()
        assert res.status_code == 200, f"状态码异常：{res.status_code}"
        assert data["errno"] == 0, f"查询评论列表失败：{data}"
        assert "list" in data["data"], "返回data无list数组字段"

    # TC_COMMENT_002 仅查看带图评论 showType=1
    def test_comment_list_only_pic(self, base_url, public_headers):
        full_url = base_url + self.url_list
        params = {"type": 0, "valueId": 1001, "page": 1, "limit": 10, "showType": 1}
        res = requests.get(url=full_url, headers=public_headers, params=params, **GLOBAL_ARGS)
        data = res.json()
        assert res.status_code == 200, f"状态码异常：{res.status_code}"
        assert data["errno"] == 0, f"仅看图评论查询失败：{data}"

    # TC_COMMENT_003 page传非数字非法参数
    def test_comment_list_page_illegal(self, base_url, public_headers):
        full_url = base_url + self.url_list
        params = {"type": 0, "valueId": 1001, "page": "abc", "limit": 10}
        res = requests.get(url=full_url, headers=public_headers, params=params, **GLOBAL_ARGS)
        data = res.json()
        assert res.status_code == 400, f"非法分页状态码异常：{res.status_code}"
        assert data["errno"] == 402, f"非法分页预期402，实际返回：{data}"

    # TC_COMMENT_004 正常查询商品评论总数
    def test_comment_count_normal(self, base_url, public_headers):
        full_url = base_url + self.url_count
        params = {"type": 0, "valueId": 1001}
        res = requests.get(url=full_url, headers=public_headers, params=params, **GLOBAL_ARGS)
        data = res.json()
        assert res.status_code == 200, f"状态码异常：{res.status_code}"
        assert data["errno"] == 0, f"评论总数查询失败：{data}"
        assert "total" in data["data"], "返回data无total统计字段"

    # TC_COMMENT_005 查询不存在商品评论统计
    def test_comment_count_goods_not_exist(self, base_url, public_headers):
        full_url = base_url + self.url_count
        params = {"type": 0, "valueId": 999999}
        res = requests.get(url=full_url, headers=public_headers, params=params, **GLOBAL_ARGS)
        data = res.json()
        assert res.status_code == 200, f"状态码异常：{res.status_code}"
        assert data["errno"] == 0, f"不存在商品评论统计返回异常：{data}"

    # TC_COMMENT_006 登录用户正常发布评论
    def test_comment_post_normal(self, base_url, auth_headers):
        full_url = base_url + self.url_post
        body = {
            "valueId": 1001,
            "type": 0,
            "content": "商品做工精细，推荐购买",
            "star": 5,
            "hasPicture": False,
            "picUrls": []
        }
        res = requests.post(url=full_url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        assert res.status_code == 200, f"状态码异常：{res.status_code}"
        assert data["errno"] == 0, f"正常发布评论失败：{data}"
        assert "commentId" in data["data"], "返回data无评论ID字段"

    # TC_COMMENT_007 未登录提交评论
    def test_comment_post_no_token(self, base_url, public_headers):
        full_url = base_url + self.url_post
        body = {"valueId": 1001, "type": 0, "content": "测试评价", "star": 5}
        res = requests.post(url=full_url, headers=public_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        # 项目统一未登录错误码501，替换原401
        assert data["errno"] == 501, f"未登录预期501，实际返回：{data}"

    # TC_COMMENT_008 过期token提交评论
    # 注释：conftest无expire_auth_headers夹具，启用需新增过期token夹具
    # def test_comment_post_expire_token(self, base_url, expire_auth_headers):
    #     full_url = base_url + self.url_post
    #     body = {"valueId": 1001, "type": 0, "content": "测试评价", "star": 5}
    #     res = requests.post(url=full_url, headers=expire_auth_headers, json=body,** GLOBAL_ARGS)
    #     data = res.json()
    #     assert data["errno"] == 501, f"过期token预期501，实际返回：{data}"

    # TC_COMMENT_009 star评分非法9分
    def test_comment_post_star_illegal(self, base_url, auth_headers):
        full_url = base_url + self.url_post
        body = {"valueId": 1001, "type": 0, "content": "测试", "star": 9}
        res = requests.post(url=full_url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        assert res.status_code == 400, f"非法评分状态码异常：{res.status_code}"
        assert data["errno"] == 402, f"非法评分预期402，实际返回：{data}"

    # TC_COMMENT_010 content为空提交评论
    def test_comment_post_miss_content(self, base_url, auth_headers):
        full_url = base_url + self.url_post
        body = {"valueId": 1001, "type": 0, "content": "", "star": 5}
        res = requests.post(url=full_url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        assert data["errno"] == 402, f"空内容预期402，实际返回：{data}"

    # TC_COMMENT_011 content携带SQL注入
    def test_comment_post_sql_inject(self, base_url, auth_headers):
        full_url = base_url + self.url_post
        body = {"valueId": 1001, "type": 0, "content": "1' or 1=1 --", "star": 5}
        res = requests.post(url=full_url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        assert data["errno"] == 0, f"SQL注入评论提交异常：{data}"

    # TC_COMMENT_012 content携带XSS脚本
    def test_comment_post_xss_inject(self, base_url, auth_headers):
        full_url = base_url + self.url_post
        body = {"valueId": 1001, "type": 0, "content": "<script>alert(1)</script>", "star": 5}
        res = requests.post(url=full_url, headers=auth_headers, json=body, **GLOBAL_ARGS)
        data = res.json()
        assert data["errno"] == 0, f"XSS脚本评论提交异常：{data}"