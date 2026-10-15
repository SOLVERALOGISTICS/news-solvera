#!/usr/bin/env python3
"""Đăng 1 bài Breaking News vào posts.json (chuẩn SEO, giữ nguyên nội dung gốc).
Cách dùng:
  python3 add_breaking.py --slug breaking-2026-10-16-ten-tin --date 2026-10-16 \
     --title "Tiêu đề bài (rõ nghĩa)" --sub "Dòng phụ dưới tiêu đề" --summary "Tóm tắt <=155 ký tự" \
     --body /tmp/body.html [--cover ten_anh.jpg] 
Trong body.html: dùng <p>, <h2>, <h3>, <ul><li>, <strong>. Ảnh chèn bằng dòng riêng:
  [[IMG:duong/dan/anh.jpg|mô tả alt|chú thích]]
Script: nén ảnh -> images/<slug>-N.jpg, tạo mục lục từ h2, thêm CSS (chế độ tối OK), gợi ý đọc tiếp,
khối liên hệ, mast; ghi vào posts.json (cùng slug thì thay thế). Sau đó chạy build.py.
"""
import argparse, json, re, html, shutil, os, datetime, unicodedata
from PIL import Image
ap = argparse.ArgumentParser()
ap.add_argument('--slug', required=True); ap.add_argument('--date', required=True)
ap.add_argument('--title', required=True); ap.add_argument('--sub', default='')
ap.add_argument('--summary', required=True); ap.add_argument('--body', required=True)
ap.add_argument('--cover', default='')
a = ap.parse_args()
posts = json.load(open('posts.json'))
ref = next(p for p in posts if p['slug'] == 'van-tai-hang-khong-duong-bien-viet-nhat')
styles = ''.join(s for s in re.findall(r'<style>.*?</style>', ref['main_html'], flags=re.S) if '.goals' in s)
contact = ref['main_html'][ref['main_html'].index('<section class="contact"'):]
body = open(a.body, encoding='utf-8').read()
n = [0]; first = ['']
def img(m):
    n[0] += 1
    src, alt, cap = (m.group(1).split('|') + ['', ''])[:3]
    out = f'images/{a.slug}-{n[0]}.jpg'
    im = Image.open(src).convert('RGB'); im.thumbnail((1400, 1400)); im.save(out, quality=82, optimize=True)
    if n[0] == 1: first[0] = out
    return (f'<figure class="fig"><img src="/{out}" alt="{html.escape(alt)}" loading="lazy" style="width:100%;border-radius:12px;display:block">'
            f'<figcaption style="font-size:.85rem;color:#5b6b78;margin-top:6px">{html.escape(cap)}</figcaption></figure>')
body = re.sub(r'\[\[IMG:(.*?)\]\]', img, body)
toc = []
def h2(m):
    t = re.sub('<[^>]+>', '', m.group(2)); i = re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', t.lower().replace('đ','d')).encode('ascii', 'ignore').decode()).strip('-')[:50].strip('-') or f's{len(toc)+1}'
    toc.append((i, t)); return f'<h2 id="{i}">{m.group(2)}</h2>'
body = re.sub(r'<h2([^>]*)>(.*?)</h2>', h2, body, flags=re.S)
nav = '<nav class="jump" aria-label="Mục lục">' + ''.join(f'<a href="#{i}">{html.escape(html.unescape(t))}</a>' for i, t in toc) + '</nav>' if len(toc) > 1 else ''
posts = [p for p in posts if p['slug'] != a.slug]
others = [p for p in sorted(posts, key=lambda x: x['date'], reverse=True) if p['category'] in ('Breaking News', 'Phân tích chuyên sâu')][:3]
rel = '<section class="rel"><h2 id="doc-tiep">Đọc tiếp</h2>' + ''.join(f'<a href="/{p["slug"]}/">{html.escape(p.get("topic") or p["title"])}<span>{html.escape(p["summary"])}</span></a>' for p in others) + '</section>'
d = datetime.date.fromisoformat(a.date)
wd = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật'][d.weekday()]
mast = (f'<header class="mast"><div class="wrap">\n  <div class="eyebrow">Solvera Logistics · Breaking News</div>\n  <h1>{html.escape(a.title)}</h1>\n'
        f'  <p>{html.escape(a.sub)}</p>\n  <span class="date">{wd}, {d.day:02d}/{d.month:02d}/{d.year}</span>\n</div></header>')
main = styles + body.replace('@NAV@', '') + '' if False else None
lead_split = re.search(r'</p>', body)
if nav and lead_split: body = body[:lead_split.end()] + nav + body[lead_split.end():]
main = styles + body + rel + contact
cover = a.cover or first[0] or 'images/thumb-tuan.jpg'
if a.cover and os.path.exists(a.cover):
    out = f'images/{a.slug}-cover.jpg'; im = Image.open(a.cover).convert('RGB'); im.thumbnail((1400, 1400)); im.save(out, quality=82, optimize=True); cover = out
posts.insert(0, {"slug": a.slug, "date": a.date, "category": "Breaking News", "topic": a.title, "title": a.title, "summary": a.summary,
                 "image": cover, "body_html": "", "page_css": ref['page_css'], "mast_html": mast, "main_html": main})
json.dump(posts, open('posts.json', 'w'), ensure_ascii=False, indent=1)
print('OK', a.slug, 'ảnh:', n[0], 'mục:', len(toc))
