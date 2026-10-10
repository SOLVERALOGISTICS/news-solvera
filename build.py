#!/usr/bin/env python3
"""Sinh trang tin tĩnh cho news.solveralogistics.vn từ posts.json -> thư mục docs/"""
import json, html, pathlib, shutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
DOMAIN = "news.solveralogistics.vn"
SITE = "Solvera Logistics News"
MAIN = "https://solveralogistics.vn"

CSS = """
:root{--navy:#0a2a40;--teal:#0b7e93;--orange:#ff8d1c;--surface:#eef6f8;--bg:#f5f7fa;--ink:#1c2733;--mut:#6b7a8a}
*{box-sizing:border-box}body{margin:0;font-family:'Be Vietnam Pro',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--ink);line-height:1.65}
a{color:inherit;text-decoration:none}
header{background:#fff;color:var(--navy);border-bottom:4px solid var(--teal)}
.bar{max-width:1100px;margin:auto;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.brand{font-weight:800;display:flex;align-items:center;gap:12px}.brand span{color:var(--teal);filter:brightness(1.6)}.brand b{color:var(--orange)}
.bar a.back{font-size:14px;color:var(--teal);border:1px solid var(--teal);padding:6px 12px;border-radius:6px}
.hero{max-width:1100px;margin:auto;padding:28px 20px 8px}.hero h1{margin:0;font-size:28px;color:var(--navy);border-left:5px solid var(--orange);padding-left:12px}.hero p{margin:6px 0 0;color:var(--mut)}
.grid{max-width:1100px;margin:auto;padding:16px 20px 48px;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.card{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08);display:flex;flex-direction:column}
.card img{width:100%;height:180px;object-fit:cover;background:#cfd8e3}
.card .in{padding:14px 16px 18px}.tag{display:inline-block;background:var(--orange);color:#fff;font-size:12px;font-weight:700;padding:2px 8px;border-radius:4px}
.card h2{font-size:18px;margin:8px 0 6px;color:var(--navy)}.card p{margin:0;color:var(--mut);font-size:14px}.date{font-size:12px;color:var(--mut);margin-top:8px}
article{max-width:780px;margin:0 auto;padding:28px 20px 56px}article h1{color:var(--navy);font-size:30px;line-height:1.3;margin:8px 0}
article .cover{width:100%;max-height:420px;object-fit:cover;border-radius:10px;margin:14px 0}
article h2{color:var(--navy);margin-top:36px;font-size:24px}article h2 small{display:block;font-size:13px;font-weight:700;color:var(--teal);letter-spacing:.06em}
.lead{font-size:17px;color:var(--mut)}.item{border-top:1px solid #d5e4e9;padding:18px 0}.item .tag{background:var(--teal)}.item h3{font-size:19px;color:var(--navy);margin:6px 0}
.impact{background:var(--surface);padding:10px 14px;border-radius:10px;border-left:4px solid var(--orange)}.impact b{color:var(--orange)}
.src{font-size:14px;color:var(--mut);padding-left:18px}.src a{color:var(--teal);text-decoration:underline;word-break:break-word}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin:12px 0}.kpi{background:var(--surface);border-radius:12px;padding:12px 14px}.kpi b{display:block;font-size:22px;color:var(--orange)}.kpi i{font-size:12px;color:var(--mut);font-style:normal}
.note{font-size:14px;color:var(--mut)}.advice li{margin-bottom:8px}
.date{display:inline-block;background:#0f3b57;color:var(--orange);font-weight:800;padding:2px 10px;border-radius:6px}
footer{border-top:4px solid var(--orange)}
.mast{background:var(--navy);color:#fff;padding:30px 20px 32px}.mast .w{max-width:780px;margin:auto}.eyebrow{color:var(--orange);font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:13px}.mast h1{font-size:clamp(28px,6vw,42px);line-height:1.15;margin:8px 0;font-weight:800;color:#fff}.mast p{margin:0;color:#c8dde5}.mast .date{margin-top:14px}
nav.jump{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 0}nav.jump a{color:var(--teal);border:1px solid #d5e4e9;padding:4px 12px;border-radius:999px;font-size:14px;font-weight:600;background:#fff}
article{background:#fff;max-width:780px;margin:0 auto;padding:8px 20px 56px}article h1{display:none}article>.tag:first-child,article>.date:first-of-type{display:none}.src a{color:#0a6d80!important;text-decoration:underline!important}
footer{background:var(--navy);color:#cfd8e3;text-align:center;padding:22px 16px;font-size:14px}footer a{color:var(--orange)}
"""

LANG = ('<style>.soc{display:flex;gap:6px;align-items:center;margin-left:auto;margin-right:12px}.soc a{width:32px;height:32px;border-radius:50%;border:1.5px solid #0b7e93;display:flex;align-items:center;justify-content:center;color:#0b7e93;fill:#0b7e93;text-decoration:none}.soc a b{font:700 9px "Be Vietnam Pro",sans-serif}.soc a:hover{background:#0b7e93;color:#fff;fill:#fff}.svtop div,header .bar{flex-wrap:wrap;row-gap:8px}.lang{display:flex;gap:6px;align-items:center;margin-right:12px}.lang a{font:600 13px "Be Vietnam Pro",sans-serif;color:#0b7e93;border:1.5px solid #0b7e93;border-radius:999px;padding:4px 10px;text-decoration:none;white-space:nowrap}.lang a:hover{background:#0b7e93;color:#fff}.goog-te-banner-frame,#goog-gt-tt{display:none!important}body{top:0!important}@media(max-width:560px){.back,.bk{order:1;padding:4px 8px!important;font-size:12px!important;margin-left:auto}.soc{order:2;margin:0 6px 0 0}.soc a{width:28px;height:28px}.lang{order:3;margin:0}.lang a{padding:3px 8px;font-size:12px}}</style>'
 '<span class="soc notranslate" translate="no"><a href="https://zalo.me/2938397457262576692" target="_blank" rel="noopener" aria-label="Zalo" title="Zalo"><b>Zalo</b></a><a href="https://www.facebook.com/share/1CQrtY27t4/?mibextid=wwXIfr" target="_blank" rel="noopener" aria-label="Facebook" title="Facebook"><svg viewBox="0 0 24 24" width="16" height="16"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg></a><a href="https://www.linkedin.com/company/solvera-logistics/" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" width="16" height="16"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg></a><a href="https://www.tiktok.com/@solveralogistics" target="_blank" rel="noopener" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" width="16" height="16"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a><a href="https://www.youtube.com/@SOLVERALOGISTICS" target="_blank" rel="noopener" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" width="16" height="16"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2C0 8.1 0 12 0 12s0 3.9.5 5.8a3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1c.5-1.9.5-5.8.5-5.8s0-3.9-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg></a></span><span class="lang notranslate" translate="no"><a id="l-vi" href="#">VI</a><a id="l-en" href="#">EN</a><a id="l-ja" href="#">日本語</a><a id="l-zh" href="#">中文</a></span>'
 '<script>(function(){var q=new URLSearchParams(location.search);["_x_tr_sl","_x_tr_tl","_x_tr_hl","_x_tr_pto"].forEach(function(k){q.delete(k)});var s=q.toString(),b=location.pathname+(s?"?"+s:""),t="https://news-solveralogistics-vn.translate.goog"+b+(s?"&":"?");'
 'document.getElementById("l-vi").href="https://news.solveralogistics.vn"+b;document.getElementById("l-en").href=t+"_x_tr_sl=vi&_x_tr_tl=en&_x_tr_hl=en";document.getElementById("l-ja").href=t+"_x_tr_sl=vi&_x_tr_tl=ja&_x_tr_hl=ja";document.getElementById("l-zh").href=t+"_x_tr_sl=vi&_x_tr_tl=zh-CN&_x_tr_hl=zh-CN"})()</script>')

def page(title, body, desc="", canonical="/"):
    t = html.escape(title)
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://{DOMAIN}{canonical}">
<meta property="og:image" content="https://news.solveralogistics.vn/images/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta property="og:title" content="{t}"><meta property="og:description" content="{html.escape(desc)}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&display=swap"><style>{CSS}</style></head><body>
<header><div class="bar"><a class="brand" href="/"><img src="/images/logo.png" alt="Solvera Logistics" style="height:40px;display:block"><span>News</span></a>
{LANG}<a class="back" href="{MAIN}">← Main website</a></div></header>
{body}
<footer>© Solvera Logistics Co., Ltd · <a href="{MAIN}">solveralogistics.vn</a> · Hanoi</footer>
</body></html>"""

def full_page(p):
    t = html.escape(p["title"] + " | " + SITE)
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{html.escape(p["summary"])}">
<link rel="canonical" href="https://{DOMAIN}/{p["slug"]}/">
<meta property="og:image" content="https://news.solveralogistics.vn/images/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta property="og:title" content="{t}"><meta property="og:description" content="{html.escape(p["summary"])}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&display=swap">
<style>{p["page_css"]}</style>
<style>.svtop{{background:#fff;color:#0a2a40;border-bottom:4px solid #0b7e93;font-family:'Be Vietnam Pro',sans-serif}}.svtop div{{max-width:1100px;margin:auto;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px}}.svtop a{{color:#0a2a40;text-decoration:none}}.svtop .lg{{display:flex;align-items:center;gap:12px;font-weight:700}}.svtop img{{display:block;height:40px;width:auto}}.svtop b{{color:#ff8d1c}}.svtop .bk{{font-size:14px;border:1px solid #0b7e93;color:#0b7e93;padding:5px 12px;border-radius:6px}}.svfoot{{background:#061520;color:#cfd8e3;text-align:center;padding:22px 16px;font:14px 'Be Vietnam Pro',sans-serif;border-top:4px solid #ff8d1c}}.svfoot a{{color:#ff8d1c}}</style></head><body>
<div class="svtop"><div><a href="/" class="lg"><img src="/images/logo.png" alt="Solvera Logistics" height="40"><span>News</span></a>{LANG}<a class="bk" href="{MAIN}">← Main website</a></div></div>
{p["mast_html"]}
<main class="wrap">{p["main_html"]}</main>
<div class="svfoot">© Solvera Logistics Co., Ltd · <a href="{MAIN}">solveralogistics.vn</a> · Hanoi</div>
</body></html>"""

def main():
    posts = json.loads((ROOT / "posts.json").read_text(encoding="utf-8"))
    posts.sort(key=lambda p: p["date"], reverse=True)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    (OUT / "CNAME").write_text(DOMAIN)
    (OUT / ".nojekyll").write_text("")

    cards = []
    for p in posts:
        img = f'<img src="{html.escape(p.get("image",""))}" alt="" loading="lazy">' if p.get("image") else ''
        cards.append(f'<a class="card" href="/{p["slug"]}/">{img}<div class="in"><span class="tag">{html.escape(p["category"])}</span>'
                     f'<h2>{html.escape(p["title"])}</h2><p>{html.escape(p["summary"])}</p><div class="date">{p["date"]}</div></div></a>')
    idx = f'<div class="hero"><h1>{SITE}</h1><p>Tin tức hàng hải, hàng không, logistics, Supply Chain và kinh doanh xuất nhập khẩu.</p></div><div class="grid">{"".join(cards)}</div>'
    (OUT / "index.html").write_text(page(SITE, idx, "Tin tức hàng hải, hàng không, logistics, Supply Chain và kinh doanh xuất nhập khẩu"), encoding="utf-8")

    for p in posts:
        d = OUT / p["slug"]
        d.mkdir()
        if p.get("main_html"):
            (d / "index.html").write_text(full_page(p), encoding="utf8"); continue
        cover = f'<img class="cover" src="{html.escape(p["image"])}" alt="">' if p.get("image") else ""
        nav = '<nav class="jump"><a href="#hang-hai">Hàng hải</a><a href="#xnk">Xuất nhập khẩu</a><a href="#hang-khong">Hàng không</a><a href="#khuyen-nghi">Khuyến nghị</a></nav>' if 'id="hang-hai"' in p["body_html"] else ""
        body = (f'<div class="mast"><div class="w"><div class="eyebrow">Solvera Logistics · {html.escape(p["category"])}</div><h1>{html.escape(p["title"])}</h1>'
                f'<p>{html.escape(p["summary"])}</p><span class="date">{p["date"]}</span></div></div>'
                f'<article>{cover}{nav}{p["body_html"]}</article>')
        (d / "index.html").write_text(page(p["title"] + " | " + SITE, body, p["summary"], f'/{p["slug"]}/'), encoding="utf-8")
    print(f"OK: {len(posts)} bài -> {OUT}")

if __name__ == "__main__":
    main()
