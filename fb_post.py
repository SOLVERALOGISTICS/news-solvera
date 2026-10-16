"""Soạn bài fanpage Facebook từ bài Breaking News mới nhất (hoặc --slug). Ra fb/<slug>.txt + fb/<slug>.jpg (1200x630, ảnh nền thật + tiêu đề lớn)."""
import json, re, html, sys, os, textwrap
from PIL import Image, ImageDraw, ImageFont
slug = sys.argv[sys.argv.index('--slug')+1] if '--slug' in sys.argv else None
P = [p for p in json.load(open('posts.json')) if p['category'] == 'Breaking News']
p = next(x for x in P if x['slug'] == slug) if slug else sorted(P, key=lambda x: x['date'])[-1]
tx = lambda s: html.unescape(re.sub('<[^>]+>', '', s)).strip()
h3 = [re.sub(r'^\d+\.\s*','',tx(h)) for h in re.findall(r'<h3>(.*?)</h3>', p['main_html'], re.S)][:5]
url = f'https://news.solveralogistics.vn/{p["slug"]}/'
cap = f'🔴 {tx(p["title"]).upper()}\n\n{tx(p["summary"])}\n\n' + ''.join(f'▪️ {h}\n' for h in h3) + f'\n👉 Đọc đầy đủ tại: {url}\n\n#Solvera #SolveraLogistics #BreakingNews #Logistics #HangHai #XuatNhapKhau #HaiQuan\n\n--------///---------\n\n📞 Contact Us:\n- Hotline: +84 913 034 407\n- Email: admin@solveralogistics.vn\n- Website: https://solveralogistics.vn\n\n🌐 Connect with us:\n- LinkedIn: https://www.linkedin.com/company/solvera-logistics/\n- YouTube: https://www.youtube.com/@SOLVERALOGISTICS\n- Facebook: https://www.facebook.com/share/1CQrtY27t4/?mibextid=wwXIfr\n- Zalo: https://zalo.me/2938397457262576692\n- TikTok: https://www.tiktok.com/@solveralogistics\n- News: https://news.solveralogistics.vn'
os.makedirs('fb', exist_ok=True)
open(f'fb/{p["slug"]}.txt', 'w').write(cap)
W, H = 1200, 630
im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
for y in range(H):
    k = y/H; d.line([(0, y), (W, y)], fill=(int(10+8*k), int(42+14*k), int(64+20*k)))
d.rectangle([0, 0, 14, H], fill=(224, 123, 32))
lg = Image.open('images/logo.png').convert('RGBA'); lg.thumbnail((300, 110))
im.paste(lg, (46, 40), lg)
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
d.rounded_rectangle([50, 200, 330, 256], 8, fill=(200, 30, 40)); d.text((72, 212), 'BREAKING NEWS', font=ImageFont.truetype(F, 28), fill='white')
ttl = tx(p['title']); ttl = re.sub(r'^Tin nóng \d+/\d+:\s*', '', ttl).upper()
fs = 60; f = ImageFont.truetype(F, fs); lines = textwrap.wrap(ttl, 26)
while len(lines) > 3: fs -= 4; f = ImageFont.truetype(F, fs); lines = textwrap.wrap(ttl, 32)
y = 290
for ln in lines: d.text((50, y), ln, font=f, fill='white'); y += fs+14
d.text((50, H-60), 'news.solveralogistics.vn', font=ImageFont.truetype(F, 26), fill=(224, 123, 32))
im.save(f'fb/{p["slug"]}.jpg', quality=90); im.save(f'images/fb-{p["slug"]}.jpg', quality=90)
