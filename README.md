#Spirit-Framework ZSD v1.0.5
###Version:1.0.5    By:ZSD 3he11
***

以MSF为参考制作的渗透框架，目前功能并不是非常完善。还有很多bug，谅大佬们多多海涵。

目前版本：支持 后门/shellcode 生成，端口扫描，爬虫信息收集(rad)，Web漏洞扫描（基于xray），FOFA搜索。

漏洞利用目前只支持CVE-2020-0796 MS17-010

***
  生成EXE DLL格式后门需要安装cmake Mingw-W64
***


##模块开发
~~~
from SpiritCore.Modules import *
class Module(Modules):
	Info = {
		"Name": "Moduels Name",
		"Author": "Author Name",
		"Description": "Test ",
		"Options": (
			("ParameaterName", "Values", True, 'Description',None),# 普通参数，但是加入了下面DEFINE条件区，所以变成条件参数
			("Prtolo", "SMB", True, 'Description',["SMB","RPC"]), #多选参数。通过使用TAB按键填充
		),         
		"Payload":["Payload","Description"],  #Need to be add
		"ConParame": (#需要条件的参数组，可以设置成代理等等
			("Parame", "Values", True, "Descripttion"),
		),

     }
	DEFINE = { #条件内容
		"ConParame": {"ParameaterName": "Values"}
	}

	def Exploit(self):
	    print_success("hello word")
	    print_msg("hello")
            print_error("hello")		

~~~

如果ParameaterName内容为Values，那么ConParame就会可以使用。

~~~~
"ConParame": (
			("Parame", "Values", True, "Descripttion"),
		),
~~~~



###安装:

#####安装组件
~~~~
sudo apt install mingw-w64
sudo apt install cmake
~~~~


#####Python模块安装
~~~~
Python-pyreadline   (Support GetOutputFile Windows需要安装)
Python-impacket    （如果对MS17-010进行利用，那么需要安装）
Python-keystone 	（目前版本并不运用所以不用安装。）
~~~~
