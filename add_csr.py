import json,re,html,os,datetime,glob
from PIL import Image
A=glob.glob("/mnt/user-data/attachments/*/")[0]
os.makedirs("images/csr-2026",exist_ok=True)
def img(f,name):
    im=Image.open(A+f+"-image.jpg").convert("RGB");im.thumbnail((1400,1400));im.save(f"images/csr-2026/{name}.jpg",quality=82,optimize=True);return f"/images/csr-2026/{name}.jpg"
def fig(f,name,alt,cap):
    return f'<figure class="ff"><img src="{img(f,name)}" alt="{html.escape(alt)}" loading="lazy"><figcaption>{html.escape(cap)}</figcaption></figure>'
posts=json.load(open('posts.json'));slug="csr-ve-sinh-moi-truong-ngay-van-hoa-viet-nam-2026"
posts=[p for p in posts if p['slug']!=slug]
ref=next(p for p in posts if p['slug']=='van-tai-hang-khong-duong-bien-viet-nhat')
styles=''.join(s for s in re.findall(r'<style>.*?</style>',ref['main_html'],flags=re.S) if '.goals' in s)
contact=ref['main_html'][ref['main_html'].index('<section class="contact"'):]
css='<style>.ff{margin:20px 0}.ff img{width:100%;height:auto;border-radius:12px;display:block}.ff figcaption{font-size:.9rem;color:#0d3b3b;opacity:.8;margin-top:8px}.hvid{display:block;width:100%;aspect-ratio:16/9;margin:18px 0;border-radius:12px;background:#0d3b3b}</style>'
C="Hoạt động CSR của Solvera Logistics"
title="Đại diện Cty Solvera Logistics tham gia cổ vũ tinh thần vệ sinh môi trường"
summ="Nhân dịp chào mừng Ngày Đại đoàn kết toàn dân tộc và Ngày Văn hóa Việt Nam 2026, Solvera Logistics hào hứng cổ vũ tinh thần làm vệ sinh môi trường."
cover=img("808a8d12","cover")
b=['<p>Doanh nghiệp muốn làm được CSR thì mỗi cá nhân, mỗi tế bào của doanh nghiệp phải tự ý thức và thể hiện được điều đó ngay tại chính nơi mình ở hay nơi làm việc.</p>',
'<p>Nhân dịp chào mừng Ngày Đại đoàn kết toàn dân tộc và Ngày Văn hóa Việt Nam năm 2026, Solvera Logistics hào hứng cổ vũ tinh thần làm vệ sinh môi trường.</p>',
'<video class="hvid" controls playsinline preload="metadata" poster="/videos/csr-ve-sinh-moi-truong.jpg" aria-label="Solvera Logistics cổ vũ tinh thần vệ sinh môi trường"><source src="/videos/csr-ve-sinh-moi-truong.mp4" type="video/mp4"></video>',
'<h2 id="van-hoa">Môi trường sạch đẹp cũng là văn hóa</h2>',
'<p>Tháng 11 là tháng của những ngày hội lớn: Ngày hội Đại đoàn kết toàn dân tộc (18/11) và Ngày Văn hóa Việt Nam (24/11), ngày được thiết lập từ năm 2021 để tôn vinh các giá trị văn hóa của dân tộc. Trong chuỗi hoạt động hưởng ứng, bên cạnh những chương trình nghệ thuật, triển lãm, lễ hội, còn có một nét văn hóa rất đời thường: giữ gìn không gian sống chung sạch đẹp.</p>',
'<p>Một lối đi được quét dọn, một sảnh nhà gọn gàng cũng là cách mỗi người thể hiện văn hóa ứng xử với cộng đồng và với môi trường. Đó là lý do Solvera Logistics chọn bắt đầu tinh thần hưởng ứng ngày hội văn hóa bằng một việc làm cụ thể, giản dị ngay trước cửa nhà.</p>',
fig("808a8d12","cover","Các cô chú cầm chổi và xẻng hót rác trước sảnh tòa nhà","Chổi, xẻng hót rác và nụ cười: một buổi sáng chung tay giữ gìn môi trường."),
'<h2 id="csr">CSR bắt đầu từ mỗi người</h2>',
'<p>Với Solvera Logistics, làm logistics là làm với sự chân thành và tử tế. Tinh thần ấy không chỉ dành cho khách hàng và đối tác, mà còn thể hiện ở cách chúng tôi chung tay giữ gìn nơi mình sống và làm việc. CSR không phải khẩu hiệu hay một chương trình lớn đặt ở đâu đó xa xôi, mà là thói quen của từng người: bỏ rác đúng chỗ, giữ sạch lối đi, sẵn sàng cầm chổi khi cần.</p>',
fig("6926be37","anh-1","Nhóm cô chú chụp ảnh cùng dụng cụ vệ sinh","Những người chung tay làm sạch khu vực trước sảnh."),
fig("76f6ac01","anh-2","Nhóm cô chú trước cửa kính tòa nhà","Tinh thần vệ sinh môi trường được lan tỏa từ những việc nhỏ."),
'<h2 id="van-hoa-nghe">Cùng tuần với những hoạt động văn hóa</h2>',
'<p>Cũng trong tuần này, Solvera Logistics đã có mặt tại <a href="/festival-lang-nghe-toan-cau-2026/">Festival Bảo tồn và Phát triển Làng nghề toàn cầu 2026</a> ở Hoàng thành Thăng Long, nơi nhiều nghệ nhân đưa các nghề thủ công truyền thống đến với công chúng. Từ việc gìn giữ làng nghề đến giữ gìn môi trường sống, chúng tôi tin rằng bảo tồn văn hóa và trách nhiệm với cộng đồng luôn đi cùng nhau.</p>',
'<p>Solvera Logistics sẽ tiếp tục cập nhật các hoạt động CSR tại chuyên mục này.</p>']
e=html.escape(title);d="2026-11-14";dd=datetime.date.fromisoformat(d)
wd=['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật'][dd.weekday()]
rp=[p for p in posts if p['slug']=='festival-lang-nghe-toan-cau-2026']+[p for p in posts if p['category']=='Phân tích chuyên sâu'][:2]
rel='<section class="rel"><h2 id="doc-tiep">Đọc tiếp</h2>'+''.join(f'<a href="/{p["slug"]}/">{html.escape(p.get("topic") or p["title"])}<span>{html.escape(p["summary"])}</span></a>' for p in rp)+'</section>'
mast=f'<header class="mast"><div class="wrap">\n  <div class="eyebrow">Solvera Logistics · {C}</div>\n  <h1>{e}</h1>\n  <p>{html.escape(summ)}</p>\n  <span class="date">{wd}, {dd.day:02d}/{dd.month:02d}/{dd.year}</span>\n</div></header>'
posts.append({"slug":slug,"date":d,"category":C,"topic":title,"title":title,"summary":summ[:155],"image":"images/csr-2026/cover.jpg","body_html":"","page_css":ref['page_css'],"mast_html":mast,"main_html":styles+css+"".join(b)+rel+contact})
json.dump(posts,open('posts.json','w'),ensure_ascii=False,indent=1);print("ok")
