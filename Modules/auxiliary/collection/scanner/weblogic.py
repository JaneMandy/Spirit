from SpiritCore.System import *
from SpiritCore.Modules import *
from SpiritCore.Lib.Detection.Middleware.Weblogic import *




class Module(Modules):
    Info = {
        "Name": "Weblogic Vuln Scanner ",
        "Author": "ZSD",
        "Description": "Weblogic Scanner Support Proxy Scan ",
        "Options": (
            ("address", "vulfocus.fofa.so", True, 'Target Weblogic Address', None),
            ("port", "54550", True, 'Target Weblogic Port', None),
            ("VulnCode", "CVE20173506", True, 'Target Weblogic Port', ["CVE202014882","CVE20173506"]),
        ),
    }
    def Exploit(self):
        print_success("Weblogic Detection")
        CVE202014882Object=CVE202014882()
        CVE20173506Object= CVE20173506()
        if self.Parameate["VulnCode"]=="ALL":
            pass
        elif self.Parameate["VulnCode"]=="CVE202014882":
            CVE202014882Object.make(self.Parameate["address"],self.Parameate['port'])
            if CVE202014882Object.verify():
                print_success("Success")
        elif self.Parameate["VulnCode"]=="CVE20173506":
            CVE20173506Object.make(self.Parameate["address"],self.Parameate['port'])
            if CVE20173506Object.verify():
                print_success("Success")











