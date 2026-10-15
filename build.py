import re
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
.card{transition:transform .15s,box-shadow .15s}.card:hover,.card:active{transform:translateY(-3px);box-shadow:0 6px 16px rgba(10,42,64,.18)}.more{display:inline-block;margin-top:10px;color:var(--orange);font-weight:700;font-size:14px}.card h2{font-size:18px;margin:8px 0 6px;color:var(--navy)}.card p{margin:0;color:var(--mut);font-size:14px}.date{font-size:12px;color:var(--mut);margin-top:8px}
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
.lt img{width:36%!important;height:auto!important;min-height:0!important;aspect-ratio:1200/630;object-fit:contain!important;align-self:flex-start;margin:26px 0 26px 26px;border-radius:10px}@media(max-width:700px){.lt img{width:calc(100% - 32px)!important;margin:16px}}

.bc{max-width:1100px;margin:0 auto;padding:12px 20px;font-size:14px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;color:var(--mut)}.bc a{color:var(--teal);font-weight:600}.bc a:hover{text-decoration:underline}.bc i{font-style:normal}.backbtn{display:inline-block;margin:28px 0 8px;padding:12px 20px;border:1.5px solid var(--teal);border-radius:8px;color:var(--teal);font-weight:700}.backbtn:hover{background:var(--teal);color:#fff}

.pn{max-width:1100px;margin:auto;padding:8px 20px 56px}.ph{margin:14px 0 18px}.ph h2{margin:0;font-size:26px;color:var(--navy)}.ph p{margin:2px 0 4px;color:var(--ink)}.ph span{font-size:13px;color:var(--mut)}
.lt{display:flex;background:#fff;border:1px solid #e3ecef;border-left:5px solid var(--orange);border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(10,42,64,.08)}.lt img{width:40%;object-fit:cover;min-height:250px}.lt .in{padding:24px 28px;flex:1}.lt:hover{box-shadow:0 6px 18px rgba(10,42,64,.18)}
.bd{display:flex;gap:8px;align-items:center}.no{background:var(--navy);color:#fff;font-weight:800;font-size:13px;padding:3px 10px;border-radius:6px}.new{background:var(--orange);color:#fff;font-weight:800;font-size:12px;padding:3px 9px;border-radius:6px;letter-spacing:.05em}
.lt h2{margin:10px 0 0;font-size:28px;color:var(--navy)}.sub{color:var(--mut);font-size:14px}.hl{margin-top:14px;font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--teal)}.lt ul{margin:6px 0 0;padding-left:20px;color:var(--ink);font-size:15px}.lt li{margin-bottom:4px}.lt .more{display:inline-block;margin-top:12px}
.oh{margin:30px 0 10px;font-size:14px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}.rows{background:#fff;border:1px solid #e3ecef;border-radius:12px;overflow:hidden}.rw{display:flex;align-items:center;gap:16px;padding:16px 20px;border-top:1px solid #eef2f4}.rw:first-child{border-top:0}.rw:hover{background:var(--surface)}.rw .no{background:#e6eef2;color:var(--navy)}.rw .pr{flex:1;display:flex;flex-direction:column}.rw b{color:var(--navy)}.rw em{font-style:normal;color:var(--mut);font-size:14px}.rw .more{margin:0;white-space:nowrap}
@media(max-width:700px){.lt{flex-direction:column}.lt img{width:100%;min-height:0;height:170px}.lt .in{padding:18px}.lt h2{font-size:22px}.tabs{overflow-x:auto;flex-wrap:nowrap}.tab{white-space:nowrap}}

.hero2{background:linear-gradient(135deg,#0a2a40 0%,#0f4a63 100%);color:#fff;border-bottom:4px solid var(--orange)}.hero2 .hw{max-width:1100px;margin:auto;padding:40px 20px 36px}.hero2 .eb{color:var(--orange);font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:13px}.hero2 h1{margin:6px 0 8px;font-size:clamp(28px,5vw,42px);line-height:1.15;font-weight:800;color:#fff}.hero2 p{margin:0;color:#c8dde5;font-size:17px;max-width:640px}
.tabs{max-width:1100px;margin:22px auto 0;padding:0 20px;display:flex;gap:8px;flex-wrap:wrap}.tab{font:600 14px 'Be Vietnam Pro',sans-serif;border:1.5px solid #cfdde3;background:#fff;color:var(--navy);border-radius:999px;padding:8px 16px;cursor:pointer;display:inline-block}.tab i{font-style:normal;color:var(--teal);margin-left:4px}.tab.on{background:var(--navy);border-color:var(--navy);color:#fff}.tab.on i{color:var(--orange)}
.grid2{max-width:1100px;margin:auto;padding:20px 20px 56px;display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:22px}.grid2 .card.big{grid-column:1/-1;flex-direction:row}.grid2 .card.big img{width:46%;height:auto;min-height:260px}.grid2 .card.big .in{padding:26px 28px;display:flex;flex-direction:column;justify-content:center}.grid2 .card.big h2{font-size:26px}
.grid2 .card{display:flex;flex-direction:column;border:1px solid #e3ecef;box-shadow:0 1px 3px rgba(10,42,64,.06)}.grid2 .card img{height:180px;width:100%;object-fit:cover}.grid2 .card h2{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}.grid2 .card p{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}.grid2 .card .in{flex:1;display:flex;flex-direction:column}.foot{margin-top:auto;padding-top:14px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #eef2f4}.dt{font-size:13px;color:var(--mut)}.foot .more{margin:0}
.grid2 .tag{align-self:flex-start}.empty{grid-column:1/-1;border:2px dashed #b9d3db;border-radius:12px;background:#fff;padding:28px;text-align:center;color:var(--mut)}.empty b{display:block;color:var(--navy);font-size:20px;margin-bottom:6px}
@media(max-width:700px){.grid2 .card.big{flex-direction:column}.grid2 .card.big img{width:100%;min-height:0;height:190px}.grid2 .card.big h2{font-size:20px}.grid2 .card.big .in{padding:16px}}

.mast{background:var(--navy);color:#fff;padding:30px 20px 32px}.mast .w{max-width:780px;margin:auto}.eyebrow{color:var(--orange);font-weight:700;letter-spacing:.12em;text-transform:uppercase;font-size:13px}.mast h1{font-size:clamp(28px,6vw,42px);line-height:1.15;margin:8px 0;font-weight:800;color:#fff}.mast p{margin:0;color:#c8dde5}.mast .date{margin-top:14px}
nav.jump{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 0}nav.jump a{color:var(--teal);border:1px solid #d5e4e9;padding:4px 12px;border-radius:999px;font-size:14px;font-weight:600;background:#fff}
article{background:#fff;max-width:780px;margin:0 auto;padding:8px 20px 56px}article h1{display:none}article>.tag:first-child,article>.date:first-of-type{display:none}.src a{color:#0a6d80!important;text-decoration:underline!important}
footer{background:var(--navy);color:#cfd8e3;text-align:center;padding:22px 16px;font-size:14px}footer a{color:var(--orange)}
"""

LANG = ('<style>.soc{display:flex;gap:6px;align-items:center;margin-left:auto;margin-right:12px}.soc a{width:32px;height:32px;border-radius:50%;border:1.5px solid #0b7e93;display:flex;align-items:center;justify-content:center;color:#0b7e93;fill:#0b7e93;text-decoration:none}.soc a b{font:700 9px "Be Vietnam Pro",sans-serif}.soc a:hover{background:#0b7e93;color:#fff;fill:#fff}.svtop div,header .bar{flex-wrap:wrap;row-gap:8px}.lang{position:relative;margin-right:12px}.lang summary{list-style:none;cursor:pointer;font:600 13px "Be Vietnam Pro",sans-serif;color:#0b7e93;border:1.5px solid #0b7e93;border-radius:999px;padding:4px 10px;white-space:nowrap}.lang summary::-webkit-details-marker{display:none}.lang .lm{position:absolute;right:0;top:calc(100% + 6px);background:#fff;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,.18);padding:6px;display:flex;flex-direction:column;gap:2px;z-index:50;min-width:110px}.lang .lm a{border:0;border-radius:6px;padding:8px 12px}.lang a{font:600 13px "Be Vietnam Pro",sans-serif;color:#0b7e93;border:1.5px solid #0b7e93;border-radius:999px;padding:4px 10px;text-decoration:none;white-space:nowrap}.lang a:hover{background:#0b7e93;color:#fff}.src,.src li{color:#0b7e93!important;font-style:italic}.src li::marker{color:#ff8d1c}.goog-te-banner-frame,#goog-gt-tt{display:none!important}body{top:0!important}@media(max-width:560px){.back,.bk{order:1;padding:4px 8px!important;font-size:12px!important;margin-left:auto}.soc{order:2;margin:0 6px 0 0}.soc a{width:28px;height:28px}.lang{order:3;margin:0}.lang summary{padding:3px 8px;font-size:12px}}</style>'
 '<span class="soc notranslate" translate="no"><a href="https://zalo.me/2938397457262576692" target="_blank" rel="noopener" aria-label="Zalo" title="Zalo"><b>Zalo</b></a><a href="https://www.facebook.com/share/1CQrtY27t4/?mibextid=wwXIfr" target="_blank" rel="noopener" aria-label="Facebook" title="Facebook"><svg viewBox="0 0 24 24" width="16" height="16"><path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/></svg></a><a href="https://www.linkedin.com/company/solvera-logistics/" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" width="16" height="16"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg></a><a href="https://www.tiktok.com/@solveralogistics" target="_blank" rel="noopener" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" width="16" height="16"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a><a href="https://www.youtube.com/@SOLVERALOGISTICS" target="_blank" rel="noopener" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" width="16" height="16"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2C0 8.1 0 12 0 12s0 3.9.5 5.8a3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1c.5-1.9.5-5.8.5-5.8s0-3.9-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg></a></span><details class="lang notranslate" translate="no"><summary>🌐 Language ▾</summary><div class="lm"><a id="l-vi" href="#">VI</a><a id="l-en" href="#">EN</a><a id="l-ja" href="#">日本語</a><a id="l-zh" href="#">中文</a></div></details>'
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

def trunc(x, n):
    x = x.strip()
    return x if len(x) <= n else x[:n-1].rsplit(" ", 1)[0].rstrip(",;:–-") + "…"

def full_page(p):
    ci = {"Tin tức đầu tuần": 0, "Tin tức Nhật - Việt cuối tuần": 1, "Phân tích chuyên sâu": 2, "Hoạt động Solvera Logistics": 3, "Breaking News": 4}.get(p["category"], 0)
    bcss = "<style>.bc{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:18px 0 6px;font:600 14px 'Be Vietnam Pro',sans-serif;color:#6b7a8a}.bc a{color:#0b7e93;text-decoration:none}.bc a.home,.bc a.cat{background:#0b7e93;color:#fff;padding:7px 14px;border-radius:999px}.bc a.home:hover,.bc a.cat:hover{background:#0a2a40}.bc i{font-style:normal;color:#9fb0bb}.backbtn{display:inline-block;margin:28px 0 8px;padding:12px 20px;border:1.5px solid #0b7e93;border-radius:8px;color:#0b7e93;font-weight:700;text-decoration:none}.backbtn:hover{background:#0b7e93;color:#fff}</style>"
    bc = bcss + f'<nav class="bc"><a class="home" href="/">← Trang chủ</a><i>›</i><a class="cat" href="/#c{ci}">← {html.escape(p["category"])}</a><i>›</i><span>{p["date"][8:]}/{p["date"][5:7]}/{p["date"][:4]}</span></nav>'
    mast = re.sub(r'(<div class="eyebrow">)[^<]*', lambda m: m.group(1) + "Solvera Logistics · " + html.escape(p["category"]), p["mast_html"], count=1)
    head = p["title"].split(":")[0] if ":" in p["title"] and len(p["title"].split(":")[0]) >= 25 else p["title"]
    t = html.escape(trunc(head, 44) + " | Solvera News")
    ld = json.dumps({"@context": "https://schema.org", "@type": "NewsArticle", "headline": trunc(p["title"], 110),
        "datePublished": p["date"], "dateModified": p["date"], "inLanguage": "vi",
        "description": trunc(p["summary"], 155), "image": ["https://news.solveralogistics.vn/images/og.png"],
        "mainEntityOfPage": f"https://{DOMAIN}/{p['slug']}/",
        "author": {"@type": "Organization", "name": "Solvera Logistics"},
        "publisher": {"@type": "Organization", "name": "Solvera Logistics", "logo": {"@type": "ImageObject", "url": "https://news.solveralogistics.vn/images/logo.png"}}}, ensure_ascii=False)
    return f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{html.escape(trunc(p["summary"], 155))}"><script type="application/ld+json">{ld}</script>
<link rel="canonical" href="https://{DOMAIN}/{p["slug"]}/">
<meta property="og:image" content="https://news.solveralogistics.vn/images/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta property="og:title" content="{t}"><meta property="og:description" content="{html.escape(p["summary"])}">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&display=swap">
<style>{p["page_css"]}</style>
<style>.svtop{{background:#fff;color:#0a2a40;border-bottom:4px solid #0b7e93;font-family:'Be Vietnam Pro',sans-serif}}.svtop div{{max-width:1100px;margin:auto;padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px}}.svtop a{{color:#0a2a40;text-decoration:none}}.svtop .lg{{display:flex;align-items:center;gap:12px;font-weight:700}}.svtop img{{display:block;height:40px;width:auto}}.svtop b{{color:#ff8d1c}}.svtop .bk{{font-size:14px;border:1px solid #0b7e93;color:#0b7e93;padding:5px 12px;border-radius:6px}}.svfoot{{background:#061520;color:#cfd8e3;text-align:center;padding:22px 16px;font:14px 'Be Vietnam Pro',sans-serif;border-top:4px solid #ff8d1c}}.svfoot a{{color:#ff8d1c}}</style></head><body>
<div class="svtop"><div><a href="/" class="lg"><img src="/images/logo.png" alt="Solvera Logistics" height="40"><span>News</span></a>{LANG}<a class="bk" href="{MAIN}">← Main website</a></div></div>
{mast}
<main class="wrap">{bc}{p["main_html"]}<a class="backbtn" href="/#c{ci}">← Quay lại {html.escape(p["category"])}</a></main>
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

    TH = {"Tin tức đầu tuần": "/images/thumb-tuan.jpg", "Tin tức Nhật - Việt cuối tuần": "/images/thumb-nhatviet.jpg", "Phân tích chuyên sâu": "/images/thumb-phantich.jpg", "Hoạt động Solvera Logistics": "/images/thumb-hoatdong.jpg", "Breaking News": "/images/thumb-tuan.jpg"}
    INFO = {"Tin tức đầu tuần": ("Hàng hải · Hàng không · Xuất nhập khẩu", "Phát hành sáng thứ Hai hằng tuần"),
            "Tin tức Nhật - Việt cuối tuần": ("Vận tải · Logistics · Chuỗi cung ứng tuyến Nhật – Việt", "Phát hành sáng thứ Bảy hằng tuần"),
            "Phân tích chuyên sâu": ("Góc nhìn chuyên gia Solvera Logistics", "Cập nhật theo chủ đề"),
            "Hoạt động Solvera Logistics": ("Sự kiện · Đối tác · Hoạt động của Solvera Logistics", "Cập nhật khi có hoạt động mới"),
            "Breaking News": ("Tin nóng · Hàng hải · Hàng không · Xuất nhập khẩu", "Cập nhật hằng ngày khi có tin nóng")}
    CATS = list(INFO)
    def meta(p, n):
        pr = re.search(r"\d{2}[–-]\d{2}/\d{2}/\d{4}|\d{2}/\d{2}/\d{4}", p["title"])
        y, m, d_ = p["date"].split("-")
        hs = [html.unescape(re.sub("<[^>]+>", "", h)) for h in re.findall(r"<h3>(.*?)</h3>", p.get("main_html", ""), re.S)]
        tp = p.get("topic")
        if tp:
            h2 = [html.unescape(re.sub("<[^>]+>", "", re.sub("<small>.*?</small>", "", h))) for h in re.findall(r"<h2[^>]*>(.*?)</h2>", p.get("main_html", ""), re.S)]
            hs = [h for h in h2 if not h.startswith("Điểm cần nhớ")][:3] or hs
        return dict(topic=tp, n=n, period=pr.group(0) if pr else f"{d_}/{m}/{y}", date=f"{d_}/{m}/{y}", hs=hs[:3] or [p["summary"]])
    def latest(p, mt):
        im = p.get("image") or TH.get(p["category"], "/images/og.png")
        li = "".join(f"<li>{html.escape(h)}</li>" for h in mt["hs"])
        return (f'<a class="lt" href="/{p["slug"]}/"><img src="{html.escape(im)}" alt="" loading="lazy"><div class="in"><div class="bd"><span class="no">Số {mt["n"]:02d}</span><span class="new">MỚI NHẤT</span></div>'
                f'<h2>{html.escape(mt["topic"]) if mt["topic"] else "Kỳ " + mt["period"]}</h2><div class="sub">Phát hành {mt["date"]}</div><div class="hl">{"Nội dung chính" if mt["topic"] else "Tin chính"}</div><ul>{li}</ul><span class="more">{"Đọc bài" if mt["topic"] else "Đọc bản tin"} →</span></div></a>')
    def row(p, mt):
        return (f'<a class="rw" href="/{p["slug"]}/"><span class="no">Số {mt["n"]:02d}</span><span class="pr"><b>{html.escape(mt["topic"]) if mt["topic"] else "Kỳ " + mt["period"]}</b><em>{html.escape(mt["hs"][0])}</em></span><span class="more">Đọc →</span></a>')
    panels = ""; tabs = ""
    for k, c in enumerate(CATS):
        ps = sorted([p for p in posts if p["category"] == c], key=lambda x: x["date"])
        mts = {p["slug"]: meta(p, n + 1) for n, p in enumerate(ps)}
        ps = ps[::-1]
        tabs += f'<span role="tab" tabindex="0" class="tab{" on" if k == 0 else ""}" data-f="{k}">{html.escape(c)}</span>'
        head = f'<div class="ph"><h2>{html.escape(c)}</h2><p>{INFO[c][0]}</p><span>{INFO[c][1]} · {len(ps)} {"bài" if c in ("Phân tích chuyên sâu","Hoạt động Solvera Logistics","Breaking News") else "số"} đã phát hành</span></div>'
        if ps:
            body = latest(ps[0], mts[ps[0]["slug"]]) + ('<h3 class="oh">Các ' + ("bài" if c in ("Phân tích chuyên sâu","Hoạt động Solvera Logistics","Breaking News") else "số") + ' trước</h3><div class="rows">' + "".join(row(p, mts[p["slug"]]) for p in ps[1:]) + "</div>" if len(ps) > 1 else "")
        else:
            body = ('<div class="empty"><b>Sắp ra mắt</b><p>Hình ảnh, sự kiện và hoạt động của Solvera Logistics sẽ được cập nhật tại đây.</p></div>' if c=='Hoạt động Solvera Logistics' else '<div class="empty"><b>Chưa có tin nóng</b><p>Các tin nóng của ngành hàng hải, hàng không và xuất nhập khẩu sẽ được cập nhật tại đây ngay khi có.</p></div>' if c=='Breaking News' else '') or '<div class="empty"><b>Sắp ra mắt</b><p>Các bài phân tích chuyên gia của Solvera Logistics về hàng hải, hàng không, xuất nhập khẩu và chuỗi cung ứng sẽ được đăng tại đây.</p></div>'
        panels += f'<section class="panel" id="p{k}"{"" if k == 0 else " hidden"}>{head}{body}</section>'
    js = '<script>function sel(k){document.querySelectorAll(".tab").forEach(function(x){x.classList.toggle("on",x.dataset.f==k)});document.querySelectorAll(".panel").forEach(function(p){p.hidden=p.id!="p"+k})}var m=location.hash.match(/#c(\\d)/);if(m)sel(m[1]);document.querySelectorAll(".tab").forEach(function(t){t.onclick=function(){document.querySelectorAll(".tab").forEach(function(x){x.classList.remove("on")});t.classList.add("on");document.querySelectorAll(".panel").forEach(function(p){p.hidden=p.id!="p"+t.dataset.f})}})</script>'
    idx = (f'<div class="hero2"><div class="hw"><div class="eb">Solvera Logistics</div><h1>{SITE}</h1><p>Tin tức hàng hải, hàng không, logistics, Supply Chain và kinh doanh xuất nhập khẩu.</p></div></div>'
           f'<div class="tabs">{tabs}</div><div class="pn">{panels}</div>{js}')
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
