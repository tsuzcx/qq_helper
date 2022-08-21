import os,socket,random,threading,time,traceback,io,functools,faker

socket.setdefaulttimeout(60)

def uuid_str():
    ans = []
    for n in (4,2,2,2,6):
        b = os.urandom(n)
        h = b.hex()
        ans.append(h)
    return '-'.join(ans)

class RunnerBase:
    def __init__(self,addr,gener):
        self.addr = addr
        self.gener = gener
        self.b_send = gener()
        self.b_recv = b''
        self.exc = ''
        self.n = 0
        self.mutex = threading.Lock()
    
    def post(self):
        s = socket.socket()
        s.connect(self.addr)
        s.send(self.b_send)
        self.b_recv = s.recv(1000)
        s.close()
        with self.mutex:
            self.n += 1

    def one_thread(self):
        while True:
            try:
                self.post()
            except:
                s = io.StringIO()
                traceback.print_exc(file=s)
                s = s.getvalue()
                self.exc = s

    def main(self,tn=100,max_time=30):
        t0 = time.time()
        for _ in range(tn):
            t = threading.Thread(target=self.one_thread,daemon=True)
            t.start()
        while True:
            s = self.b_recv.decode('utf-8','ignore').rstrip()
            exc = self.exc
            self.exc = ''
            dt = time.time() - t0
            dn = self.n
            speed = dn / dt
            if s:
                print('# last received')
                print(s)
            if exc:
                print('# last exception')
                print(exc)
            print(f'{dn} ({speed} req/s)')
            if max_time and dt > max_time:
                break
            for _ in range(5):
                self.b_send = self.gener()
                time.sleep(1)
        exit()
