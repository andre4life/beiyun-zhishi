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

def _fingerprint(topic):
    """话题指纹：去掉标点/空白后取前15字，用于识别「换汤不换药」的重复选题"""
    import re
    return re.sub(r"[^\w\u4e00-\u9fff]", "", topic or "")[:15]


def _days_between(d1, d2):
    """d2 - d1，返回天数；格式错误返回 None"""
    try:
        a = datetime.strptime(d1, "%Y-%m-%d")
        b = datetime.strptime(d2, "%Y-%m-%d")
        return (b - a).days
    except Exception:
        return None


def pick_topic(date_str, content_bank, history=None):
    """选话题：优先避开历史已用过，且同一天多次运行结果一致。

    规则（按优先级）：
    1. 从未在 history 出现过的条目优先；
    2. 若条目已全部用过，选「最久未使用」的那条（最后一次出现的日期最早）；
    Actions 一天两跑也不会漂移（用 day_of_year 做确定性偏移）。
    """
    history = history or []
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    day_of_year = dt.timetuple().tm_yday

    last_used = {}
    for rec in history:
        fp = _fingerprint(rec.get("topic", ""))
        d = rec.get("date", "")
        if fp and (fp not in last_used or d > last_used[fp]):
            last_used[fp] = d

    unused = [i for i, c in enumerate(content_bank)
              if _fingerprint(c.get("topic", "")) not in last_used]
    if unused:
        return content_bank[unused[day_of_year % len(unused)]]

    n = len(content_bank)
    ordered = sorted(range(n),
                     key=lambda i: (last_used.get(_fingerprint(content_bank[i].get("topic", "")), ""), i))
    return content_bank[ordered[0]]

def generate(date_str):
    output_file = os.path.join(SCRIPT_DIR, f"by_{date_str}.html")
    index_file = os.path.join(SCRIPT_DIR, "index.html")

    # 如果今天的文件已经存在，跳过
    if os.path.exists(output_file):
        print(f"[SKIP] {output_file} 已存在，跳过生成")
        return

    template = load_template()
    content_bank = load_content_bank()
    history = load_data_json()
    topic_data = pick_topic(date_str, content_bank, history)

    # 兜底：万一仍撞上最近 60 天内用过的话题，顺延到下一条未撞车的
    recent = {_fingerprint(r.get("topic", ""))
              for r in history if _days_between(r.get("date", ""), date_str) is not None
              and 0 <= _days_between(r.get("date", ""), date_str) < 60}
    if _fingerprint(topic_data.get("topic", "")) in recent:
        for cand in content_bank:
            if _fingerprint(cand.get("topic", "")) not in recent:
                print(f"[DEDUP] 避开近期重复：{topic_data['topic'][:20]}… → 改选 {cand['topic'][:20]}…")
                topic_data = cand
                break

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

    # 更新 data.json（同日记录已存在则不重复追加）
    data = history
    if any(r.get("date") == date_str for r in data):
        print(f"[SKIP] data.json 已有 {date_str} 记录，不重复追加")
    else:
        import re
        data.append({
            "date": date_str,
            "topic": topic_data["topic"],
            "summary": re.sub(r"<[^>]+>", "", topic_data["summary"]),
            "file": f"by_{date_str}.html"
        })
        save_data_json(data)
        print(f"[DATA] data.json 已更新 (共 {len(data)} 条)")

    print(f"[GENERATED] {output_file}")
    print(f"[GENERATED] {index_file}")
    print(f"[TOPIC] {topic_data['topic']}")

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
