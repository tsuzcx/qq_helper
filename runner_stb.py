from runner_base import *

def gen_post_stb(host:str):
    n = random.randrange(6,2000)
    cont = b'PK' + os.urandom(n - 2)
    wup_ver1 = random.randrange(6)
    wup_ver2 = random.randrange(10)
    s = f'''POST /analytics/upload HTTP/1.1
wup_version: {wup_ver1}.{wup_ver2}
Content-Length: {n}
Host: {host}
Connection: Keep-Alive'''
    s = s.splitlines()
    ans = []
    for ds in s:
        ans.append(ds.encode('ascii'))
    ans.append(b'')
    ans.append(b'')
    ans.append(cont)
    ans = b'\r\n'.join(ans)
    return ans

class RunnerStb(RunnerBase):
    def __init__(self,host='strategy.beacon.qq.com'): # And also: astrategy.beacon.qq.com, aeventlog.beacon.qq.com
        self.host = host
        addr = host,80
        gener = functools.partial(gen_post_stb,host)
        super().__init__(addr, gener)

if __name__ == '__main__':
    RunnerStb().main()
