from pathlib import Path
from collections import deque
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "logos_parceiros" / "processadas"
OUT.mkdir(parents=True, exist_ok=True)

def remove_border_background(source: Path, target: Path, tolerance: int = 26):
    image = Image.open(source).convert("RGBA")
    px = image.load(); w, h = image.size
    corner = px[0, 0][:3]
    seen = set(); queue = deque([(0,0),(w-1,0),(0,h-1),(w-1,h-1)])
    def close(rgb):
        return sum((int(rgb[i])-int(corner[i]))**2 for i in range(3)) ** .5 <= tolerance
    while queue:
        x,y=queue.popleft()
        if (x,y) in seen or not (0<=x<w and 0<=y<h) or not close(px[x,y][:3]): continue
        seen.add((x,y)); px[x,y]=(px[x,y][0],px[x,y][1],px[x,y][2],0)
        queue.extend(((x+1,y),(x-1,y),(x,y+1),(x,y-1)))
    image.save(target, optimize=True)

sources = {
    "CasaDoCodigo.png": ROOT / "logos_parceiros" / "CasaDoCodigo.png",
    "hostgator.png": ROOT / "logos_parceiros" / "hostgator.png",
    "aceleradev.png": ROOT / "logos_parceiros" / "aceleradev.jpeg",
    "nexupp.png": ROOT / "logos_parceiros" / "nexupp.jpeg",
    "lamit.png": ROOT / "logos_parceiros" / "lamit.jpeg",
    "techsisters.png": ROOT / "logos_parceiros" / "techsisters.jpeg",
    "estilodeti.png": ROOT / "tmp" / "pdfs" / "estilodeti.png",
}
for name, source in sources.items():
    remove_border_background(source, OUT / name, 34 if name == "aceleradev.png" else 28)

# Acelera Dev is supplied on a square canvas around its circular identity.
# Remove only the outer canvas, preserving every pixel inside the circle.
acelera = Image.open(OUT / "aceleradev.png").convert("RGBA")
px = acelera.load(); w, h = acelera.size; cx, cy = w / 2, h / 2; radius = min(w, h) * .465
for y in range(h):
    for x in range(w):
        if ((x-cx)**2 + (y-cy)**2) ** .5 > radius:
            px[x,y] = (*px[x,y][:3], 0)
acelera.save(OUT / "aceleradev.png", optimize=True)

remove_border_background(ROOT / "elementos" / "cerejas.jpeg", ROOT / "public" / "elementos" / "cerejas.png", 42)

public = ROOT / "public" / "logos" / "processadas"
public.mkdir(parents=True, exist_ok=True)
for file in OUT.glob("*.png"):
    (public / file.name).write_bytes(file.read_bytes())
