import json,re,csv,html,shutil,docx,unicodedata
N=lambda s:unicodedata.normalize('NFC',s).replace('\xa0',' ')
from PIL import Image
V='/tmp/v/'
esc=lambda s:html.escape(s.strip(),quote=False)
# ---- images
IM=[('i1','vefta-01-hanh-trinh-14-nam'),('i2','vefta-02-tom-tat-dieu-hanh'),('i3','vefta-03-chu-the-efta-viet-nam'),('i4','vefta-04-tong-quan-3-tram'),('i5','vefta-05-tram-1-dong-bang'),('i6','vefta-06-lo-trinh-thue-quan'),('i7','vefta-07-so-do-cam-ket')]
for s,n in IM:
    im=Image.open(V+s+'.jpg').convert('RGB'); im.thumbnail((1400,1400)); im.save('images/%s.jpg'%n,quality=82,optimize=True)
def fig(i,alt,cap):
    return '<figure class="fig"><img src="/images/%s.jpg" alt="%s" loading="lazy" style="width:100%%;border-radius:12px;display:block"><figcaption style="font-size:.85rem;color:#5b6b78;margin-top:6px">%s</figcaption></figure>'%(IM[i][1],alt,cap)
# ---- docx
P=[N(p.text.strip()) for p in docx.Document(V+'Nội_dung_.docx').paragraphs if p.text.strip() and not p.text.strip().isdigit()]
T=lambda k:P[k]   # 0-based index in cleaned list
def find(prefix):
    for i,t in enumerate(P):
        if t.startswith(prefix): return i
    raise KeyError(prefix)
def ps(*ks): return ''.join('<p>%s</p>'%esc(T(k)) for k in ks)
def lab(k):
    t=T(k)
    if ': ' in t[:60]:
        a,b=t.split(': ',1); return '<li><b>%s:</b> %s</li>'%(esc(a),esc(b))
    return '<li>%s</li>'%esc(t)
def ul(ks): return '<ul>'+''.join(lab(k) for k in ks)+'</ul>'
I=lambda p:find(p)
fix=lambda s:s.replace('Investor EFTA','Nhà đầu tư EFTA').replace('Đầu tư ngoài dịch vụ','Đầu tư ngoài dịch vụ')
P=[fix(t) for t in P]
a=find('Bạn có biết'); lead=P[a]+' '+P[a+1].replace('Bài học này','Bài phân tích này').split(' Sau khi hoàn thành')[0]
goals=[P[find('Phân tích lịch sử')],P[find('Đánh giá lộ trình')],P[find('Giải mã quy tắc')],P[find('Xác định các cơ hội')]]
n=lambda p:find(p)
h1=n('Chặng đường 14');h1b=n('Khối EFTA là ai');h2=n('Mở cửa Thị trường');h2a=n('Cơ cấu hàng hóa');h2b=n('Lộ trình cắt giảm');h3=n('Giải mã Quy tắc');h3a=n('Điểm đột phá');h3b=n('Chứng nhận xuất xứ');h4=n('Dịch vụ, Đầu tư');h4a=n('Thương mại Dịch vụ');h4b=n('Tiêu chuẩn Phát triển');h5=n('Tổng kết');kt=n('Tóm tắt các điểm')
main=[]
def H2(id,lbl,t): return '<h2 id="%s"><small>%s</small>%s</h2>'%(id,lbl,esc(t))
def H3(k): return '<h3>%s</h3>'%esc(P[k])
body=[]
body.append(H2('chang-duong-14-nam','PHẦN 1',P[h1]))
body.append('<article class="item">'+ps(h1+1)+'</article>')
body.append(fig(3,'Tổng quan hành trình 14 năm của VEFTA qua ba trạm: khởi động 2012, tái khởi động 8/9/2025 và ký kết 18/10/2026','Ba trạm của hành trình: 2012–2018 khởi động và đóng băng, 8/9/2025 tái khởi động tại Geneva, 18/10/2026 ký kết tại Hà Nội.'))
body.append(fig(4,'Trạm 1: khởi động đàm phán tháng 7/2012 và giai đoạn đóng băng 2012–2018','Trạm 1: khởi động tháng 7/2012 rồi chững lại sau năm 2018.'))
body.append('<article class="item">'+ps(h1+2)+'</article>')
body.append(H3(h1b)); body.append('<article class="item">'+ps(h1b+1)+ul(range(h1b+2,h1b+5))+ps(h1b+5)+'</article>')
body.append(fig(2,'Khối EFTA và Việt Nam: thế mạnh của hai bên bổ trợ cho nhau','Khối EFTA (đổi mới sáng tạo, tài chính, dược phẩm) bổ trợ cho Việt Nam (gia công, sản xuất quy mô lớn).'))
body.append(H2('mo-cua-hang-hoa','PHẦN 2',P[h2]))
body.append('<article class="item">'+ps(h2+1,h2+2)[0:0]+ps(h2+1)+'</article>')
body.append(fig(1,'Tóm tắt điều hành VEFTA: 14 năm đàm phán, khối EFTA, 4,8 tỷ EUR thương mại, mở cửa toàn diện','Bức tranh toàn cảnh VEFTA: 14 năm, khối EFTA, thương mại 4,8 tỷ EUR (2025) và mở cửa toàn diện.'))
body.append(H3(h2a)); body.append('<article class="item">'+ul([h2a+1,h2a+2])+'</article>')
body.append(H3(h2b)); body.append('<article class="item">'+ps(h2b+1)+'<p><b>%s</b></p>'%esc(P[h2b+2])+ul([h2b+3,h2b+4])+'<p><b>%s</b></p>'%esc(P[h2b+5])+ul([h2b+6,h2b+7])+'</article>')
body.append(fig(5,'Lộ trình xóa bỏ thuế quan VEFTA: khối EFTA xóa thuế ngay lập tức, Việt Nam tối đa 11 năm (công nghiệp, thủy sản) và 16 năm (nông sản)','Khối EFTA xóa thuế ngay cho hàng Việt Nam; Việt Nam xóa thuế tối đa 11 năm (công nghiệp, thủy sản) và 16 năm (nông sản chế biến).'))
body.append(H2('quy-tac-xuat-xu','PHẦN 3',P[h3]))
body.append('<article class="item">'+ps(h3+1)+'</article>')
body.append(H3(h3a)); body.append('<article class="item">'+ps(h3a+1)+ul([h3a+2,h3a+3])+'</article>')
body.append(H3(h3b)); body.append('<article class="item">'+ul([h3b+1,h3b+2])+'</article>')
lk=n('Lời khuyên cho doanh nghiệp'); a2,b2=P[lk].split(': ',1)
body.append('<div class="goals"><p><b>%s:</b> %s</p></div>'%(esc(a2),esc(b2)))
body.append(H2('dich-vu-dau-tu','PHẦN 4',P[h4]))
body.append('<article class="item">'+ps(h4+1)+'</article>')
body.append(fig(6,'Sơ đồ tư duy các cam kết chuyên sâu trong VEFTA: thương mại dịch vụ, đầu tư, sở hữu trí tuệ, mua sắm công, phát triển bền vững','Sơ đồ tư duy các cam kết chuyên sâu: dịch vụ, đầu tư, sở hữu trí tuệ, mua sắm công và phát triển bền vững.'))
body.append(H3(h4a)); body.append('<article class="item">'+ps(h4a+1)+ul([h4a+2,h4a+3])+'</article>')
body.append(H3(h4b)); body.append('<article class="item">'+ul([h4b+1,h4b+2])+'</article>')
body.append('<h2 id="tom-tat"><small>TỔNG KẾT</small>%s</h2>'%esc(P[h5]))
body.append('<article class="item">'+ps(h5+1)+'</article>')
body.append('<h3 class="kt">%s</h3><ul class="kt">'%esc(P[kt])+''.join(lab(k) for k in range(kt+1,len(P)))+'</ul>')
# ---- quiz
qd=[N(l.strip()) for p in docx.Document(V+'BT_TRẮC_NGHIỆM.docx').paragraphs for l in p.text.split('\n') if l.strip()]
Q=[];cur=None
for t in qd:
    m=re.match(r'Câu \d+: (.*?)\s*A\. (.*)',t)
    if m: cur={'q':m.group(1),'o':[m.group(2)],'a':None,'e':''};Q.append(cur);continue
    if cur is None: continue
    m=re.match(r'([BCD])\. (.*)',t)
    if m: cur['o'].append(m.group(2));continue
    m=re.match(r'Đáp án đúng: ([ABCD])',t)
    if m: cur['a']='ABCD'.index(m.group(1));continue
    m=re.match(r'Giải thích: (.*)',t)
    if m: cur['e']=m.group(1)
assert len(Q)==11 and all(len(q['o'])==4 and q['a'] is not None and q['e'] for q in Q),[len(q['o']) for q in Q]
# ---- flashcards
rows=[[N(c) for c in r] for r in csv.reader(open(V+'flashcards.csv',encoding='utf-8'))]
rows=[r for r in rows if len(r)>=2]
assert len(rows)==25
groups=[('Lịch sử đàm phán và các bên ký kết',[5,9,19]),('Thuế quan và cơ cấu hàng hóa',[1,2,20,11,17]),('Quy tắc xuất xứ và cơ chế cộng gộp',[3,21,14,16,12,15,10,6,4,7]),('Dịch vụ, đầu tư, bền vững và cơ chế thực thi',[8,13,22,23,18,24,25])]
assert sorted(sum([g[1] for g in groups],[]))==list(range(1,26))
fc='';c=0
for t,ks in groups:
    fc+='<h3 class="qh">%s</h3>'%esc(t)
    for k in ks:
        c+=1;q,a=rows[k-1]
        fc+='<details class="qz"><summary><span class="n">%d</span><span class="t">%s</span><span class="hint">Bấm xem đáp án</span></summary><div class="ans"><b>Đáp án</b>%s</div></details>'%(c,esc(q),esc(a))
# ---- template parts
P0=json.load(open('posts.json'))
tpl=[p for p in P0 if p['slug']=='json-dataformat-hai-quan-15-10-2026'][0]
m=tpl['main_html']
pre=m[:m.find('<p class="lead">')]
s1=m.find('<script>(function(){var d=document.querySelectorAll("details.qz")');e1=m.find('</script>',s1)+9
fcscript=m[s1:e1]
s2=m.find('<script>(function(){var Q=');e2=m.find('</script>',s2)
sc=m[s2:e2]
eng=sc[sc.find(';var el=document.getElementById("mc")'):]
R='[[10,"Hiền triết Logistics","Biết mình biết người, trăm trận không nguy. (Tôn Tử)"],[8,"Quân sư Hải trình","Binh quý thần tốc. (Tôn Tử)"],[6,"Môn sinh Chuỗi cung ứng","Học mà không suy thì mờ tối. (Khổng Tử)"],[3,"Lữ khách Tìm đường","Hành trình vạn dặm bắt đầu từ một bước chân. (Lão Tử)"],[0,"Học trò của Socrates","Tôi chỉ biết rằng tôi không biết gì cả. (Socrates)"]]'
qscript='<script>(function(){var Q='+json.dumps(Q,ensure_ascii=False)+',R='+R+eng+'</script>'
toc=[('chang-duong-14-nam',P[h1]),('mo-cua-hang-hoa',P[h2]),('quy-tac-xuat-xu',P[h3]),('dich-vu-dau-tu',P[h4]),('tom-tat','Tóm tắt'),('bai-tap','Bài tập thử tài logistics')]
nav='<nav class="jump" aria-label="Mục lục">'+''.join('<a href="#%s">%s</a>'%(i,esc(t)) for i,t in toc)+'</nav>'
gl='<section class="goals"><h2>Sau khi đọc xong bài phân tích này, bạn sẽ có thể</h2><ul>'+''.join('<li>%s</li>'%esc(g) for g in goals)+'</ul></section>'
tb='<h2 id="bai-tap"><small>LUYỆN TẬP</small>Bài tập thử tài logistics</h2><div class="tb2"><span class="on" data-p="mc" role="tab" tabindex="0">Trắc nghiệm <i>11 câu</i></span><span data-p="fc" role="tab" tabindex="0">Hỏi nhanh <i>25 thẻ</i></span></div><div id="pane-mc"><div class="mc" id="mc"></div></div><div id="pane-fc" hidden><div id="quizwrap"><div class="qbar" id="qbar"><span class="pg">Đã xem đáp án: <i id="qn">0</i>/25</span><span class="bt"><span id="qall">Mở tất cả</span><span id="qnone">Thu gọn</span></span><span class="pbar"><u id="qu"></u></span></div>'+fc+'</div></div>'
tail=m[m.find('<section class="rel">'):]
tail=tail.replace('</section><p class="src-note">','<a href="/json-dataformat-hai-quan-15-10-2026/">JSON DataFormat áp dụng từ 15/10/2026<span>Chuẩn dữ liệu Hải quan, phân cấp C/O và lộ trình 5 bước trên eCoSys.</span></a></section><p class="src-note">',1)
tail=re.sub(r'<p class="src-note">.*?</p>','<p class="src-note"><i>Nguồn: tổng hợp từ tài liệu phân tích Solvera Logistics về Hiệp định Thương mại Tự do Việt Nam – EFTA (VEFTA), ký ngày 18/10/2026 tại Hà Nội.</i></p>',tail,1,flags=re.S)
main_html=pre+'<p class="lead">'+esc(lead)+'</p>\n'+gl+'\n'+nav+'\n'+'\n'.join(body)+'\n'+tb+fcscript+qscript+tail
slug='vefta-hiep-dinh-viet-nam-efta-18-10-2026'
mast='<header class="mast"><div class="wrap">\n  <div class="eyebrow">Solvera Logistics · Phân tích chuyên sâu</div>\n  <h1>VEFTA: Hiệp định Việt Nam – EFTA sau 14 năm đàm phán</h1>\n  <p>Lộ trình thuế quan, quy tắc xuất xứ và cơ hội cho doanh nghiệp xuất nhập khẩu.</p>\n  <span class="date">Chủ Nhật, 18/10/2026</span>\n</div></header>'
post=dict(slug=slug,date='2026-10-18',category='Phân tích chuyên sâu',topic='Hiệp định VEFTA Việt Nam – EFTA',title='VEFTA ký sáng 18/10: Việt Nam – EFTA sau 14 năm đàm phán',summary='VEFTA ký 18/10/2026: EFTA xóa 100% thuế hàng công nghiệp, thủy sản Việt Nam; cộng gộp xuất xứ mở rộng, mở cửa dịch vụ và đầu tư.',image='images/vefta-01-hanh-trinh-14-nam.jpg',body_html='',page_css=tpl['page_css'],mast_html=mast,main_html=main_html)
print(len(post['summary']),len(post['title']))
P0=[p for p in P0 if p['slug']!=slug]
# add link to older Phân tích posts' rel
link='<a href="/%s/">Hiệp định VEFTA Việt Nam – EFTA<span>14 năm đàm phán, lộ trình thuế quan và quy tắc xuất xứ cho doanh nghiệp.</span></a>'%slug
for p in P0:
    if p['category']=='Phân tích chuyên sâu' and slug not in p['main_html']:
        p['main_html']=p['main_html'].replace('</section><p class="src-note">',link+'</section><p class="src-note">',1) if '</section><p class="src-note">' in p['main_html'] else p['main_html']
P0.insert(0,post)
json.dump(P0,open('posts.json','w'),ensure_ascii=False,indent=1)
