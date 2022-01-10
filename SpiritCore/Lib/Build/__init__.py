from posixpath import expanduser
from typing import Type
from SpiritCore.Lib.Logs import *
from SpiritCore.System import *
from SpiritCore.Lib.Lib import *
import uuid,subprocess
import os
if Win32Platform:
    CppCmakeLists="""set(CMAKE_SYSTEM_NAME Windows)
project(hello_world)
%s"""
else:
    CppCmakeLists="""set(CMAKE_SYSTEM_NAME Windows)
set(TOOLCHAIN_PREFIX x86_64-w64-mingw32)
# cross compilers to use for C, C++ and Fortran
set(CMAKE_C_COMPILER ${TOOLCHAIN_PREFIX}-gcc)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_PREFIX}-g++)
set(CMAKE_Fortran_COMPILER ${TOOLCHAIN_PREFIX}-gfortran)
set(CMAKE_RC_COMPILER ${TOOLCHAIN_PREFIX}-windres)

# target environment on the build host system
set(CMAKE_FIND_ROOT_PATH /usr/${TOOLCHAIN_PREFIX})

# modify default behavior of FIND_XXX() commands
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
project(hello_world)
%s"""

def hex2bytes(s):
    rbytes = ''
    for i in range(0, len(s), 2):
        hx = s[i:i+2]
        rbytes += '\\x' + hx
    return rbytes

class CMAKE:
<<<<<<< HEAD
    STDOUT=False
=======
    
>>>>>>> 9dbce14cb0e4785b049f67e3bb46f02c4c305560
    Types="exe"
    Filename="shellcode"
    Sources="main.cpp"  #
    CmakeFilePath=""
    SourceCode=""  #BuildCode 
    GenerateFile="" # Build File
    def __init__(self):
        self.CppCmakeLists=CppCmakeLists
    def Generate(self):
        WriteLogs("Generate:CMakeLists.txt")
        try:
            if self.Types=="exe" or self.Types=="dll":
                CmakeLists=self.CppCmakeLists%self.AddGenerateType(self.Types,self.Filename,self.Sources)
            
            self.CmakeFilePath=MakeLogsPath(["CMakeFile-%s"%uuid.uuid4()])
            WriteLogs("Cmake Path:%s"%self.CmakeFilePath)
            WriteLogs("---------------------------CMakeLists.txt----------------------------------------\n"+CmakeLists)
            WriteLogs("---------------------------------------------------------------------------------")
            
            if(os.path.exists(self.CmakeFilePath)):
                pass
            else:
                os.mkdir(self.CmakeFilePath)
                WriteLogs("Create Dir:%s "%self.CmakeFilePath)
            CmakeListsTxt = MakePath(["CMakeLists.txt"],self.CmakeFilePath)
            WriteLogs("Build Type:%s -> %s"%(self.Types,self.Filename))
            Sources = MakePath([self.Sources],self.CmakeFilePath)
            if Win32Platform:
                self.GenerateFile=MakePath(["Release",self.Filename+"."+self.Types],self.CmakeFilePath)
            else:
                if self.Types=="dll":
                    self.GenerateFile=MakePath(["lib"+self.Filename+"."+self.Types],self.CmakeFilePath)
                elif self.Types=="exe":
                    self.GenerateFile=MakePath([self.Filename+"."+self.Types],self.CmakeFilePath)
            WriteLogs("WriteFile:%s"%CmakeListsTxt)
            open(CmakeListsTxt,"wb+").write(bytes(CmakeLists,encoding="utf-8"))
            WriteLogs("Sources:%s"%Sources)
            WriteLogs("---------------------------Source Code----------------------------------------\n"+self.SourceCode)
            WriteLogs("------------------------------------------------------------------------------")
            open(Sources,"wb+").write(bytes(self.SourceCode,encoding="utf-8"))
            Command = ["cmake"]
            if Win32Platform:
                Command.append("-A")
                Command.append("x64")
            Command.append(".")
            WriteLogs("Run CMake:%s"%" ".join(Command))
<<<<<<< HEAD
            if self.STDOUT:
                object = subprocess.Popen(Command,stdout = subprocess.PIPE,stderr = subprocess.STDOUT,cwd=self.CmakeFilePath)
            else:
                object = subprocess.Popen(Command,cwd=self.CmakeFilePath)
            object.wait()
=======
            object = subprocess.Popen(Command,cwd=self.CmakeFilePath)
            object.wait()
            WriteLogs("Run Command"+object.__str__())
>>>>>>> 9dbce14cb0e4785b049f67e3bb46f02c4c305560
            if True:  #Windows Linux support 
                Command=[]
                Command.append("cmake")
                Command.append("--build")
                Command.append(".")
                Command.append("--config")
                Command.append("Release")
            WriteLogs("Build Command CMake:%s"%" ".join(Command))
<<<<<<< HEAD
            if self.STDOUT:
                print_success("Build DLL........")
                object2 = subprocess.Popen(Command,stdout = subprocess.PIPE,stderr = subprocess.STDOUT,cwd=self.CmakeFilePath)
            else:
                object2 = subprocess.Popen(Command,cwd=self.CmakeFilePath)
            object2.wait()
            #print(self.GenerateFile)
=======
            object2 = subprocess.Popen(Command,cwd=self.CmakeFilePath)
            object2.wait()
>>>>>>> 9dbce14cb0e4785b049f67e3bb46f02c4c305560
            if os.path.exists(self.GenerateFile):
                WriteLogs("=======================================================================================")
                WriteLogs("=======================================================================================")
                WriteLogs("=======================================================================================")
                WriteLogs("=======================================================================================")
                WriteLogs("Build Success:%s"%self.GenerateFile)
                return self.GenerateFile
            else:
                WriteLogs("Build Faild")
                return ""
        except Exception as error:
            print(error)
            return ""
        
    def AddGenerateType(self,Types,Filename,Sources):
        if Types=="exe" or Types=="elf":
            ADD="add_executable(%s %s)"%(Filename,Sources)
        elif Types=="os" or Types=="dll": 
            ADD="add_library(%s SHARED %s)"%(Filename,Sources)
        return ADD



<<<<<<< HEAD
class NASM:
    Types="exe"
    NasmFilePath=""
    Filename="shellcode"
    SourceCode=""
    Sources="main.asm"
    GenerateFile="shellcode.bin"
    def Generate(self):
        WriteLogs("Generate:NASM Build")
        try:
            self.NasmFilePath=MakeLogsPath(["NASM-%s"%uuid.uuid4()])
            if(os.path.exists(self.NasmFilePath)):
                pass
            else:
                os.mkdir(self.NasmFilePath)
                WriteLogs("Create Dir:%s "%self.NasmFilePath)
            WriteLogs("Build  %s"%(self.Filename))
            Sources = MakePath([self.Sources],self.NasmFilePath)
            if True:
                self.GenerateFile=MakePath([self.Filename+".bin"],self.NasmFilePath)
            WriteLogs("Sources:%s"%Sources)
            WriteLogs("---------------------------Source Code----------------------------------------\n"+self.SourceCode)
            WriteLogs("------------------------------------------------------------------------------")
            open(Sources,"wb+").write(bytes(self.SourceCode,encoding="utf-8")) #Windows Linux support 
            Command=[]
            Command.append("nasm")
            Command.append(Sources)
            Command.append("-o")
            Command.append(self.GenerateFile)
            WriteLogs("Build Command CMake:%s"%" ".join(Command))
            object2 = subprocess.Popen(Command,cwd=self.NasmFilePath)
            object2.wait()
            #print(self.GenerateFile)
            if os.path.exists(self.GenerateFile):
                WriteLogs("=======================================================================================")
                WriteLogs("=======================================================================================")
                WriteLogs("=======================================================================================")
                WriteLogs("=======================================================================================")
                WriteLogs("Build Success:%s"%self.GenerateFile)
                return self.GenerateFile
            else:
                WriteLogs("Build Faild")
                return ""
        except Exception as error:
            print(error)
            return ""
=======

>>>>>>> 9dbce14cb0e4785b049f67e3bb46f02c4c305560









