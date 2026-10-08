#!/usr/bin/env python3
"""Đăng NGUYÊN VẸN trang bản tin (artifact HTML) lên news site, bỏ phần Bài đăng mạng xã hội.
Dùng: python3 add_post.py <artifact.html> <slug> <yyyy-mm-dd> "<category>" "<title>" "<summary>" [image]
Giữ nguyên CSS, masthead, mục lục, KPI, tin, khuyến nghị, link nguồn của bản đã duyệt."""
import re, sys, json, pathlib
src, slug, date, cat, title, summ = sys.argv[1:7]
image = sys.argv[7] if len(sys.argv) > 7 else ""
h = pathlib.Path(src).read_text(encoding="utf8")
css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", h, re.S))
mast = re.search(r'<header class="mast">.*?</header>', h, re.S).group(0)
mast = re.sub(r"\s*(và|,)?\s*bộ bài đăng sẵn cho 4 kênh", "", mast)
mast = re.sub(r"\s*(và|,)?\s*bộ bài đăng[^<.]*", "", mast)
m = re.search(r'<main class="wrap">(.*)</main>', h, re.S)
body = m.group(1)
# cắt từ tiêu đề mục "Bài đăng" trở đi (và mọi thứ sau đó)
cut = re.search(r'<h2[^>]*>(?:(?!</h2>).)*Bài đăng', body, re.S)
if cut: body = body[:cut.start()]
body = re.sub(r'<a href="#bai-dang">.*?</a>', "", body)   # bỏ nút mục lục Bài đăng
body = re.sub(r'<script.*?</script>', "", body, flags=re.S)
body = re.sub(r'<img[^>]*data:image[^>]*>', "", body)
CONTACT_CSS = '.contact-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:14px 0 0}.ct{display:flex;flex-direction:column;gap:4px;padding:14px 16px;border-radius:12px;background:#fff;border:1px solid #d5e3e8;border-top:4px solid #0b7e93;text-decoration:none;color:#0a2a40;transition:transform .15s,box-shadow .15s}.ct span{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#0b7e93}.ct b{font-size:16px;word-break:break-word}.ct:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(10,42,64,.12)}.ct-call{background:#0a2a40;border-color:#0a2a40;border-top-color:#ff8d1c;color:#fff}.ct-call span{color:#ff8d1c}'
CONTACT = '<section class="contact" id="lien-he"><h2>Liên hệ Solvera Logistics</h2><div class="contact-grid"><a class="ct ct-call" href="tel:+84913034407"><span>Hotline</span><b>+84 913 034 407</b></a><a class="ct ct-zalo" href="https://zalo.me/84913034407" target="_blank" rel="noopener"><span>Zalo</span><b>Chat ngay</b></a><a class="ct ct-wa" href="https://wa.me/84913034407" target="_blank" rel="noopener"><span>WhatsApp</span><b>Chat ngay</b></a><a class="ct" href="mailto:admin@solveralogistics.vn"><span>Email</span><b>admin@solveralogistics.vn</b></a></div></section>'
if 'class="contact"' not in body: body += CONTACT
css += CONTACT_CSS
# thứ tự chuẩn của chị: Hàng hải, Hàng không, Xuất nhập khẩu
OLD_T = "Hàng hải, Xuất nhập khẩu & Hàng không"; NEW_T = "Hàng hải, Hàng không & Xuất nhập khẩu"
mast = mast.replace(OLD_T, NEW_T).replace(OLD_T.replace("&","&amp;"), NEW_T.replace("&","&amp;")); title = title.replace(OLD_T, NEW_T)
i1 = body.find('<h2 id="xnk"'); i2 = body.find('<h2 id="hang-khong"'); i3 = body.find('<section class="contact"')
i3 = i3 if i3 > 0 else len(body)
k = body.find('<h2 id="khuyen-nghi"')
if 0 < i1 < i2 < k:
    xnk, hk = body[i1:i2], body[i2:k]
    xnk = re.sub(r'(PHẦN )\d', r'\g<1>3', xnk, count=1); hk = re.sub(r'(PHẦN )\d', r'\g<1>2', hk, count=1)
    body = body[:i1] + hk + xnk + body[k:]
    body = re.sub(r'(<a href="#xnk">[^<]*</a>)(<a href="#hang-khong">[^<]*</a>)', r'\2\1', body)
p = pathlib.Path("posts.json")
posts = json.loads(p.read_text(encoding="utf8"))
posts = [x for x in posts if x["slug"] != slug]
posts.append(dict(slug=slug, date=date, category=cat, title=title, summary=summ, image=image,
                  body_html="", page_css=css, mast_html=mast, main_html=body))
p.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf8")
print("OK", slug, len(body), "ký tự")
