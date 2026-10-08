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
p = pathlib.Path("posts.json")
posts = json.loads(p.read_text(encoding="utf8"))
posts = [x for x in posts if x["slug"] != slug]
posts.append(dict(slug=slug, date=date, category=cat, title=title, summary=summ, image=image,
                  body_html="", page_css=css, mast_html=mast, main_html=body))
p.write_text(json.dumps(posts, ensure_ascii=False, indent=1), encoding="utf8")
print("OK", slug, len(body), "ký tự")
