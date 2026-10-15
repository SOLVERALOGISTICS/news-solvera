"""Soạn bài fanpage Facebook từ bài Breaking News mới nhất (hoặc --slug). Ra fb/<slug>.txt + fb/<slug>.jpg (1200x630, ảnh nền thật + tiêu đề lớn)."""
import json, re, html, sys, os, textwrap
from PIL import Image, ImageDraw, ImageFont
slug = sys.argv[sys.argv.index('--slug')+1] if '--slug' in sys.argv else None
P = [p for p in json.load(open('posts.json')) if p['category'] == 'Breaking News']
p = next(x for x in P if x['slug'] == slug) if slug else sorted(P, key=lambda x: x['date'])[-1]
tx = lambda s: html.unescape(re.sub('<[^>]+>', '', s)).strip()
h3 = [re.sub(r'^\d+\.\s*','',tx(h)) for h in re.findall(r'<h3>(.*?)</h3>', p['main_html'], re.S)][:5]
url = f'https://news.solveralogistics.vn/{p["slug"]}/'
cap = f'🔴 {tx(p["title"]).upper()}\n\n{tx(p["summary"])}\n\n' + ''.join(f'▪️ {h}\n' for h in h3) + f'\n👉 Đọc đầy đủ tại: {url}\n\n📞 Solvera Logistics – Hotline/Zalo: +84 913 034 407\n\n#Solvera #SolveraLogistics #BreakingNews #Logistics #HangHai #XuatNhapKhau #HaiQuan'
os.makedirs('fb', exist_ok=True)
open(f'fb/{p["slug"]}.txt', 'w').write(cap)
im = Image.open(p['image']).convert('RGB'); W, H = 1200, 630
r = max(W/im.width, H/im.height); im = im.resize((int(im.width*r)+1, int(im.height*r)+1)); l = (im.width-W)//2; t = (im.height-H)//2
im = im.crop((l, t, l+W, t+H)).convert('RGBA')
g = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(g)
for y in range(H): d.line([(0, y), (W, y)], fill=(10, 42, 64, int(245*(y/H)**0.9)))
im = Image.alpha_composite(im, g); d = ImageDraw.Draw(im)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
ttl = tx(p['title']); ttl = re.sub(r'^Tin nóng \d+/\d+:\s*', '', ttl).upper()
fs = 60; f = ImageFont.truetype(F, fs); lines = textwrap.wrap(ttl, 24)
while len(lines) > 3: fs -= 4; f = ImageFont.truetype(F, fs); lines = textwrap.wrap(ttl, 30)
y = H-110-len(lines)*(fs+10)
for ln in lines: d.text((50, y), ln, font=f, fill='white'); y += fs+10
im.convert('RGB').save(f'fb/{p["slug"]}.jpg', quality=88); print('OK fb/' + p['slug'])
