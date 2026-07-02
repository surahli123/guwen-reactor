#!/usr/bin/env python3
"""Build accurate China map geometry for the 山河卷 SVG (viewBox 1600x900).
Source: Natural Earth 50m (public domain). Projection: Albers equal-area conic,
standard parallels 25N/47N, central meridian 105E (standard for China maps).
Outputs mapgeo.js with: LAND path, RIVERS paths, projected RANGES, station PTS."""
import json, math, os, sys, urllib.request

S = os.path.dirname(os.path.abspath(__file__))
BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
FILES = {"countries": "ne_50m_admin_0_countries.geojson",
         "rivers": "ne_50m_rivers_lake_centerlines.geojson"}

for k, f in FILES.items():
    p = os.path.join(S, f)
    if not os.path.exists(p):
        print("downloading", f, "...", flush=True)
        urllib.request.urlretrieve(BASE + f, p)
    print(k, os.path.getsize(p), "bytes")

# ---------- Albers equal-area conic ----------
p1, p2 = math.radians(25), math.radians(47)
lam0 = math.radians(105)
n = (math.sin(p1) + math.sin(p2)) / 2
C = math.cos(p1) ** 2 + 2 * n * math.sin(p1)
rho0 = math.sqrt(C) / n  # phi0 = 0

def proj(lon, lat):
    lam, phi = math.radians(lon), math.radians(lat)
    rho = math.sqrt(C - 2 * n * math.sin(phi)) / n
    th = n * (lam - lam0)
    return rho * math.sin(th), rho0 - rho * math.cos(th)

# ---------- collect China (+ Taiwan) rings ----------
cj = json.load(open(os.path.join(S, FILES["countries"])))
rings = []
for ft in cj["features"]:
    name = ft["properties"].get("ADMIN") or ft["properties"].get("admin") or ""
    if name not in ("China", "Taiwan"):
        continue
    geom = ft["geometry"]
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        rings.append(poly[0])  # outer ring only

# project, find bbox
prings = [[proj(x, y) for x, y in r] for r in rings]
xs = [p[0] for r in prings for p in r]; ys = [p[1] for r in prings for p in r]
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
# fit into 1600x900 with margins (map slightly low-center, sky above)
MX0, MX1, MY0, MY1 = 100, 1560, 120, 858
sc = min((MX1 - MX0) / (maxx - minx), (MY1 - MY0) / (maxy - miny))
ox = MX0 + ((MX1 - MX0) - (maxx - minx) * sc) / 2
oy = MY0 + ((MY1 - MY0) - (maxy - miny) * sc) / 2

def to_svg(pt):
    return (ox + (pt[0] - minx) * sc, oy + (maxy - pt[1]) * sc)  # y flipped

def ring_area(r):
    a = 0
    for i in range(len(r) - 1):
        a += r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1]
    return abs(a) / 2

# Douglas-Peucker
def dp(pts, tol):
    if len(pts) < 3: return pts
    def d2(p, a, b):
        ax, ay = a; bx, by = b; px, py = p
        dx, dy = bx - ax, by - ay
        if dx == dy == 0: return (px - ax) ** 2 + (py - ay) ** 2
        t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
        qx, qy = ax + t * dx, ay + t * dy
        return (px - qx) ** 2 + (py - qy) ** 2
    keep = [False] * len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i0, i1 = stack.pop()
        best, bi = -1, -1
        for i in range(i0 + 1, i1):
            dd = d2(pts[i], pts[i0], pts[i1])
            if dd > best: best, bi = dd, i
        if best > tol * tol:
            keep[bi] = True
            stack.append((i0, bi)); stack.append((bi, i1))
    return [p for p, k in zip(pts, keep) if k]

svg_rings = []
for r in prings:
    sr = [to_svg(p) for p in r]
    if ring_area(sr) < 60:  # drop islets < ~60px² (keep mainland, Taiwan, Hainan)
        continue
    svg_rings.append(dp(sr, 1.3))
svg_rings.sort(key=ring_area, reverse=True)
print("kept rings:", len(svg_rings), "sizes:", [len(r) for r in svg_rings])

def path_of(rr):
    out = []
    for r in rr:
        out.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in r) + " Z")
    return " ".join(out)

LAND = path_of(svg_rings)

# ---------- rivers: Yangtze + Huang He ----------
rj = json.load(open(os.path.join(S, FILES["rivers"])))
def river_paths(match):
    segs = []
    for ft in rj["features"]:
        nm = (ft["properties"].get("name") or "") + "|" + (ft["properties"].get("name_en") or "")
        if match.lower() not in nm.lower(): continue
        g = ft["geometry"]
        lines = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
        for ln in lines:
            pts = [to_svg(proj(x, y)) for x, y in ln]
            pts = dp(pts, 1.5)
            if len(pts) > 1:
                segs.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts))
    return " ".join(segs)
YANGTZE = river_paths("Yangtze")
HUANGHE = river_paths("Huang")
print("yangtze len", len(YANGTZE), "| huanghe len", len(HUANGHE))

# ---------- story locations (考订,见凡例;史源见工作流/册页) ----------
PTS_LL = {
    "G01": (118.75, 36.50),  # 北海朱虛(今山东临朐/安丘一带)— 管寧籍贯
    "G02": (118.78, 32.04),  # 建康(今南京)— 謝氏寓所
    "G03": (118.35, 35.05),  # 琅琊臨沂(今山东临沂)— 王戎籍贯
}
PTS = {}
for k, (lo, la) in PTS_LL.items():
    x, y = to_svg(proj(lo, la))
    PTS[k] = [round(x, 1), round(y, 1), round(x / 16, 2), round(y / 9, 2)]  # svg + %
    print(k, PTS[k])

# ---------- mountain spines by real lon/lat, projected ----------
def spine(*ll): return [list(map(lambda v: round(v, 1), to_svg(proj(lo, la)))) for lo, la in ll]
RANGES = [
 dict(pts=spine((73.8,38.5),(75.5,37.2),(76.5,36.0)), rows=3,h=22,step=15,f="qd",op=.9, ink=1),  # 帕米尔
 dict(pts=spine((76,42.3),(83,43.2),(89,43.4),(94,43.0)), rows=3,h=26,step=18,f="q",op=.9,ink=1), # 天山
 dict(pts=spine((85.5,48.4),(88.5,48.0),(90.5,47.2)), rows=2,h=20,step=16,f="q",op=.7,ink=0),     # 阿尔泰
 dict(pts=spine((75.5,36.6),(82,36.0),(89,35.8),(96,35.6)), rows=3,h=26,step=18,f="q",op=.92,ink=1), # 昆仑
 dict(pts=spine((76.5,35.6),(78.5,35.0),(80.5,34.5)), rows=2,h=26,step=15,f="qd",op=.9,ink=1),    # 喀喇昆仑
 dict(pts=spine((80,33.8),(85,33.6),(90,33.4),(93,33.0)), rows=2,h=24,step=17,f="q",op=.9,ink=0), # 羌塘/唐古拉
 dict(pts=spine((84,30.6),(89,30.3),(93,30.0),(95.5,29.6)), rows=2,h=26,step=16,f="qd",op=.92,ink=1), # 念青唐古拉
 dict(pts=spine((80,31.4),(84,31.2),(87.5,31.0)), rows=2,h=24,step=16,f="q",op=.9,ink=0),          # 冈底斯
 dict(pts=spine((77,28.6),(82,28.3),(87,28.0),(92,28.0),(95,28.6)), rows=2,h=30,step=15,f="qd",op=.95,ink=1), # 喜马拉雅
 dict(pts=spine((94.5,39.4),(98.5,38.8),(102.5,37.6)), rows=2,h=22,step=16,f="q",op=.8,ink=0),     # 祁连
 dict(pts=spine((98.8,31.8),(99.2,29.8),(99.6,27.8)), rows=2,h=26,step=14,f="qd",op=.9,ink=1),     # 横断北(纵)
 dict(pts=spine((100.2,28.6),(100.6,26.8),(101.2,25.2)), rows=2,h=25,step=14,f="q",op=.85,ink=0),  # 横断南(纵)
 dict(pts=spine((107.5,41.2),(110,41.4),(112.5,41.0)), rows=1,h=16,step=18,f="far",op=.55,ink=0),  # 阴山
 dict(pts=spine((105.8,39.3),(106.1,38.2)), rows=1,h=17,step=13,f="q",op=.68,ink=0),               # 贺兰
 dict(pts=spine((106.4,36.4),(106.2,35.2)), rows=1,h=15,step=13,f="q",op=.65,ink=0),               # 六盘
 dict(pts=spine((111.3,39.0),(111.6,37.4),(111.2,36.2)), rows=1,h=18,step=14,f="q",op=.7,ink=0),   # 吕梁
 dict(pts=spine((114.4,39.6),(113.6,37.6),(112.8,35.8)), rows=1,h=20,step=15,f="qd",op=.75,ink=0), # 太行
 dict(pts=spine((115.5,40.8),(117.3,40.6),(119.2,40.4)), rows=2,h=18,step=15,f="q",op=.7,ink=0),   # 燕山
 dict(pts=spine((104,33.9),(107.5,33.7),(111.5,33.6)), rows=2,h=24,step=17,f="lud",op=.9,ink=1),   # 秦岭
 dict(pts=spine((106.5,32.4),(109,32.2),(111,32.0)), rows=1,h=17,step=16,f="lu",op=.8,ink=0),      # 大巴
 dict(pts=spine((103,26.8),(104.8,26.2),(106.5,25.8)), rows=3,h=20,step=15,f="lu",op=.8,ink=0),    # 云贵
 dict(pts=spine((101.4,24.6),(102.5,23.8),(103.5,23.2)), rows=1,h=16,step=14,f="lu",op=.7,ink=0),  # 哀牢
 dict(pts=spine((109.5,29.2),(110.2,28.2),(110.8,27.4)), rows=2,h=18,step=15,f="lu",op=.78,ink=0), # 武陵雪峰
 dict(pts=spine((110.5,25.6),(112.5,25.2),(114.2,25.2)), rows=2,h=20,step=16,f="lu",op=.85,ink=1), # 南岭
 dict(pts=spine((116.2,27.8),(117.2,26.6),(118.2,25.4)), rows=2,h=24,step=14,f="lud",op=.85,ink=0),# 武夷
 dict(pts=spine((113.9,27.6),(114.1,26.4)), rows=1,h=16,step=14,f="lu",op=.7,ink=0),               # 罗霄
 dict(pts=spine((115.2,31.4),(116.4,31.1)), rows=1,h=14,step=14,f="lud",op=.7,ink=0),              # 大别
 dict(pts=spine((119.2,30.3),(120.6,29.8)), rows=1,h=12,step=13,f="pale",op=.6,ink=0),             # 天目会稽
 dict(pts=spine((117.4,36.4),(118.6,36.3)), rows=1,h=11,step=14,f="pale",op=.6,ink=0),             # 鲁中
 dict(pts=spine((120.8,52.5),(121.8,50.0),(120.5,47.5),(119.5,46.0)), rows=2,h=22,step=15,f="q",op=.8,ink=1), # 大兴安岭(纵)
 dict(pts=spine((127,49.2),(129,48.2),(130.5,47.4)), rows=1,h=16,step=16,f="pale",op=.6,ink=0),    # 小兴安岭
 dict(pts=spine((126.8,42.6),(127.8,42.0),(128.6,41.6)), rows=2,h=20,step=15,f="lud",op=.85,ink=0),# 长白
 dict(pts=spine((121.2,24.6),(121.0,23.4)), rows=1,h=14,step=12,f="lud",op=.85,ink=0),             # 台湾中央山脉(纵)
 dict(pts=spine((109.5,19.2),(110.0,18.8)), rows=1,h=10,step=11,f="lu",op=.75,ink=0),              # 五指山
]

# 平原/大漠 tint 椭圆(lon/lat 中心 → svg)
def ell(lo,la,rx,ry,fill,op):
    x,y=to_svg(proj(lo,la)); return dict(cx=round(x,1),cy=round(y,1),rx=rx,ry=ry,fill=fill,op=op)
TINTS=[ell(83,39.5,150,42,"#e8d5a2",.9), ell(105,42.5,160,36,"#e3d2a4",.7),
       ell(115.5,36.5,100,62,"#e9ddb4",.85), ell(124.5,45.5,80,64,"#e6dbb2",.8),
       ell(105,30.5,62,40,"#d3d3a6",.7)]

# 平原撒丘框(经纬两角 → svg 两角)
def box(lo1,la1,lo2,la2):
    x1,y1=to_svg(proj(lo1,la1)); x2,y2=to_svg(proj(lo2,la2))
    return [round(min(x1,x2),1),round(min(y1,y2),1),round(max(x1,x2),1),round(max(y1,y2),1)]
PLAINS=[box(113,39,119,33.5),box(115,33.5,120.5,28),box(122,48,128,43),
        box(104,43.5,118,40),box(102,37,107,34),box(106,35.5,112,33),
        box(96,42.5,104,40),box(112,44,120,41.5)]

# 魏晋要地(静默标注,denseButQuiet):真实经纬 → svg
CITY_LL={"洛陽":(112.45,34.62),"長安":(108.94,34.26),"會稽":(120.58,30.00)}
CITIES={k:[round(v,1) for v in to_svg(proj(*ll))] for k,ll in CITY_LL.items()}

# 河名标注位(晋陕峡谷段/荆江段)
RIVLBL={"黃河":[round(v,1) for v in to_svg(proj(110.6,37.8))],"長江":[round(v,1) for v in to_svg(proj(112.3,30.1))]}

out = {"LAND": LAND, "YANGTZE": YANGTZE, "HUANGHE": HUANGHE, "PTS": PTS,
       "RANGES": RANGES, "TINTS": TINTS, "PLAINS": PLAINS, "CITIES": CITIES, "RIVLBL": RIVLBL}
open(os.path.join(S, "mapgeo.js"), "w").write("const GEO=" + json.dumps(out, ensure_ascii=False) + ";")
print("mapgeo.js written:", os.path.getsize(os.path.join(S, "mapgeo.js")), "bytes")
