#Spirit-Framework ZSD v1.0.2
***
Add MS17-010(github.com/worawit)

DoublePulsar (SC sub-assembly reference:http://bobao.360.cn/member/contribute?uid=2554610746)

PHP WebShell (reference:Godzila) (Disable Function Support:Linux) backdoor/php/backdoor

Ring3 ShellCode Add windows/bind_shell_tcp (test)

Shell Session Manager :exploit/multi/handler
***
 Because of functional requirements,don't do too much optimization first
 Many Functions of this update are not encapsulated.

CVE-2020-0796 Not Exploit 
***

Version:1.0.2    By:ZSD 3he11

Support Platform:Windows Linux MacOS



Python:2x ,3x
Recommend:Python 3x
***

##Update Inf
###1. Fix some bug
###2. Increase Modules load
###3. Support set show exploit command


##Modules kit
~~~
from SpiritCore.Modules import *
class Module(Modules):
	Info = {
		"Name": "Moduels",
		"Author": "Kit Name",
		"Description": "Test ",
		"Options": (
			("ParameaterName", "Values", True, 'Description'),
		),         
		"Payload":["Payload","Description"],  #Need to be add
		"ConParame": (
			("Parame", "Values", True, "Descripttion"),
		),

     }
	DEFINE = {
		"ConParame": {"ParameaterName": "Values"}
	}

	def Exploit(self):
	    print_success("hello word")
	    print_msg("hello")
            print_error("hello")		

~~~


The part requires DEFINE value as a condition
~~~~
"ConParame": (
			("Parame", "Values", True, "Descripttion"),
		),
~~~~



Install:
~~~~
Python-pyreadline   (Support GetOutputFile) 
Python-impacket
Python-keystone

~~~~

