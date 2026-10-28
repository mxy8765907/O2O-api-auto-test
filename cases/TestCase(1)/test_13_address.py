
import requests
import warnings
warnings.filterwarnings("ignore")
class TestAddress:

    url_list = "/wx/address/list"
    url_detail = "/wx/address/detail"
    url_save = "/wx/address/save"
    url_delete = "/wx/address/delete"
    url_region = "/wx/address/region"

    # TC_ADDR_001 登录用户查询地址列表
    def test_address_list_normal(self, base_url, auth_headers):
        full_url = base_url + self.url_list
        res = requests.get(url=full_url, headers=auth_headers, verify=False, proxies={})
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 0
        assert "list" in data["data"]

    # TC_ADDR_002 未登录查询地址列表
    def test_address_list_no_token(self, base_url, public_headers):
        full_url = base_url + self.url_list
        res = requests.get(url=full_url, headers=public_headers, verify=False, proxies={})
        data = res.json()
        assert data["errno"] == 401

    # TC_ADDR_010 查询地址详情正常
    def test_address_detail_normal(self, base_url, auth_headers):
        full_url = base_url + self.url_detail
        params = {"id": 10}
        res = requests.get(url=full_url, headers=auth_headers, params=params, verify=False, proxies={})
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 0

    # TC_ADDR_011 id不存在查询详情
    def test_address_detail_id_not_exist(self, base_url, auth_headers):
        full_url = base_url + self.url_detail
        params = {"id": 999999}
        res = requests.get(url=full_url, headers=auth_headers, params=params, verify=False, proxies={})
        data = res.json()
        assert data["errno"] == 402

    # TC_ADDR_020 新增收货地址
    def test_address_save_add(self, base_url, auth_headers):
        full_url = base_url + self.url_save
        body = {
            "id": 0,
            "name": "张三",
            "mobile": "13800138000",
            "province": "四川省",
            "city": "成都市",
            "area": "郫都区",
            "address": "科技园1号楼",
            "isDefault": True
        }
        res = requests.post(url=full_url, headers=auth_headers, json=body, verify=False, proxies={})
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 0
        assert "id" in data["data"]

    # TC_ADDR_021 手机号格式错误新增地址
    def test_address_save_mobile_err(self, base_url, auth_headers):
        full_url = base_url + self.url_save
        body = {
            "id": 0,
            "name": "张三",
            "mobile": "123",
            "province": "四川",
            "city": "成都",
            "area": "郫都",
            "address": "xxx",
            "isDefault": False
        }
        res = requests.post(url=full_url, headers=auth_headers, json=body, verify=False, proxies={})
        data = res.json()
        assert data["errno"] == 402

    # TC_ADDR_030 正常删除地址
    def test_address_delete_normal(self, base_url, auth_headers):
        full_url = base_url + self.url_delete
        body = {"id": 10}
        res = requests.post(url=full_url, headers=auth_headers, json=body, verify=False, proxies={})
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 0

    # TC_ADDR_031 未登录删除地址
    def test_address_delete_no_token(self, base_url, public_headers):
        full_url = base_url + self.url_delete
        body = {"id": 10}
        res = requests.post(url=full_url, headers=public_headers, json=body, verify=False, proxies={})
        data = res.json()
        assert data["errno"] == 401

    # TC_ADDR_040 获取省份列表 pid=0
    def test_address_region_province(self, base_url, public_headers):
        full_url = base_url + self.url_region
        params = {"pid": 0}
        res = requests.get(url=full_url, headers=public_headers, params=params, verify=False, proxies={})
        data = res.json()
        assert res.status_code == 200
        assert data["errno"] == 0