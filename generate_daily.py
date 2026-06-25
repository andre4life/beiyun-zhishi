#!/usr/bin/env python3
"""
备孕知识 每日自动生成器（GitHub Actions用）
用法: python generate_daily.py [--date YYYY-MM-DD]
不传日期则自动生成今天的。
如果今天的文件已存在→跳过。
"""
import sys, os, json, html
from datetime import datetime, date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_BANK = os.path.join(SCRIPT_DIR, "content_bank.json")
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "template.html")
DATA_JSON = os.path.join(SCRIPT_DIR, "data.json")

def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()

def load_content_bank():
    with open(CONTENT_BANK, "r", encoding="utf-8") as f:
        return json.load(f)

def load_data_json():
    if os.path.exists(DATA_JSON):
        with open(DATA_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data_json(data):
    with open(DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def pick_topic(date_str, content_bank):
    """根据日期确定性选话题，每天不同"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    day_of_year = dt.timetuple().tm_yday
    idx = day_of_year % len(content_bank)
    return content_bank[idx]

def generate(date_str):
    output_file = os.path.join(SCRIPT_DIR, f"by_{date_str}.html")
    index_file = os.path.join(SCRIPT_DIR, "index.html")

    # 如果今天的文件已经存在，跳过
    if os.path.exists(output_file):
        print(f"[SKIP] {output_file} 已存在，跳过生成")
        return

    template = load_template()
    content_bank = load_content_bank()
    topic_data = pick_topic(date_str, content_bank)

    # 填充模板
    html_content = template.replace("{{DATE}}", date_str)
    html_content = html_content.replace("{{TOPIC}}", html.escape(topic_data["topic"]))
    html_content = html_content.replace("{{KNOWLEDGE}}", topic_data["knowledge"])
    html_content = html_content.replace("{{TIPS}}", topic_data["tips"])
    html_content = html_content.replace("{{NUTRITION}}", topic_data["nutrition"])
    html_content = html_content.replace("{{SUMMARY}}", topic_data["summary"])

    # 保存
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 更新 data.json
    data = load_data_json()
    data.append({
        "date": date_str,
        "topic": topic_data["topic"],
        "summary": topic_data["summary"].replace('<span class="highlight">', '').replace('</span>', ''),
        "file": f"by_{date_str}.html"
    })
    save_data_json(data)

    print(f"[GENERATED] {output_file}")
    print(f"[GENERATED] {index_file}")
    print(f"[DATA] data.json 已更新 (共 {len(data)} 条)")

if __name__ == "__main__":
    arg_date = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--date" and i + 1 < len(sys.argv):
            arg_date = sys.argv[i + 1]
            i += 2
        else:
            arg_date = sys.argv[i]
            i += 1
    if arg_date is None:
        arg_date = date.today().strftime("%Y-%m-%d")
    generate(arg_date)
