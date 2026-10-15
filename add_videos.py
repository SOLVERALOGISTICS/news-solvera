#!/usr/bin/env python3
"""Đăng video YouTube (kênh @SOLVERALOGISTICS hoặc video Unlisted) thành bài ngắn trong mục "Video địa chính trị".
Dùng: python3 add_videos.py videos.txt  (mỗi dòng: videoId|tiêu đề gốc trên YouTube[|slug-bài-phân-tích-liên-quan])
Đã đăng (cùng videoId) thì bỏ qua -> không trùng. Ghi videos_done tự nhiên qua posts.json (slug video-<id>)."""
import json, re, html, sys, datetime
posts = json.load(open('posts.json'))
have = {p['slug'] for p in posts}
ref = next(p for p in posts if p['slug'] == 'van-tai-hang-khong-duong-bien-viet-nhat')
styles = ''.join(s for s in re.findall(r'<style>.*?</style>', ref['main_html'], flags=re.S) if '.goals' in s)
contact = ref['main_html'][ref['main_html'].index('<section class="contact"'):]
vcss = ('<style>.vid{position:relative;aspect-ratio:16/9;background:#0a2a40 center/cover no-repeat;border-radius:12px;overflow:hidden;margin:18px 0;cursor:pointer}'
        '.vid iframe{position:absolute;inset:0;width:100%;height:100%;border:0}.vid button{position:absolute;inset:0;margin:auto;width:72px;height:72px;border-radius:50%;border:0;background:#ff8d1c;color:#0a2a40;font-size:30px;cursor:pointer}'
        '.vnote{background:#fff;color:#0a2a40;border:1px solid #d6e2ea;border-radius:12px;padding:14px 16px;margin:16px 0}.vnote a{color:#0b7e93;font-weight:700}</style>')
def clean(t):
    t = re.sub(r'\s+\d+ (minutes?|seconds?|hours?).*$', '', t.strip())
    parts = [x.strip() for x in re.split(r'\s+[I|]\s+', t) if x.strip() and not re.search(r'solver|sovler|sovera', x, re.I)]
    return ' – '.join(parts) or t
new = 0
for ln in open(sys.argv[1], encoding='utf-8'):
    if '|' not in ln: continue
    vid, raw = ln.strip().split('|', 1)
    slug = f'video-{vid}'
    if slug in have: continue
    title = clean(raw); e = html.escape(title)
    img = f'https://i.ytimg.com/vi/{vid}/hqdefault.jpg'
    rel_posts = [p for p in posts if p['category'] == 'Phân tích chuyên sâu'][:3]
    rel = '<section class="rel"><h2 id="doc-tiep">Đọc tiếp</h2>' + ''.join(f'<a href="/{p["slug"]}/">{html.escape(p.get("topic") or p["title"])}<span>{html.escape(p["summary"])}</span></a>' for p in rel_posts) + '</section>'
    body = (f'<p>Video địa chính trị «{e}» từ kênh YouTube Solvera Logistics.</p>'
            f'<div class="vid" id="v-{vid}" style="background-image:url({img})" role="button" aria-label="Phát video {e}"><button type="button" aria-label="Phát video">▶</button></div>'
            f'<script>document.getElementById("v-{vid}").addEventListener("click",function(){{this.innerHTML=\'<iframe src="https://www.youtube-nocookie.com/embed/{vid}?autoplay=1&rel=0" title="{e}" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>\'}})</script>'
            f'<div class="vnote"><strong>Xem thêm video địa chính trị:</strong> <a href="https://www.youtube.com/@SOLVERALOGISTICS" rel="noopener" target="_blank">kênh YouTube Solvera Logistics</a> · <a href="https://www.youtube.com/watch?v={vid}" rel="noopener" target="_blank">mở trên YouTube</a>.</div>')
    d = datetime.date.today(); wd = ['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật'][d.weekday()]
    mast = (f'<header class="mast"><div class="wrap">\n  <div class="eyebrow">Solvera Logistics · Video địa chính trị</div>\n  <h1>{e}</h1>\n'
            f'  <p>Video từ kênh YouTube Solvera Logistics.</p>\n  <span class="date">{wd}, {d.day:02d}/{d.month:02d}/{d.year}</span>\n</div></header>')
    posts.append({"slug": slug, "date": d.isoformat(), "category": "Video địa chính trị", "topic": title, "title": title,
                  "summary": f'Video địa chính trị «{title}» từ kênh YouTube Solvera Logistics.'[:155], "image": img, "body_html": "",
                  "page_css": ref['page_css'], "mast_html": mast, "main_html": styles + vcss + body + rel + contact})
    new += 1
json.dump(posts, open('posts.json', 'w'), ensure_ascii=False, indent=1)
print('Đã thêm', new, 'video')
