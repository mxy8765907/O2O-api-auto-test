# O2O-api-auto-test
O2O线上电商商城接口自动化测试项目

## 📌 项目简介
针对O2O电商商城购物车、订单、售后等23个核心接口开展接口功能测试与自动化回归，使用Postman调试接口，基于Python+requests+pytest搭建自动化测试框架，Allure生成可视化报告，接入Jenkins CI实现版本迭代自动回归。

## 🛠️ 技术栈
- 编程语言：Python3
- 自动化库：requests + pytest
- 测试工具：Postman、Allure、Jenkins
- 报告：Allure测试可视化报告

## 📂 目录结构
- cases/：pytest 自动化测试脚本、用例
- docs/：测试用例、缺陷报告、思维导图、答辩文档
- jenkins/：Jenkins 持续集成截图、构建记录
- postman_collection/：Postman 接口集合导出 json
- report/：Allure 可视化测试报告
- .gitignore
- README.md

## 🚀 项目运行说明
```bash
1. 环境准备：Python3，安装依赖
pip install pytest requests allure-pytest
2.执行自动化用例
pytest cases/ --alluredir=report/tmp
3.本地启动、查看Allure报告
allure serve report/tmp


