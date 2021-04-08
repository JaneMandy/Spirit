#Spirit-Framework ZSD v1.0.1
***
Version:1.0.1    By:ZSD 3he11

Support Platform:Windows Linux MacOS

Python:2x 3x
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
~~~~









# Spirit
