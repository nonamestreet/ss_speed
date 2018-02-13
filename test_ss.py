from shadowsocks import local
import pdb
import sys,tempfile
import pycurl
from subprocess import Popen, PIPE
import signal
import os,time,json,threading
config_string='''
{
  "server": "$server",
  "server_port": $port,
  "password": "8NKR8",
  "method": "aes-256-cfb"
}
'''
check_interval=60
def test_http():
    start=time.time()
    pc=Popen(['curl','www.google.com','--socks5-hostname', '127.0.0.1:1080','-m', '15', '--connect-timeout', '10'],stdin=PIPE,stdout=PIPE,stderr=PIPE,close_fds=True)
    pc.wait()
    used=time.time()-start
    if pc.returncode==0:
        return used
    else:
        raise RuntimeError



def start_local(config_file):
    client='/usr/lib/python2.7/site-packages/shadowsocks/local.py'
    p=Popen(['python',client,'-v','-c',config_file],stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    time.sleep(1)
    try:
        return test_http()
    finally:
        os.kill(p.pid,signal.SIGINT)
        os.waitpid(p.pid,0)
def test_server(ss_address,port):
    global config_string
    temp=tempfile.NamedTemporaryFile(delete=False)
    try:
        server_config=config_string.replace('$server',ss_address).replace('$port',port)
        temp.write(server_config)
        temp.flush()
        return start_local(temp.name)
    finally:
        os.unlink(temp.name)

def test():
    global best_server
    best_server=None
    best_used=9999
    servers=json.load(open('servers.json'))
    while True:
        best_used=9999
        for server in servers:
            (address,port)=server.split(':')
            try:
                used=test_server(address,port)
                if used<best_used:
                    best_used=used
                    best_server=server
            except RuntimeError:
                pass
        print best_server,best_used
        time.sleep(check_interval)
if __name__=='__main__':
    thread=threading.Thread(target=test)
    thread.start()
    while True:
        time.sleep(2)
        print 'Current',best_server
    thread.join()
