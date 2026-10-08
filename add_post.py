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
CONTACT_CSS = ".contact-card{background:var(--surface,#eef6f8);border-left:4px solid var(--orange,#ff8d1c);border-radius:10px;padding:14px 18px;margin:8px 0 0}.contact-card p{margin:6px 0}.contact-card a{color:var(--link,#0a6d80);font-weight:700}"
CONTACT = ('<section class="contact" id="lien-he"><h2><small>LIÊN HỆ</small>Liên hệ Solvera Logistics</h2><div class="contact-card">'
 '<p>Cần tư vấn, liên hệ:</p>'
 '<p><b>Hotline / Zalo / WhatsApp:</b> <a href="tel:+84913034407">+84 913 034 407</a> · <a href="https://zalo.me/84913034407" target="_blank" rel="noopener">Zalo</a> · <a href="https://wa.me/84913034407" target="_blank" rel="noopener">WhatsApp</a></p>'
 '<p><b>Email:</b> <a href="mailto:admin@solveralogistics.vn">admin@solveralogistics.vn</a></p></div></section>')
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
