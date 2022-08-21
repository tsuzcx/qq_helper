from runner_base import *

def gen_post_rqd(host_rqd:str):
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

class RunnerRqd(RunnerBase):
    def __init__(self,host='android.rqd.qq.com'):
        self.host = host
        addr = host,80
        gener = functools.partial(gen_post_rqd,host)
        super().__init__(addr, gener)

if __name__ == '__main__':
    RunnerRqd().main()
