#!/usr/bin/env python3
"""Sinh trang tin tĩnh cho news.solveralogistics.vn từ posts.json -> thư mục docs/"""
import json, html, pathlib, shutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
DOMAIN = "news.solveralogistics.vn"
SITE = "Tin tức Solvera Logistics"
MAIN = "https://solveralogistics.vn"

CSS = """
:root{--navy:#0a2a40;--teal:#0b7e93;--orange:#ff8d1c;--surface:#eef6f8;--bg:#f5f7fa;--ink:#1c2733;--mut:#6b7a8a}
*{box-sizing:border-box}body{margin:0;font-family:'Be Vietnam Pro',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--ink);line-height:1.65}
a{color:inherit;text-decoration:none}
header{background:var(--navy);color:#fff;border-bottom:4px solid var(--teal)}
.bar{max-width:1100px;margin:auto;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.brand{font-weight:800;letter-spacing:.5px}.brand span{color:var(--teal);filter:brightness(1.6)}.brand b{color:var(--orange)}
.bar a.back{font-size:14px;opacity:.9;border:1px solid rgba(255,255,255,.4);padding:6px 12px;border-radius:6px}
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

def page(title, body, desc="", canonical="/"):
    t = html.escape(title)
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="https://{DOMAIN}{canonical}">
<meta property="og:title" content="{t}"><meta property="og:description" content="{html.escape(desc)}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&display=swap"><style>{CSS}</style></head><body>
<header><div class="bar"><a class="brand" href="/"><img src="/images/logo.png" alt="Solvera Logistics" style="height:40px;vertical-align:middle;background:#fff;border-radius:6px;padding:4px 8px"> · Tin tức</a>
<a class="back" href="{MAIN}">← Về website chính</a></div></header>
{body}
<footer>© Solvera Logistics Co., Ltd · <a href="{MAIN}">solveralogistics.vn</a> · Hà Nội</footer>
</body></html>"""

def full_page(p):
    t = html.escape(p["title"] + " | " + SITE)
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{html.escape(p["summary"])}">
<link rel="canonical" href="https://{DOMAIN}/{p["slug"]}/">
<meta property="og:title" content="{t}"><meta property="og:description" content="{html.escape(p["summary"])}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&display=swap">
<style>{p["page_css"]}</style>
<style>.svtop{{background:#fff;color:#0a2a40;border-bottom:4px solid #0b7e93;font-family:'Be Vietnam Pro',sans-serif}}.svtop div{{max-width:1100px;margin:auto;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px}}.svtop a{{color:#0a2a40;text-decoration:none}}.svtop .lg{{display:flex;align-items:center;gap:12px;font-weight:700}}.svtop img{{display:block;height:40px;width:auto}}.svtop b{{color:#ff8d1c}}.svtop .bk{{font-size:14px;border:1px solid #0b7e93;color:#0b7e93;padding:5px 12px;border-radius:6px}}.svfoot{{background:#061520;color:#cfd8e3;text-align:center;padding:22px 16px;font:14px 'Be Vietnam Pro',sans-serif;border-top:4px solid #ff8d1c}}.svfoot a{{color:#ff8d1c}}</style></head><body>
<div class="svtop"><div><a href="/" class="lg"><img src="/images/logo.png" alt="Solvera Logistics" height="40"><span>Tin tức</span></a><a class="bk" href="{MAIN}">← Về website chính</a></div></div>
{p["mast_html"]}
<main class="wrap">{p["main_html"]}</main>
<div class="svfoot">© Solvera Logistics Co., Ltd · <a href="{MAIN}">solveralogistics.vn</a> · Hà Nội</div>
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
        img = f'<img src="{html.escape(p.get("image",""))}" alt="" loading="lazy">' if p.get("image") else '<img alt="">'
        cards.append(f'<a class="card" href="/{p["slug"]}/">{img}<div class="in"><span class="tag">{html.escape(p["category"])}</span>'
                     f'<h2>{html.escape(p["title"])}</h2><p>{html.escape(p["summary"])}</p><div class="date">{p["date"]}</div></div></a>')
    idx = f'<div class="hero"><h1>{SITE}</h1><p>Cập nhật hàng hải, xuất nhập khẩu, hàng không và tuyến Nhật – Việt.</p></div><div class="grid">{"".join(cards)}</div>'
    (OUT / "index.html").write_text(page(SITE, idx, "Tin tức logistics, hàng hải, xuất nhập khẩu từ Solvera Logistics"), encoding="utf-8")

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
