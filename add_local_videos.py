#!/usr/bin/env python3
"""Đăng video tự lưu trong repo (videos/<name>.mp4 + .jpg) vào mục Video, loạt Logistics in Motion.
Dùng: python3 add_local_videos.py  (sửa danh sách V bên dưới). Bài đã có (cùng slug) thì bỏ qua."""
import json, re, html, datetime
posts = json.load(open('posts.json'))
have = {p['slug'] for p in posts}
ref = next(p for p in posts if p['slug'] == 'van-tai-hang-khong-duong-bien-viet-nhat')
styles = ''.join(s for s in re.findall(r'<style>.*?</style>', ref['main_html'], flags=re.S) if '.goals' in s)
contact = ref['main_html'][ref['main_html'].index('<section class="contact"'):]
vcss = '<style>.lvid{display:block;width:100%;max-width:340px;aspect-ratio:9/16;margin:18px auto;border-radius:12px;background:#0d3b3b}.vnote{background:#fff;color:#0d3b3b;border:1px solid #d6e2ea;border-radius:12px;padding:14px 16px;margin:16px 0}.vnote a{color:#00a896;font-weight:700}</style>'
V = [
 ("vefta-vietnam-to-efta-sea-inland", "2026-11-13", "Vietnam to EFTA: Sea and Inland Routes I VEFTA I Logistics in Motion",
  "Routes from Cai Mep, Vietnam to Norway, Switzerland and Liechtenstein under the Vietnam–EFTA Free Trade Agreement (VEFTA, signed on 18 October 2026).",
  "Sea freight and inland connections from Cai Mep to Oslo, Zurich and Geneva. Routes are illustrative; transshipment may apply."),
 ("vefta-air-freight-vietnam-to-efta", "2026-11-13", "Air Freight: Vietnam to EFTA I VEFTA I Logistics in Motion",
  "Air freight routes between Vietnam and EFTA markets: exports, imports, high-value cargo and time-critical shipments.",
  "Air connections for high-value and time-critical cargo between Vietnam and EFTA, supporting global supply chain connectivity."),
 ("vietnam-to-indian-ocean-routes", "2026-11-13", "Routes from Vietnam to the Indian Ocean I Hormuz and Cape of Good Hope I Logistics in Motion",
  "Three illustrative shipping routes from Vietnam to the Indian Ocean, including the route via the Arabian Sea and the Strait of Hormuz and the route around the Cape of Good Hope.",
  "Illustrative routes from Vietnam through the South China Sea and the Indian Ocean, with the route around the Cape of Good Hope."),
]
new = 0
for name, date, title, summ, para in V:
    slug = f'video-{name}'
    if slug in have: continue
    e = html.escape(title); d = datetime.date.fromisoformat(date)
    wd = ['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật'][d.weekday()]
    rel_posts = [p for p in posts if p['category'] == 'Phân tích chuyên sâu'][:3]
    rel = '<section class="rel"><h2 id="doc-tiep">Đọc tiếp</h2>' + ''.join(f'<a href="/{p["slug"]}/">{html.escape(p.get("topic") or p["title"])}<span>{html.escape(p["summary"])}</span></a>' for p in rel_posts) + '</section>'
    body = (f'<p>Video «{e}» của Solvera Logistics.</p>'
            f'<video class="lvid" controls playsinline preload="metadata" poster="/videos/{name}.jpg" aria-label="{e}"><source src="/videos/{name}.mp4" type="video/mp4"></video>'
            f'<h2 id="noi-dung">{html.escape(summ)}</h2><p>{html.escape(para)}</p>'
            '<div class="vnote"><strong>Xem thêm video:</strong> <a href="https://www.youtube.com/@SOLVERALOGISTICS" rel="noopener" target="_blank">kênh YouTube Solvera Logistics</a>.</div>')
    mast = (f'<header class="mast"><div class="wrap">\n  <div class="eyebrow">Solvera Logistics · Logistics in Motion</div>\n  <h1>{e}</h1>\n'
            f'  <p>Video của Solvera Logistics.</p>\n  <span class="date">{wd}, {d.day:02d}/{d.month:02d}/{d.year}</span>\n</div></header>')
    posts.append({"series": "Logistics in Motion", "short": True, "lang": "en", "slug": slug, "date": date, "category": "Video", "topic": title, "title": title,
                  "summary": summ[:155], "image": f"videos/{name}.jpg", "body_html": "", "page_css": ref['page_css'], "mast_html": mast,
                  "main_html": styles + vcss + body + rel + contact})
    new += 1
json.dump(posts, open('posts.json', 'w'), ensure_ascii=False, indent=1)
print('Đã thêm', new, 'video')
