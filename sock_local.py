import os,socket,random,faker,threading,time,traceback,io

socket.setdefaulttimeout(60)

host_rqd = 'android.rqd.qq.com'

def uuid_str():
    ans = []
    for n in (4,2,2,2,6):
        b = os.urandom(n)
        h = b.hex()
        ans.append(h)
    return '-'.join(ans)

def gen_post_rqd():
    n = random.randrange(2000)
    cont = os.urandom(n)
    aid = uuid_str()
    sid = uuid_str()
    wup_ver1 = random.randrange(6)
    wup_ver2 = random.randrange(10)
    app_ver1 = random.randrange(10)
    app_ver2 = random.randrange(2)
    app_ver3 = random.randrange(10)
    app_ver4 = random.randrange(10000)
    app = random.choice(['mobileqq','mobileqqi','minihd.qq','mm','qqlite','tim'])
    sdk_ver1 = random.randrange(4)
    sdk_ver2 = random.randrange(10)
    sdk_ver3 = random.randrange(4)
    cmd = random.randrange(1000)
    net = random.choice(['WIFI','4G','5G'])
    pid = random.randrange(3)
    f = faker.Faker()
    ua = f.user_agent()
    s = f'''POST /analytics/async?aid={aid} HTTP/1.1
wup_version: {wup_ver1}.{wup_ver2}
secureSessionId: {sid}_SH
strategylastUpdateTime: 0
appVer: {app_ver1}.{app_ver2}.{app_ver3}.{app_ver4}
bundleId: com.tencent.{app}
sdkVer: {sdk_ver1}.{sdk_ver2}.{sdk_ver3}
prodId: com.tencent.{app}
cmd: {cmd}
platformId: {pid}
A37: {net}
A38: {net}
Content-Type: application/x-www-form-urlencoded
User-Agent: {ua}
Host: {host_rqd}
Connection: Keep-Alive
Accept-Encoding: gzip
Content-Length: {n}'''
    s = s.splitlines()
    ans = []
    for ds in s:
        ans.append(ds.encode('ascii'))
    ans.append(b'')
    ans.append(b'')
    ans.append(cont)
    ans = b'\r\n'.join(ans)
    return ans

_send_rqd = b''
_recv_rqd = b''
_exc_rqd = ''
_n_rqd = 0

def post_rqd():
    global _recv_rqd,_n_rqd
    s = socket.socket()
    s.connect((host_rqd,80))
    s.send(_send_rqd)
    _recv_rqd = s.recv(1000)
    s.close()
    with threading.Lock():
        _n_rqd += 1

def one_thread():
    global _exc_rqd
    while True:
        try:
            post_rqd()
        except:
            s = io.StringIO()
            traceback.print_exc(file=s)
            s = s.getvalue()
            _exc_rqd = s

def main_local(tn=100,max_time=30):
    global _send_rqd,_exc_rqd
    ts = []
    _send_rqd = gen_post_rqd()
    t0 = time.time()
    for _ in range(tn):
        t = threading.Thread(target=one_thread,daemon=True)
        t.start()
        ts.append(t)
    while True:
        s = _recv_rqd.decode('utf-8','ignore').rstrip()
        exc = _exc_rqd
        _exc_rqd = ''
        dt = time.time() - t0
        dn = _n_rqd
        speed = dn / dt
        if s:
            print('# last received')
            print(s)
        if exc:
            print('# last exception')
            print(exc)
        print(f'{dn} ({speed} req/s)')
        if dt > max_time:
            break
        for _ in range(5):
            _send_rqd = gen_post_rqd()
            time.sleep(1)
    exit()

if __name__ == '__main__':
    main_local()
