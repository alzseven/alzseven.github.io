import sys, json, os, subprocess
from PIL import Image
S, D = sys.argv[1], sys.argv[2]
X = os.path.join(S, 'render/x/ppt/media')
assets = json.load(open(os.path.join(S, 'raw.json'), encoding='utf-8'))['assets']
mp = {}
for a in assets:
    src = os.path.join(X, a)
    base, ext = os.path.splitext(a)
    if ext == '.mp4':
        out = os.path.join(D, 'video', base + '.mp4')
        if not os.path.exists(out):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-an', '-c:v', 'libx264', '-crf', '27', '-preset', 'slow',
                            '-vf', "scale='if(gt(iw,ih),min(1280,iw),-2)':'if(gt(iw,ih),-2,min(1280,ih))'",
                            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
        mp[a] = 'video/' + base + '.mp4'
        continue
    im = Image.open(src)
    if im.mode == 'P':
        im = im.convert('RGBA')
    cap = 2200 if a in ('image8.png', 'image13.png', 'image3.png') else 1600
    if max(im.size) > cap:
        r = cap / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    out = os.path.join(D, 'img', base + '.webp')
    im.save(out, 'WEBP', quality=84, method=6)
    mp[a] = 'img/' + base + '.webp'
json.dump(mp, open(os.path.join(S, 'assetmap.json'), 'w'), indent=1)
tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(D) for f in fs)
print(len(mp), 'assets', round(tot / 1e6, 1), 'MB')
