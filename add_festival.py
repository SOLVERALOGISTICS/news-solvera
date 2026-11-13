import json,re,html,os,datetime
from PIL import Image
S="/tmp/claude-0/-home-claude/2bd2426b-fc62-57c6-b229-509972739cdf/scratchpad/"
A=glob=__import__('glob').glob("/mnt/user-data/attachments/*/")[0]
U=open(S+"u.txt").read().split("\n")
os.makedirs("images/festival-2026",exist_ok=True)
def img(i,name):
    im=Image.open(A+U[i]).convert("RGB");im.thumbnail((1400,1400));im.save(f"images/festival-2026/{name}.jpg",quality=82,optimize=True);return f"/images/festival-2026/{name}.jpg"
def fig(i,name,alt,cap):
    return f'<figure class="ff"><img src="{img(i,name)}" alt="{html.escape(alt)}" loading="lazy"><figcaption>{html.escape(cap)}</figcaption></figure>'
cover=img(17,"khai-mac")
posts=json.load(open('posts.json'))
slug="festival-lang-nghe-toan-cau-2026"
posts=[p for p in posts if p['slug']!=slug]
ref=next(p for p in posts if p['slug']=='van-tai-hang-khong-duong-bien-viet-nhat')
styles=''.join(s for s in re.findall(r'<style>.*?</style>',ref['main_html'],flags=re.S) if '.goals' in s)
contact=ref['main_html'][ref['main_html'].index('<section class="contact"'):]
css='<style>.ff{margin:20px 0}.ff img{width:100%;height:auto;border-radius:12px;display:block}.ff figcaption{font-size:.9rem;color:#0d3b3b;opacity:.8;margin-top:8px}</style>'
title="Solvera Logistics tại Festival Bảo tồn và Phát triển Làng nghề toàn cầu 2026"
summ="Đại diện Solvera Logistics có mặt tại Festival Bảo tồn và Phát triển Làng nghề toàn cầu lần thứ nhất (Hoàng thành Thăng Long, 13–16/11/2026) để gặp gỡ các nghệ nhân và đối tác tiềm năng."
d="2026-11-13"
b=[]
b.append('<p>Hôm nay (13/11/2026), đại diện <strong>Solvera Logistics</strong> tham dự ngày khai mạc <strong>Festival Bảo tồn và Phát triển Làng nghề toàn cầu lần thứ nhất năm 2026</strong> (Global Crafts Festival 2026) tại Khu di tích Hoàng thành Thăng Long, số 19C Hoàng Diệu, Ba Đình, Hà Nội. Festival diễn ra từ 13 đến 16/11/2026, do UBND Thành phố Hà Nội phối hợp cùng Bộ Nông nghiệp và Môi trường tổ chức.</p>')
b.append('<p>Chuyến đi là cơ hội để Solvera gặp gỡ trực tiếp các nghệ nhân, doanh nghiệp làng nghề và những đối tác tiềm năng đến từ nhiều quốc gia, đồng thời tìm hiểu nhu cầu vận chuyển quốc tế của nhóm hàng thủ công mỹ nghệ.</p>')
b.append('<h2 id="khai-mac">Không khí khai mạc tại Hoàng thành Thăng Long</h2>')
b.append(fig(17,"khai-mac","Lễ khai mạc Festival tại Đoan Môn, Hoàng thành Thăng Long","Khai mạc Festival trước Đoan Môn, Hoàng thành Thăng Long."))
b.append(fig(9,"cong-hoa","Cổng hoa chào mừng Festival Bảo tồn và Phát triển Làng nghề toàn cầu 2026","Cổng hoa chào mừng Festival lần thứ nhất năm 2026."))
b.append(fig(15,"solvera-cong-hoa","Đại diện Solvera Logistics tại Festival","Đại diện Solvera Logistics tại Festival."))
b.append('<h2 id="nhat-ban">Gian hàng Nhật Bản: gốm men, đồ da và trang sức thủ công</h2>')
b.append('<p>Khu gian hàng Nhật Bản gây chú ý với nhiều nghề truyền thống. Tại gian của nghệ nhân <strong>Otsuki Yutaka</strong>, những chiếc bát trà men với hoa văn như bầu trời sao, xoáy ốc và các sắc xanh, vàng ánh kim được trưng bày trên nền vải đen. Gian của <strong>Tatsuaki Koyama</strong> giới thiệu trang sức thủy tinh thủ công (Japan Wa Kawaii) như dây chuyền và hoa tai.</p>')
b.append(fig(38,"otsuki-yutaka","Gian hàng Otsuki Yutaka, Nhật Bản","Gian hàng của nghệ nhân Otsuki Yutaka (Nhật Bản)."))
b.append(fig(16,"bat-tra","Bát trà men tại gian hàng Nhật Bản","Bát trà men thủ công tại gian hàng Nhật Bản."))
b.append(fig(26,"bat-men","Bộ bát gốm men Nhật Bản","Bộ bát gốm men với nhiều sắc độ và hoa văn riêng."))
b.append(fig(6,"koyama","Gian hàng Tatsuaki Koyama, Nhật Bản","Gian hàng của Tatsuaki Koyama với trang sức thủy tinh thủ công."))
b.append('<p>Gian hàng <strong>La Fabrique CREVON</strong> (Kyoto) kết hợp kỹ thuật thủ công Pháp với truyền thống Nhật Bản: da nhuộm chàm tự nhiên (Japan Blue), gấm dệt chỉ vàng kinran và quả cầu thêu temari làm móc khóa, phụ kiện.</p>')
b.append(fig(19,"da-cham","Da nhuộm chàm tự nhiên và gấm kinran","Da nhuộm chàm tự nhiên (Japan Blue) và gấm dệt chỉ vàng kinran."))
b.append(fig(37,"temari","Quả cầu thêu temari làm móc khóa","Temari: quả cầu thêu tay mang ý nghĩa hòa hợp và may mắn."))
b.append(fig(1,"vi-da","Ví và phụ kiện da nhiều màu","Ví, túi nhỏ và phụ kiện da thủ công nhiều màu."))
b.append('<h2 id="the-gioi">Nghề thủ công từ nhiều quốc gia</h2>')
b.append('<p>Bên cạnh Nhật Bản, Festival có sự tham gia của nhiều gian hàng quốc tế và trong nước. Chúng tôi ghi lại một số nét đặc sắc: thảm kilim và dây đeo dệt thủ công của Iran (gian Zahra Bazrafkan), đồ hồ lô vẽ và khắc nhiệt, dây đeo mặt thangka, gốm mỹ nghệ, cùng nghề tò he truyền thống của Việt Nam.</p>')
b.append(fig(3,"iran","Gian hàng Iran với thảm kilim dệt thủ công","Gian hàng Iran: thảm kilim và dây đeo dệt thủ công."))
b.append(fig(12,"ho-lo-1","Hồ lô khắc nhiệt và vẽ tay","Hồ lô khắc nhiệt, vẽ tay kết hợp chạm khắc."))
b.append(fig(39,"ho-lo-2","Hồ lô vẽ hình rồng và sư tử","Hồ lô vẽ hình rồng, nhũ vàng và sư tử."))
b.append(fig(23,"thangka","Mặt dây phong cách thangka","Mặt dây chuyền theo phong cách thangka."))
b.append(fig(4,"gom-my-nghe","Gốm mỹ nghệ nhỏ xinh","Gốm mỹ nghệ: tượng mèo, đĩa trang trí và đế lót ly."))
b.append(fig(2,"to-he","Tò he truyền thống Việt Nam","Tò he, nghề thủ công truyền thống của Việt Nam."))
b.append('<h2 id="logistics">Góc nhìn logistics: vận chuyển hàng thủ công mỹ nghệ</h2>')
b.append('<p>Nhìn qua các gian hàng, có thể thấy hàng thủ công mỹ nghệ có những yêu cầu riêng khi đi quốc tế: gốm và thủy tinh dễ vỡ cần đóng gói và chằng buộc kỹ; sản phẩm da, vải, thảm cần chống ẩm; nhiều mặt hàng giá trị cao, số lượng nhỏ nên phù hợp vận chuyển hàng không hoặc hàng lẻ (LCL), trong khi đơn lớn có thể đi đường biển. Bên cạnh đó là chứng từ xuất xứ, kiểm dịch với sản phẩm từ thực vật như hồ lô, và quy định hải quan của từng thị trường.</p>')
b.append('<p>Solvera Logistics mong muốn đồng hành cùng các nghệ nhân và doanh nghiệp làng nghề trên hành trình đưa sản phẩm đi xa, với tinh thần làm logistics chân thành và tử tế. Nếu quý vị đang cần vận chuyển hàng thủ công mỹ nghệ, xin liên hệ Solvera theo thông tin bên dưới.</p>')
e=html.escape(title);dd=datetime.date.fromisoformat(d)
wd=['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật'][dd.weekday()]
rel_posts=[p for p in posts if p['category']=='Phân tích chuyên sâu'][:3]
rel='<section class="rel"><h2 id="doc-tiep">Đọc tiếp</h2>'+''.join(f'<a href="/{p["slug"]}/">{html.escape(p.get("topic") or p["title"])}<span>{html.escape(p["summary"])}</span></a>' for p in rel_posts)+'</section>'
mast=f'<header class="mast"><div class="wrap">\n  <div class="eyebrow">Solvera Logistics · Hoạt động Solvera Logistics</div>\n  <h1>{e}</h1>\n  <p>{html.escape(summ)}</p>\n  <span class="date">{wd}, {dd.day:02d}/{dd.month:02d}/{dd.year}</span>\n</div></header>'
posts.append({"slug":slug,"date":d,"category":"Hoạt động Solvera Logistics","topic":title,"title":title,"summary":summ[:155],"image":"images/festival-2026/khai-mac.jpg","body_html":"","page_css":ref['page_css'],"mast_html":mast,"main_html":styles+css+"".join(b)+rel+contact})
json.dump(posts,open('posts.json','w'),ensure_ascii=False,indent=1)
print("ok",len(posts))
