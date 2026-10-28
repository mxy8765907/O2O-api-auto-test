# 交易核心模块接口自动化项目
负责人：毛晓雨
覆盖模块：购物车Cart、订单Order、售后Aftersale（共23个高复杂度接口）

## 目录说明
1. .venv1
Python虚拟环境，用于隔离项目依赖，无需手动修改

2. testcase/conf 全局配置目录
- conftest.py：pytest全局夹具，封装登录获取Token鉴权、通用请求方法
- pytest.ini：pytest运行配置，控制用例执行、HTML测试报告输出
- requirements.txt：项目第三方依赖清单，一键安装所有库

3. testcase 业务自动化脚本
- test_07_cart.py：购物车模块全接口自动化用例
- test_08_order.py：订单下单、支付、取消、确认收货等流程接口
- test_09_aftersale.py：退款、售后申诉、售后查询接口

4. Jenkinsfile（后续新增）
CI流水线脚本，实现自动拉取代码、安装依赖、执行用例、生成测试报告

## 本地运行命令
# 1. 安装依赖
pip install -r testcase/conf/requirements.txt
# 2. 执行全部自动化用例，生成HTML报告
pytest testcase/ -v --html=report.html