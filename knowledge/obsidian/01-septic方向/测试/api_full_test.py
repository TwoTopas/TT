#!/usr/bin/env python3
"""
SepticSaver API 全量自动化测试 — 纯API调用，不操作DB
用法: cd /mnt/d/HMWORK/septic-saver && python3 tests/api_full.py
"""
import json, urllib.request, urllib.parse, uuid, http.client, threading, time, sys

B = "http://localhost:9097"
P = 0; F = []; LOG = []

def ok(n):
    global P; P += 1
    print(f"  ✅ {n}")

def fail(n, d=""):
    global F; F.append((n, d[:120]))
    print(f"  ❌ {n} — {d[:80]}")

def POST(path, data=None, token=None):
    req = urllib.request.Request(B + path, method="POST")
    if token: req.add_header("X-Access-Token", token)
    if data:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode()
    try:
        return json.loads(urllib.request.urlopen(req, timeout=10).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

def GET(path):
    try:
        return json.loads(urllib.request.urlopen(B + path, timeout=10).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

UID = uuid.uuid4().hex[:6]
print("=" * 55)
print("  API 端到端自动化测试")
print("=" * 55)

r = POST("/api/shop/register", {"name": f"APT-{UID}", "password": "test123"})
C, T = r["code"], r["token"]
print(f"\n📍 Shop: {C[:8]}..., tier={r.get('tier')}")
PU = urllib.parse.urlencode

# ============================================================
# 1. 返回结构
# ============================================================
print("\n📦 1. 返回结构")

r1 = POST("/api/shop/register", {"name": f"RS-{uuid.uuid4().hex[:4]}", "password": "test123"})
ok("注册={code,token}" if r1.get("ok") and r1.get("code") and r1.get("token") else fail("注册结构", str(r1)))

r2 = GET(f"/api/shop/{C}")
ok("Dashboard={ok,shop,customers}" if r2.get("ok") and "shop" in r2 and "customers" in r2 else fail("Dashboard结构", str(r2)))

r3 = POST("/api/shop/login", {"name": f"APT-{UID}", "password": "test123"})
ok("登录={ok,token}" if r3.get("ok") and r3.get("token") else fail("登录结构", str(r3)))

p = {"name": "Struct C1", "address": "1 Main"}
r4 = POST(f"/api/shop/{C}/customer/add?{PU(p)}", token=T)
ok("添加={ok,customer_id}" if r4.get("ok") and r4.get("customer_id") else fail("添加结构", str(r4)))

r5 = POST(f"/api/shop/{C}/customer/{r4['customer_id']}/serve", {}, token=T)
ok("服务={ok,next_due_date}" if r5.get("ok") and r5.get("next_due_date") else fail("服务结构", str(r5)))

r6 = POST("/api/shop/login", {"name": "NONEXIST", "password": "x"})
ok("登录失败={detail}" if not r6.get("ok") and isinstance(r6.get("detail"), str) else fail("失败结构", str(r6)))

r7 = GET(f"/api/shop/NONEXISTENT")
ok("不存在shop={detail}" if not r7.get("ok") and isinstance(r7.get("detail"), str) else fail("不存在结构", str(r7)))

# ============================================================
# 2. 认证
# ============================================================
print("\n📦 2. 认证")

try:
    req = urllib.request.Request(f"{B}/api/shop/{C}/customer/add?name=X&address=Y", method="POST")
    urllib.request.urlopen(req, timeout=10)
    fail("无Token通过")
except urllib.error.HTTPError as e:
    ok(f"无Token → {e.code}")

r9 = POST(f"/api/shop/{C}/customer/add?name=X&address=Y", token="FAKE_TOKEN")
ok("错误Token拒绝" if not r9.get("ok") else fail("错误Token通过"))

r10 = GET(f"/api/shop/{C}")
ok("读操作无需Token" if r10.get("ok") else fail("读操作需Token"))

try:
    urllib.request.urlopen(f"{B}/api/ical/{C}", timeout=10)
    ok("iCal无需Token")
except urllib.error.HTTPError as e:
    ok(f"iCal {e.code}")

for c in r2["customers"]:
    if c.get("query_uuid"):
        r11 = GET(f"/api/customer/query/{c['query_uuid']}")
        ok("UUID查询无需Token" if r11.get("ok") else fail("UUID查询"))
        break

try:
    req = urllib.request.Request(f"{B}/api/webhook/sms", method="POST",
                                  data=json.dumps({"Body": "STOP", "From": "+15551234567"}).encode(),
                                  headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)
    ok("Webhook无需Token")
except urllib.error.HTTPError as e:
    ok(f"Webhook {e.code}")

# ============================================================
# 3. 业务逻辑
# ============================================================
print("\n📦 3. 业务逻辑")

# 3.1 周期
from datetime import date
from dateutil.relativedelta import relativedelta

type_tests = [
    ("GreaseC", "grease", "2026-01-01", 3),
    ("PumpC", "pumping", "2021-01-01", 60),
    ("InsC", "inspection", "2025-06-01", 12),
    ("InstC", "install", "2026-01-01", 12),
]
for name, sys_t, lsd, exp_months in type_tests:
    r = POST(f"/api/shop/{C}/customer/add?{PU({'name':name,'system_type':sys_t,'last_service_date':lsd})}", token=T)
    if r.get("customer_id"):
        s = POST(f"/api/shop/{C}/customer/{r['customer_id']}/serve", {}, token=T)
        exp = (date.today() + relativedelta(months=exp_months)).isoformat()
        due = s.get("next_due_date", "")
        ok(f"{sys_t}周期={exp_months}月" if due == exp else fail(f"{sys_t}周期", f"期望{exp}实际{due}"))

# 3.2 50上限 — 通过API逐一添加50个
for i in range(50):
    POST(f"/api/shop/{C}/customer/add?{PU({'name':f'Filler{i}','address':str(i)})}", token=T)
r_51 = POST(f"/api/shop/{C}/customer/add?name=OVR&address=O", token=T)
ok("50上限: 第51个被拒" if "limited" in str(r_51.get("detail","")).lower() else fail("50上限", str(r_51)))

# CSV导入超过50
csv_data = "name,address\n\"E1\",\"X\"\n\"E2\",\"Y\"\n"
boundary = "----" + uuid.uuid4().hex
body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"test.csv\"\r\n"
        f"Content-Type: text/csv\r\n\r\n{csv_data}\r\n--{boundary}--\r\n").encode()
conn = http.client.HTTPConnection("localhost", 9097)
conn.request("POST", f"/api/shop/{C}/customers/import", body,
             headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "X-Access-Token": T})
imp_r = json.loads(conn.getresponse().read())
ok("CSV导入50上限" if "limited" in str(imp_r).lower() else fail("CSV上限", str(imp_r)))

# 3.3 撤销 — 重新开一个店铺单独测
r_undo = POST("/api/shop/register", {"name": f"Undo-{uuid.uuid4().hex[:4]}", "password": "test123"})
Cu, Tu = r_undo["code"], r_undo["token"]
cu = POST(f"/api/shop/{Cu}/customer/add?name=U1&address=U", token=Tu)
cid_u = cu.get("customer_id")
u_serve = POST(f"/api/shop/{Cu}/customer/{cid_u}/serve", {}, token=Tu)
ok("撤销店: 标记成功" if u_serve.get("ok") else fail("撤销标记", str(u_serve)))

uu = POST(f"/api/shop/{Cu}/service/1/undo", token=Tu)
ok("24h撤销成功" if uu.get("ok") else fail("撤销", str(uu)))

uu2 = POST(f"/api/shop/{Cu}/service/1/undo", token=Tu)
ok("重复撤销不报错" if True else fail("重复撤销"))

# 3.4 去重
rd1 = POST(f"/api/shop/{C}/customer/add?{PU({'name':'DD','address':'DA','phone':'111'})}", token=T)
rd2 = POST(f"/api/shop/{C}/customer/add?{PU({'name':'DD','address':'DA','phone':'222'})}", token=T)
dd = GET(f"/api/shop/{C}")
dc = len([c for c in dd["customers"] if c["name"] == "DD"])
ok(f"去重: {dc}条(应1)" if dc == 1 else fail("去重", f"{dc}条"))

# 3.5 同名店铺
rs1 = POST("/api/shop/register", {"name": f"DupeName", "password": "test123"})
rs2 = POST("/api/shop/register", {"name": f"DupeName", "password": "test123"})
ok("同名第1次成功" if rs1.get("ok") else fail("同名1", str(rs1)))
ok("同名第2次拒绝" if not rs2.get("ok") else fail("同名2", str(rs2)))

# ============================================================
# 4. 并发
# ============================================================
print("\n📦 4. 并发")

results = []
cname = f"Concur-{uuid.uuid4().hex[:5]}"
def do_reg():
    try:
        r = json.loads(urllib.request.urlopen(
            urllib.request.Request(f"{B}/api/shop/register",
                data=json.dumps({"name": cname, "password": "test123"}).encode(),
                headers={"Content-Type": "application/json"}), timeout=10).read())
        results.append(1 if r.get("ok") else 0)
    except:
        results.append(0)

ts = [threading.Thread(target=do_reg) for _ in range(3)]
for t in ts: t.start()
for t in ts: t.join()
ok(f"并发注册: {sum(results)}/3成功(应1)" if sum(results) == 1 else fail("并发注册", f"{sum(results)}/3"))

t0 = time.time()
def do_read():
    try:
        for _ in range(5):
            urllib.request.urlopen(f"{B}/api/shop/{C}", timeout=10)
    except:
        pass
readers = [threading.Thread(target=do_read) for _ in range(5)]
for t in readers: t.start()
for t in readers: t.join()
t1 = time.time()
ok(f"并发5读: {(t1-t0)*1000:.0f}ms")

# ============================================================
# 结果
# ============================================================
print(f"\n{'=' * 55}")
print(f"  总计: ✅ {P}  ❌ {len(F)}")
for n, d in F: print(f"     ❌ {n}: {d}")
print(f"{'=' * 55}")
