"""从 data.json 动态生成 archive.html"""
import json

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

items_html = ''
for item in reversed(data):
    items_html += f'''      <div class="archive-item">
        <span class="archive-date">{item['date']}</span>
        <a class="archive-link" href="{item['file']}">{item['topic']}</a>
      </div>\n'''

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>备孕知识 - 历史回顾</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0a0a0a; min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .card {{
            width: 420px; max-width: 100%; background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
            border-radius: 16px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8);
        }}
        .header {{
            background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
            padding: 24px 20px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .tag {{ font-size: 10px; color: rgba(255,255,255,0.4); letter-spacing: 2px; margin-bottom: 8px; }}
        .title {{ font-size: 22px; font-weight: 700; color: #fff; letter-spacing: 3px; }}
        .count {{ font-size: 12px; color: rgba(255,255,255,0.4); margin-top: 6px; }}
        .list {{ padding: 20px; max-height: 500px; overflow-y: auto; }}
        .archive-item {{
            display: flex; align-items: baseline; gap: 12px; padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .archive-date {{ font-size: 12px; color: #e8a0bf; font-weight: 600; white-space: nowrap; min-width: 72px; }}
        .archive-link {{
            font-size: 13px; color: rgba(255,255,255,0.7); text-decoration: none; line-height: 1.5;
        }}
        .archive-link:hover {{ color: #e8a0bf; }}
        .back {{
            display: block; text-align: center; padding: 16px; color: #e8a0bf;
            font-size: 13px; text-decoration: none; border-top: 1px solid rgba(255,255,255,0.05);
        }}
        .back:hover {{ color: #fff; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="tag">ARCHIVE</div>
            <div class="title">备孕知识 · 往期回顾</div>
            <div class="count">共 {len(data)} 篇</div>
        </div>
        <div class="list">
{items_html}    </div>
        <a class="back" href="index.html">← 返回今日小贴士</a>
    </div>
</body>
</html>'''

with open('archive.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'archive.html generated with {len(data)} entries')
