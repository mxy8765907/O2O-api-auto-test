# O2O-api-auto-test
O2O线上电商商城接口自动化测试项目

## 📌 项目简介
针对O2O电商商城购物车、订单、售后等23个核心接口开展接口功能测试与自动化回归，使用Postman调试接口，基于Python+requests+pytest搭建自动化测试框架，Allure生成可视化报告，接入Jenkins CI实现版本迭代自动回归。

## 🛠 技术栈
- 编程语言：Python3
- 自动化库：requests + pytest
- 测试工具：Postman、Allure、Jenkins
- 报告：Allure测试可视化报告

## 📁 目录结构
├── cases/                # pytest自动化测试脚本、用例
├── docs/                 # 测试用例、缺陷报告、思维导图、答辩文档
├── jenkins/              # Jenkins持续集成截图、构建记录
├── postman_collection/   # Postman接口集合导出json
├── report/               # Allure可视化测试报告
├── .gitignore
└── README.md

