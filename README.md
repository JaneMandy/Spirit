
# Spirit-Framework ZSD v1.0.6-rc3

### Version:1.0.6   By:ZSD 3he11

***
#### 更新信息：
v1.0.6-rc3

修复了FOFA不能查询问题，并且支持修改fofa域名等信息

对MS17-010 Payload进行优化。解决了攻击后重启问题。

声明：因为最近在改框架一些代码块，所以有些bug，大佬们发现及时指出谢谢。


v1.0.6-rc2
  
  修复了空命令时仍然执行上一条已执行命令

  修复了Windows编译Spiriter问题，包括shellcode编译问题（内置了NASM编译器）

  优化了session命令，连接会话时 输出系统基本系统。
  

v1.0.6 

  本版本支持Spiriter ShellCode加载。

  添加了CMAKE NASM构造编译环境模块。
  
  generate命令 添加了-S参数，主要针对Spiriter生成非shellcode的后门。

v1.0.5-rc2

  添加了exit命令 与退出问题。 
  
  添加了search命令 以描述信息与模块名为标准搜索
  
  修复了SpiritCore.Spirit里面的load_modules函数 异常处理问题。


***

以MSF为参考制作的渗透框架，目前功能并不是非常完善。还有很多bug，谅大佬们多多海涵。


目前版本：支持 后门/shellcode 生成，端口扫描，爬虫信息收集(rad)，Web漏洞扫描（基于xray），FOFA搜索。


漏洞利用目前只支持CVE-2020-0796 MS17-010

***
  生成EXE DLL格式后门需要安装cmake Mingw-W64
***
### 命令解释

back           返回命令

exploit       运行模块Exploit函数

generate    生成后门文件

help           帮助信息 （没有写全 只要banner）

info            模块信息

session      后门会话信息

set             修改参数

show         查看参数

use            使用模块

***
### 用法与配置

用法与MSF基本一样。

SpiritCore目录下Config为配置文件，里面存放FOFA等配置，但是xray已经做到自动定位，不用填写。

### 安装与运行
支持环境：Windows Linux

（建议使用Linux，因为Windows测试并不完善）
运行环境：建议使用Python3（可以使用Python2，但不建议）

安装依赖：impacket 、mingw-w64、 cmake、nasm

***
## 模块开发
~~~

from SpiritCore.Modules import *
from SpiritCore.System import *
class Module(Modules):
  Info = {
    "Name": "Test", #模块名称
    "Author": "ZSD", #作者ID
    "Description": "Test ",  #模块介绍
    "Options": (  #参数介绍
      ("Port", "23", True, 'Target IP Address',None),
      # 参数名  值   是否为空（并不启用）  说明   多选
      # 下面DEFINE设置条件 所以我们称为条件参数，该参数值也可以使用
      ("IfLogin", "True", True, 'Target IP Address',["True","False"]),
      # 多选参数   可选内容为True False
      ("Username", "root", True, 'Target IP Address',None),
      # 正常参数  
    ),
    "Payload":["windows/exec","dd"],
    # 按需 如果需要使用payload那么添加"Payload":["攻击载荷","介绍"],
    "SSH": (  #如果 Port为22 那么该子参数为可用  分别为 IP SSH
      ("IP", "127.0.0.1", True, "ip address"), 
      ("SSH", "Yes", True, "SSH INFO"),
    ),
    "FTP": ( #如果 Port为21 那么该子参数为可用  分别为IP
      ("IP", "127.0.0.2", True, "ip address"),
    ),

     }
  DEFINE = { # 条件参数 
    "SSH": {"Port": "22"}, 
    # 如果 Port值为22 那么SSH会显示并且可以使用 ，FTP不可用
    "FTP":{"Port":"21"}
     # 如果 Port值为21 那么FTP会显示并且可以使用  SSH不可用
  }

  def Exploit(self): # 利用函数
    print_success("Success")
    print_error("error")
    print_msg("msg")  
    # SpiritCore.System里面存放打印函数
    print(self.Parameate) # 参数内容
    Port=self.Parameate["Port"] # 将Port参数赋值给Port变量

~~~

如果ParameaterName内容为Values，那么ConParame就会可以使用。

~~~~
"ConParame": (
			("Parame", "Values", True, "Descripttion"),
		),
~~~~



### 安装:

##### 安装组件
~~~~
sudo apt install mingw-w64
sudo apt install cmake
~~~~


##### Python模块安装
~~~~
Python-pyreadline   (Support GetOutputFile Windows需要安装)
Python-impacket    （如果对MS17-010进行利用，那么需要安装）
Python-keystone 	（目前版本并不运用所以不用安装。）
~~~~
