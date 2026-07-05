#!/usr/bin/env python3
"""从 data.json 自动生成 archive.html（备孕知识历史回顾）"""
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), "archive.html")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

count = len(data)
entries_html = ""
for item in reversed(data):  # 最新在前
    entries_html += f"""            <a class="entry" href="{item['file']}">
                <div class="entry-date">{item['date']}</div>
                <div class="entry-topic">{item['topic']}</div>
                <div class="entry-summary">{item['summary']}</div>
            </a>
"""

html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>备孕小贴士 · 历史回顾</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: #0a0a0a; min-height: 100vh; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; color: #fff; }}
        .container {{ max-width: 420px; margin: 0 auto; }}
        .header {{ text-align: center; padding: 32px 0 24px; }}
        .header-title {{ font-size: 28px; font-weight: 700; letter-spacing: 2px; background: linear-gradient(180deg, #e8a0bf 0%, #c77d97 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
        .header-sub {{ font-size: 11px; color: rgba(255,255,255,0.4); margin-top: 8px; }}
        .stats {{ text-align: center; padding: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; margin-bottom: 24px; font-size: 12px; color: rgba(255,255,255,0.5); }}
        .stats span {{ color: #e8a0bf; font-weight: 600; font-size: 18px; }}
        .entry-list {{ display: flex; flex-direction: column; gap: 10px; }}
        .entry {{ background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%); border-radius: 12px; padding: 16px; text-decoration: none; display: block; border: 1px solid rgba(255,255,255,0.05); }}
        .entry:hover {{ border-color: rgba(232,160,191,0.3); background: linear-gradient(135deg, #222 0%, #111 100%); }}
        .entry-date {{ font-size: 11px; color: #e8a0bf; margin-bottom: 6px; letter-spacing: 1px; }}
        .entry-topic {{ font-size: 15px; font-weight: 600; color: #e8e8e8; line-height: 1.5; }}
        .entry-summary {{ font-size: 12px; color: rgba(255,255,255,0.45); margin-top: 8px; line-height: 1.6; }}
        .back-link {{ display: block; text-align: center; padding: 20px; color: rgba(255,255,255,0.4); font-size: 13px; text-decoration: none; }}
        .back-link:hover {{ color: #e8a0bf; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-title">备孕小贴士</div>
            <div class="header-sub">历史回顾</div>
        </div>
        <div class="stats">已推送 <span>{count}</span> 篇备孕知识</div>
        <div class="entry-list">
{entries_html}        </div>
        <a href="index.html" class="back-link">← 返回今日推送</a>
    </div>
</body>
</html>
"""

with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ archive.html 已生成，共 {count} 篇")
