# AutoTest+AI ERP_PO 自动化测试项目

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue)
![PaddleOCR](https://img.shields.io/badge/PaddleOCR-latest-blue)
![Selenium](https://img.shields.io/badge/Selenium-latest-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

[English](#english) | [中文](#chinese)

---

<a id="english"></a>
## 🌟 Project Introduction

This project is an automated testing platform for ERP (Enterprise Resource Planning) management systems. Based on Python and Page Object Model (PO), it integrates tools such as PaddleOCR, PyAutoGUI, and Selenium to implement automated UI testing, OCR recognition with auto-clicking, data-driven testing, and more.

### Main Features

- Automated testing of various pages and functions in ERP management platforms
- OCR-based UI element recognition and auto-clicking (with Chinese support)
- Data-driven testing (supports CSV data reading and caching)
- Automatic screenshot capture and test report generation
- Supports custom test case extensions

## 🚀 Quick Start

### Prerequisites

- Python 3.12
- Key Dependencies:
  - [paddleocr](https://github.com/PaddlePaddle/PaddleOCR)
  - [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
  - [pillow](https://python-pillow.org/)
  - [selenium](https://www.selenium.dev/)
  - [paddlepaddle](https://www.paddlepaddle.org.cn/) (can be extended to GPU version)
  - [dashscope](https://help.aliyun.com/document_detail/611472.html) (for AI assessment)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/AutoTestAI.git
cd AutoTestAI

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

- Run test cases directly (without generating test reports):
  ```bash
  python -m ERP_PO.Website.test_case.test_add
  ```
- Run using the test entry script:
  ```bash
  python -m ERP_PO.Website.run_test
  ```

## 📂 Directory Structure

```
AutoTestAI/
  └─ ERP_PO/
      ├─ driver/                # Driver related code
      ├─ Website/
      │   ├─ run_test.py        # Test entry script
      │   ├─ test_case/         # Test cases
      │   │   ├─ model/         # Common methods, utilities
      │   │   └─ page_object/   # Page object encapsulation
      │   ├─ test_data/         # Test data & data management
      │   └─ test_report/       # Test reports & screenshots
      └─ ReadMe.md              # Project documentation
```

## 📝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<a id="chinese"></a>
## 🌟 项目简介

本项目是我在准备参加省职业技能大赛期间开发的项目，它是针对 ERP(资源协同)管理系统 的自动化测试平台，基于 Python+PO模式 开发，集成了 PaddleOCR、PyAutoGUI、Selenium 等工具，实现了自动化 UI 测试、OCR 识别与自动点击、数据驱动测试等功能。

### 项目背景
1. 为什么需要自动化测试？
   - **效率提升**： 在ERP这样庞大且功能频繁迭代的系统中，重复的手工回归测试耗时耗力，是效率的瓶颈。自动化测试能够将这些重复、繁琐的测试任务交给机器执行，显著缩短测试周期（如我们实际应用中减少了约70%的执行时间），释放测试人员精力去探索更复杂的场景和边界测试。
   - **质量保障与一致性**： 人工测试难免因疲劳或疏忽导致遗漏或误判。自动化测试脚本一旦编写完成并验证无误，每次执行都能保证完全相同的步骤和验证点，提供稳定、可靠、可重复的测试结果，极大提升测试覆盖率和软件质量的置信度。
   - **持续集成/持续交付(CI/CD)的基石**： 敏捷开发要求快速迭代、快速反馈。自动化测试是嵌入CI/CD流水线的关键环节，能在每次代码提交后快速运行，第一时间发现引入的缺陷，实现"快速失败，快速修复"，加速交付流程。
   - **覆盖复杂场景与回归测试**： 对于ERP系统中涉及多步骤流程（如我们演示的新增商品品牌 -> 新增商品单位 -> 新增商品分类 -> 新增商品）、数据依赖性强、或者需要大量数据组合验证的场景，自动化测试能够轻松、准确且高效地完成，这是手工测试难以企及的。
   - **探索性测试的赋能**： 将基础、重复的测试自动化后，测试工程师可以腾出更多时间进行更有价值的探索性测试、用户体验测试、性能和安全测试等，实现测试价值的最大化。

2. 理解了自动化测试的必要性，我们还需要一个健壮、可维护、可扩展的框架来支撑它。这正是我们选择PO模式作为核心架构的原因：
   - **代码复用性**： 通用的页面操作（如登录、导航、元素查找）被封装在基础页面类（如我们的基础页面类）和具体的页面类方法中。测试用例（test_add.py）只需要调用这些封装好的方法（如LoginPage.test_login(driver,username, password), AddGoods.test_add_brand(driver,brand_name,...)），避免代码重复，使测试用例本身更加简洁、专注于业务逻辑和验证。
   - **提高可读性**： 测试用例使用页面对象提供的业务语义化方法（如test_add_goods(),click_element_by_text()），读起来更像是在描述用户操作流程（"在商品管理页面，点击新增按钮，输入商品名称..."），而非充斥着技术细节（driver.find_element(By.ID, 'addBtn').click()）。这使得代码更易于理解、评审和维护。
   - **增强健壮性**： 封装操作时，可以在页面对象内部加入必要的等待、重试等健壮性处理逻辑（如我们处理动态下拉列表时用到的图像识别技术），对外提供更稳定可靠的接口，提升测试脚本的稳定性。
   - **支持协作**： 清晰的层次结构（页面对象层 vs 测试用例层）方便不同角色（如页面对象开发者、测试用例设计者）并行工作，也方便团队成员的协作和理解。

### 主要功能
- 自动化测试 ERP(资源协同)管理平台 的各类页面与功能
- 支持 OCR 的界面元素识别与自动点击（支持中文）
- 数据驱动测试（支持 CSV 数据读取与缓存）
- 自动截图、测试报告生成
- 支持自定义测试用例扩展

## 🚀 快速开始

### 依赖环境
- Python 3.12
- 主要依赖包：
  - [paddleocr](https://github.com/PaddlePaddle/PaddleOCR)
  - [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
  - [pillow](https://python-pillow.org/)
  - [selenium](https://www.selenium.dev/)
  - [paddlepaddle](https://www.paddlepaddle.org.cn/)（可扩展至 GPU 版本）
  - [dashscope](https://help.aliyun.com/document_detail/611472.html)（用于AI评估）

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/AutoTestAI.git
cd AutoTestAI

# 安装依赖
pip install -r requirements.txt
```

### 运行测试
- 直接运行测试用例（不生成测试报告）：
  ```bash
  python -m ERP_PO.Website.test_case.test_add
  ```
- 通过测试入口脚本运行：
  ```bash
  python -m ERP_PO.Website.run_test
  ```

## 📂 目录结构
```
AutoTestAI/
  └─ ERP_PO/
      ├─ driver/                # 驱动相关代码
      ├─ Website/
      │   ├─ run_test.py        # 测试入口脚本
      │   ├─ test_case/         # 测试用例
      │   │   ├─ model/         # 公共方法、工具
      │   │   └─ page_object/   # 页面对象封装
      │   ├─ test_data/         # 测试数据与数据管理
      │   └─ test_report/       # 测试报告与截图
      └─ ReadMe.md              # 项目说明
```

## 📝 贡献

欢迎提交贡献！请随时提交 Pull Request。

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 LICENSE 文件。
