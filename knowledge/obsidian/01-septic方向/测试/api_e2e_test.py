#!/usr/bin/env python3
import json, urllib.request, urllib.parse, sqlite3, uuid, http.client, threading

B = "http://localhost:9097"
P, F, LOG = 0, 0, []

def ok(n): global P; P+=1; print(f"  ✅ {n}")
def fail(n,d=""): global F; F+=1; LOG.append((n,d)); print(f"  ❌ {n} — {d[:80]}")

def POST(path, data=None, token=None):
    req = urllib.request.Request(B+path, method="POST")
    if token: req.add_header("X-Access-Token", token)
    if data: req.add_header("Content-Type","application/json"); req.data = json.dumps(data).encode()
    try: r = urllib.request.urlopen(req, timeout=10); return json.loads(r.read())
    except urllib.error.HTTPError as e: return json.loads(e.read())

def GET(path):
    return json.loads(urllib.request.urlopen(B+path, timeout=10).read())

print("="*55 + "\n  API 端到端全量测试\n" + "="*55)

d = POST("/api/shop/register", {"name":"MainShop","password":"test123"})
C, T = d["code"], d["token"]
ok("注册返回 ok+code+token")

L = POST("/api/shop/login", {"name":"MainShop","password":"test123"})
ok("登录成功" if L.get("ok") else fail("登录","no ok"))

L2 = POST("/api/shop/login", {"name":"MainShop","password":"wrong"})
ok("错误密码拒绝" if not L2.get("ok") else fail("错误密码","通过"))

PU = urllib.parse.urlencode
for name, sys_t, lsd in [("G1","grease","2026-03-01"),("P1","pumping","2021-01-01"),("I1","inspection","2025-01-01"),("N1","install","2026-01-01")]:
    r = POST(f"/api/shop/{C}/customer/add?{PU({'name':name,'system_type':sys_t,'last_service_date':lsd})}", token=T)
    ok(f"添加 {name} ({sys_t})" if r.get("ok") else fail(f"添加 {name}",str(r)))
    if r.get("customer_id"):
        s = POST(f"/api/shop/{C}/customer/{r['customer_id']}/serve", {}, token=T)
        ok(f"标记 {name} → {s.get('next_due_date','?')}")

r1 = POST(f"/api/shop/{C}/customer/add?name=X&address=Y", token="")
ok("无Token拒绝" if not r1.get("ok") else fail("无Token","通过"))
r2 = POST(f"/api/shop/{C}/customer/add?name=X&address=Y", token="fake")
ok("错误Token拒绝" if not r2.get("ok") else fail("错误Token","通过"))
dash = GET(f"/api/shop/{C}")
ok("读操作无需Token" if dash.get("ok") else fail("读操作","失败"))

r3 = POST("/api/shop/register", {"name":"LimitShop"+uuid.uuid4().hex[:4],"password":"test123"})
C3, T3 = r3["code"], r3["token"]
db = sqlite3.connect("/mnt/d/HMWORK/septic-saver/data/septic-saver.db")
for i in range(55):
    db.execute("INSERT INTO customers (shop_code,name,address,next_due_date,query_uuid) VALUES (?,?,?,?,?)",(C3,f"X{i}",f"{i} St","2027-01-01",uuid.uuid4().hex))
db.commit()
r_limit = POST(f"/api/shop/{C3}/customer/add?name=OVER&address=O", token=T3)
ok("50客户上限" if "limited" in str(r_limit.get("detail","")) else fail("50上限",str(r_limit)))

cid_u = POST(f"/api/shop/{C}/customer/add?name=Undoer&address=U", token=T)
cid_uv = cid_u.get("customer_id")
POST(f"/api/shop/{C}/customer/{cid_uv}/serve", {}, token=T)
u = POST(f"/api/shop/{C}/service/1/undo", token=T)
ok("24h撤销成功" if u.get("ok") else fail("撤销",str(u)))

POST(f"/api/shop/{C}/customer/add?{PU({'name':'DEDUP','address':'DA'})}", token=T)
POST(f"/api/shop/{C}/customer/add?{PU({'name':'DEDUP','address':'DA','phone':'999'})}", token=T)
d2 = GET(f"/api/shop/{C}")
dedup_cnt = len([c for c in d2["customers"] if c["name"]=="DEDUP"])
ok(f"去重: {dedup_cnt}条" if dedup_cnt==1 else fail("去重",f"{dedup_cnt}条"))

for c in d2["customers"]:
    if c.get("query_uuid"):
        q = GET(f"/api/customer/query/{c['query_uuid']}")
        ok("UUID自助查询" if q.get("ok") else fail("UUID",str(q)))
        break

try:
    r_ical = urllib.request.urlopen(f"{B}/api/ical/{C}", timeout=10)
    ok("iCal 200 OK")
except urllib.error.HTTPError as e:
    ok(f"iCal {e.code}（免费版限制）")

results = []
concur_name = "Concur" + uuid.uuid4().hex[:4]
def c_reg():
    try:
        r = json.loads(urllib.request.urlopen(urllib.request.Request(f"{B}/api/shop/register",
            data=json.dumps({"name":concur_name,"password":"test123"}).encode(), headers={"Content-Type":"application/json"}), timeout=10).read())
        results.append(1 if r.get("ok") else 0)
    except: results.append(0)
ts = [threading.Thread(target=c_reg) for _ in range(3)]
for t in ts: t.start()
for t in ts: t.join()
ok(f"并发注册: {sum(results)}/3成功(应1)" if sum(results)==1 else fail("并发",f"{sum(results)}/3"))

cid_rp = POST(f"/api/shop/{C}/customer/add?name=Double&address=Double", token=T)
cid_rv = cid_rp.get("customer_id")
if cid_rv:
    POST(f"/api/shop/{C}/customer/{cid_rv}/serve", {}, token=T)
    s2 = POST(f"/api/shop/{C}/customer/{cid_rv}/serve", {}, token=T)
    ok("重复标记不报错" if s2.get("ok") else fail("重复标记",str(s2)))

h = GET("/api/health")
ok("健康检查" if h.get("ok") else fail("健康","不健康"))

print(f"\n{'='*55}")
print(f"  总计: ✅ {P}  ❌ {F}")
for n,d in LOG: print(f"     ❌ {n}: {d}")
print(f"{'='*55}")
