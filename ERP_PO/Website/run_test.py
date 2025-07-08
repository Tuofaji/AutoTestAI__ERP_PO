import time
import unittest
from HTMLTestRunner import HTMLTestRunner
from ERP_PO.Website.test_case.test_add import Test
from ERP_PO.Website.test_report.TestAssessAgent import (
    parse_test_report,
    generate_ai_assessment, insert_ai_assessment)

print("开始测试")

report_dir = "./test_report"
now = time.strftime("%H_%M_%S")
report_name = '/' + now + "result.html"
report_path = report_dir + report_name

suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test)

with open(report_path,'wb') as f:
    runner = HTMLTestRunner(stream=f,title="ERP Test",description="erp test",tester="1186")
    runner.run(suite)

print("风险评估智能体正在检查报告中。。。")

report_data = parse_test_report(report_path)
ai_evaluation = generate_ai_assessment(report_data)
insert_ai_assessment(report_path, ai_evaluation)

print("AI 评估已成功写入到测试报告中。")
print("测试结束")