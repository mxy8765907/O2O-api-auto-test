import pytest
import requests
import base64

# ====================== 全局配置 ======================
BASE_URL = "https://dciit.cn:8013"
LOGIN_USERNAME = "user1234"
LOGIN_PASSWORD_RAW = "user1234"

COMMON_HEADERS = {
    "Content-Type": "application/json;charset=utf-8"
}

# ====================== 基础夹具 ======================
@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def public_headers():
    return COMMON_HEADERS

# ====================== 登录夹具 ======================
@pytest.fixture(scope="session")
def login_token(base_url):
    login_url = f"{base_url}/wx/auth/login"
    pwd_bytes = LOGIN_PASSWORD_RAW.encode("utf-8")
    pwd_b64 = base64.b64encode(pwd_bytes).decode("utf-8")
    login_body = {
        "username": LOGIN_USERNAME,
        "password": pwd_b64
    }
    resp = requests.post(
        url=login_url,
        json=login_body,
        headers=COMMON_HEADERS,
        #不要认证和代理
        verify=False,
        proxies={}
    )
    res_json = resp.json()
    assert res_json["errno"] == 0, f"登录失败，返回信息：{res_json['errmsg']}"
    token = res_json["data"]["token"]

    yield token

    # 会话后置：退出登录
    logout_url = f"{base_url}/wx/auth/logout"
    logout_headers = {**COMMON_HEADERS, "Sgave-Mall-Token": token}
    requests.post(url=logout_url, headers=logout_headers, verify=False, proxies={})
    print("\n测试会话结束，执行退出登录")

# ====================== 鉴权请求头夹具 ======================
@pytest.fixture(scope="session")
def auth_headers(login_token):
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Sgave-Mall-Token": login_token
    }
    return headers

# ====================== 获取优惠劵 ======================
COUPON_CONFIG = {
    "couponId": 1004,
    "userCouponId": 3108
}

@pytest.fixture(scope="session")
def usable_coupon():
    return COUPON_CONFIG


