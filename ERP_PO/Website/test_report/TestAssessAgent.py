from bs4 import BeautifulSoup
from dashscope import Generation
import dashscope
import os

# Use environment variable for API key
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY', '')

def parse_test_report(report_path):
    with open(report_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 提取统计数据
    stats = soup.select_one('#total_row').find_all('td')
    total = int(stats[1].text)
    passed = int(stats[2].text)
    failed = int(stats[3].text)
    errors = int(stats[4].text)
    pass_rate = stats[5].text.split("：")[-1]

    # 提取失败/错误用例名 + 错误日志
    failed_cases = []
    for item in soup.select('.failCase .testcase'):
        name = item.text
        detail = item.find_parent('tr').find_next_sibling('tr').select_one('pre')
        log = detail.text.strip() if detail else '无'

        failed_cases.append({
            'name': name,
            'log': log
        })

    error_cases = []
    for item in soup.select('.errorCase .testcase'):
        name = item.text
        detail = item.find_parent('tr').find_next_sibling('tr').select_one('pre')
        log = detail.text.strip() if detail else '无'

        error_cases.append({
            'name': name,
            'log': log
        })

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "pass_rate": pass_rate,
        "failed_cases": failed_cases,
        "error_cases": error_cases
    }



def generate_ai_assessment(data):
    prompt = f"""
你是一个自动化测试评估专家，请根据以下测试报告数据进行分析并输出评估内容：

总用例数: {data['total']}
通过数: {data['passed']}
失败数: {data['failed']}
错误数: {data['errors']}
通过率: {data['pass_rate']}

失败用例：
{chr(10).join([f' - {c["name"]}: {c["log"]}' for c in data['failed_cases']]) if data['failed_cases'] else '无'} 

错误用例：
{chr(10).join([f' - {c["name"]}: {c["log"]}' for c in data['error_cases']]) if data['error_cases'] else '无'}

请按以下格式输出：
- 稳定性评分（百分比）
- 风险分析（主要问题点）
- 总体评价（[从覆盖率、通过率等方面评价）
- 建议（至少三条）

不要使用Markdown格式，直接输出文本。
"""

    response = Generation.call(
        model='qwen-max',
        prompt=prompt
    )

    return response.output.text


def insert_ai_assessment(report_path, ai_text):
    with open(report_path, 'r+', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

        # 创建新的 div 标签
        ai_div = soup.new_tag('div', **{'class': 'well', 'style': 'margin:20px;'})
        ai_h3 = soup.new_tag('h3')
        ai_h3.string = "AI 评估"
        ai_pre = soup.new_tag('pre')
        ai_pre.string = ai_text

        ai_div.append(ai_h3)
        ai_div.append(ai_pre)

        # 找到 report 表格并插入 AI 内容
        report_table = soup.select_one('#result_table')
        if report_table:
            report_table.insert_before(ai_div)

        # 将修改后的内容写回文件
        f.seek(0)
        f.write(str(soup))
        f.truncate()


if __name__ == '__main__':
    report_file = './test_report/your_report.html'

    # 1. 解析测试报告
    report_data = parse_test_report(report_file)

    # 2. 生成 AI 评估内容
    ai_evaluation = generate_ai_assessment(report_data)

    # 3. 插入 AI 内容到 HTML 中
    insert_ai_assessment(report_file, ai_evaluation)

    print("AI 评估已成功插入到测试报告中。")
