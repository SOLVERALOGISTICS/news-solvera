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
C="Hoạt động Solvera Logistics"
title="Bà Nguyễn Thị Tú Quỳnh, Phó Tổng Giám đốc Solvera Logistics, tham gia cổ vũ tinh thần vệ sinh môi trường"
summ="Nhân dịp chào mừng Ngày Đại đoàn kết toàn dân tộc và Ngày Văn hóa Việt Nam 2026, Solvera Logistics chung tay giữ gìn môi trường sống, bắt đầu từ chính nơi mình ở và làm việc."
cover=img("808a8d12","cover")
def P(t): return '<p>'+t+'</p>'
def H(i,t): return f'<h2 id="{i}">{t}</h2>'
fg=lambda f,n,al,c: f'<figure class="ff"><img src="/images/csr-2026/{n}.jpg" alt="{html.escape(al)}" loading="lazy"><figcaption>{html.escape(c)}</figcaption></figure>'
b=[P('Doanh nghiệp muốn làm được CSR thì mỗi cá nhân, mỗi tế bào của doanh nghiệp phải tự ý thức và thể hiện được điều đó ngay tại chính nơi mình ở hay nơi làm việc.'),
P('Nhân dịp chào mừng Ngày Đại đoàn kết toàn dân tộc và Ngày Văn hóa Việt Nam năm 2026, bà Nguyễn Thị Tú Quỳnh, Phó Tổng Giám đốc Solvera Logistics, hào hứng cổ vũ tinh thần làm vệ sinh môi trường.'),
'<video class="hvid" controls playsinline preload="metadata" poster="/videos/csr-ve-sinh-moi-truong.jpg" aria-label="Solvera Logistics cổ vũ tinh thần vệ sinh môi trường"><source src="/videos/csr-ve-sinh-moi-truong.mp4" type="video/mp4"></video>',
H('thang-11','Tháng 11: tháng của những ngày hội lớn'),
P('Tháng 11 là thời điểm cả nước cùng hướng về hai ngày có ý nghĩa đặc biệt. Ngày hội Đại đoàn kết toàn dân tộc (18/11) nhắc chúng ta về sức mạnh của sự chung tay, cộng đồng gắn bó. Ngày Văn hóa Việt Nam (24/11), được thiết lập từ năm 2021, gợi nhớ Hội nghị văn hóa toàn quốc năm 1946 và tôn vinh các giá trị văn hóa của dân tộc. Quanh hai ngày này là chuỗi hoạt động hưởng ứng ở khắp nơi, từ chương trình nghệ thuật, triển lãm, lễ hội đến các phong trào cộng đồng.'),
fg(0,'cover','Các cô chú cầm chổi và xẻng hót rác trước sảnh tòa nhà','Chổi, xẻng hót rác và nụ cười: một buổi sáng chung tay giữ gìn môi trường.'),
H('van-hoa','Văn hóa không chỉ ở bảo tàng và lễ hội'),
P('Nói đến văn hóa, nhiều người nghĩ ngay đến di tích, lễ hội, làng nghề. Nhưng văn hóa còn nằm trong cách ứng xử hằng ngày: giữ gìn lối đi chung, không xả rác, biết dọn dẹp nơi mình đã dùng. Một không gian sạch sẽ, gọn gàng là cách giản dị nhất để mỗi người thể hiện sự tôn trọng với cộng đồng. Vì vậy, Solvera Logistics chọn bắt đầu tinh thần hưởng ứng ngày hội văn hóa bằng một việc làm cụ thể: cầm chổi, hót rác, làm sạch khu vực trước cửa nhà.'),
H('csr','CSR không bắt đầu từ báo cáo, mà từ thói quen'),
P('CSR (trách nhiệm xã hội của doanh nghiệp) thường được hiểu qua ba mảng: kinh tế, xã hội và môi trường. Nhưng một doanh nghiệp không thể nói về trách nhiệm với xã hội nếu từng người trong đó chưa quen với trách nhiệm trong những việc rất nhỏ. Bỏ rác đúng chỗ, giữ sạch nơi làm việc, sẵn sàng cầm chổi khi cần: những thói quen ấy, nhân lên theo số lượng người, mới tạo thành văn hóa doanh nghiệp. Chúng tôi tin CSR bền vững được xây từ dưới lên, từ mỗi "tế bào" của doanh nghiệp.'),
fg(1,'anh-1','Nhóm cô chú chụp ảnh cùng dụng cụ vệ sinh','Những người chung tay làm sạch khu vực trước sảnh.'),
H('cam-ket','Cam kết của một công ty logistics với môi trường'),
P('Logistics vận hành bằng tàu, xe, máy bay và kho bãi, nên tác động đến môi trường là điều Solvera Logistics luôn ý thức. Chúng tôi hướng đến hai cam kết cụ thể trong công việc hằng ngày:'),
'<ul><li><strong>Giảm giấy:</strong> ưu tiên chứng từ điện tử, trao đổi và lưu trữ hồ sơ số, hạn chế in ấn không cần thiết. Mỗi bộ chứng từ không in ra là bớt một phần giấy, mực và công vận chuyển.</li><li><strong>Đóng gói xanh:</strong> đóng gói vừa đủ, hợp lý, ưu tiên vật liệu tái sử dụng hoặc tái chế khi điều kiện hàng hóa cho phép. Vừa bảo vệ hàng, vừa giảm rác thải đến tay khách hàng.</li></ul>',
P('Từ việc quét dọn trước cửa nhà đến cách tổ chức một chuyến hàng, tinh thần là một: làm có trách nhiệm.'),
fg(2,'anh-2','Nhóm cô chú trước cửa kính tòa nhà','Tinh thần vệ sinh môi trường được lan tỏa từ những việc nhỏ.'),
H('tu-te','Chân thành và tử tế, bắt đầu từ việc nhỏ'),
P('Solvera Logistics theo đuổi triết lý làm logistics bằng sự chân thành và tử tế. Tử tế với khách hàng, đối tác, và cả với nơi mình sinh sống. Một buổi sáng chung tay làm sạch môi trường tuy không lớn, nhưng là minh chứng rằng giá trị ấy được thực hành chứ không chỉ nằm trên giấy.'),
H('van-hoa-nghe','Cùng tuần với những hoạt động văn hóa'),
P('Cũng trong tuần này, Solvera Logistics có mặt tại <a href="/festival-lang-nghe-toan-cau-2026/">Festival Bảo tồn và Phát triển Làng nghề toàn cầu 2026</a> ở Hoàng thành Thăng Long, nơi nhiều nghệ nhân đưa nghề thủ công truyền thống đến với công chúng. Từ gìn giữ làng nghề đến giữ gìn môi trường sống, bảo tồn văn hóa và trách nhiệm với cộng đồng luôn đi cùng nhau. Solvera sẽ tiếp tục cập nhật các hoạt động CSR tại chuyên mục này.')]
e=html.escape(title);d="2026-11-14";dd=datetime.date.fromisoformat(d)
wd=['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ Nhật'][dd.weekday()]
rp=[p for p in posts if p['slug']=='festival-lang-nghe-toan-cau-2026']+[p for p in posts if p['category']=='Phân tích chuyên sâu'][:2]
rel='<section class="rel"><h2 id="doc-tiep">Đọc tiếp</h2>'+''.join(f'<a href="/{p["slug"]}/">{html.escape(p.get("topic") or p["title"])}<span>{html.escape(p["summary"])}</span></a>' for p in rp)+'</section>'
mast=f'<header class="mast"><div class="wrap">\n  <div class="eyebrow">Solvera Logistics · {C}</div>\n  <h1>{e}</h1>\n  <p>{html.escape(summ)}</p>\n  <span class="date">{wd}, {dd.day:02d}/{dd.month:02d}/{dd.year}</span>\n</div></header>'
posts.append({"slug":slug,"date":d,"category":C,"sub":"CSR","topic":title,"title":title,"summary":summ[:155],"image":"images/csr-2026/cover.jpg","body_html":"","page_css":ref['page_css'],"mast_html":mast,"main_html":styles+css+"".join(b)+rel+contact})
json.dump(posts,open('posts.json','w'),ensure_ascii=False,indent=1);print("ok")
