from SpiritCore.Modules import *
from SpiritCore.Lib.IPy import IP
import socket,threading,socks

class Module(Modules):
    Info = {
        "Name": "Port Scanner ",
        "Author": "ZSD",
        "Description": "Port Scanner Support Proxy Scan ",
        "Options": (
            ("Target", "192.168.0.0/24", True, 'Target IP Address', None),
            ("Proxy", "NO", True, 'Proxy Options', ["NO","HTTP","HTTPS","SOCK5","SOCK4","SpiritProxy"]),
            ("Port", "80,443", True, 'Scan Port ', None),
        ),
        "Proxy":(
            ("ProxyAddress","127.0.0.1",True,"Proxy Server Address"),
            ("ProxyPort"        ,"8080"     ,True,"Proxy Server Port"),
            ("Username","",True,"Proxy Anth Username"),
            ("Password","",True,"Proxy Anth Password"),
        ),
    }
    DEFINE={
               "Proxy": {"Proxy": "NO"}
     }

    def get_ip_status(self,ip, port):
        if self.Parameate["Proxy"]=="NO":
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.settimeout(3)
        elif self.Parameate["Proxy"=="HTTP"]:
            server=socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, self.Parameate["ProxyAddress"], int(self.Parameate["ProxyPort"]))
        try:
            code =server.connect_ex((str(ip), port))
            if code==0:
                print_success('{0} port {1} is open'.format(ip, port))
            else:
                pass
                #print(1)
        except Exception as err:
            pass
        finally:
            server.close()
    def scan(self,ip,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        try:
            if sock.connect_ex((ip,port))==0:
                print_success("%s  --- open ----%d"%(ip,port))
            else:
                pass
        except:
            pass
    def Exploit(self):
        ScanHost=[]
        Port=[]
        Count=0
        threads=[]
        print_msg("Scanner Exploit %s" % self.Parameate["Target"])
        print_msg("Start Scanner")
        write("="*40)
        write("")
        Host = self.Parameate["Target"]
        if "/" in Host:
            IpAddress = IP(Host)
            for ip in IpAddress:
                ScanHost.append(str(ip.net()))
        else:
            ScanHost.append(str(self.Parameate["Target"]))
        if "-" in self.Parameate["Port"]:
            StartPort=int(self.Parameate["Port"].split("-")[0])
            EndPort = int(self.Parameate["Port"].split("-")[1])
            for P in range(StartPort,EndPort):
                Port.append(P)
        elif "," in self.Parameate["Port"]:
            PortList = self.Parameate["Port"].split(",")
            for P in PortList:
                Port.append(int(P))
        else:
                Port.append(int(self.Parameate["Port"]))
        for Ip in ScanHost:
            for port in Port:
                Count+=1
                Count += 1
                t = threading.Thread(target=self.scan, args=(str(Ip), int(port)))
                threads.append(t)
        for a in threads:
            a.start()
        for a in threads:
            a.join()
        write("")
        write("="*40)




