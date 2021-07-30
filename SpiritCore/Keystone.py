from binascii import b2a_hex
from keystone import *
from binascii import hexlify, unhexlify

X86_16  = 'i186'
X86_32  = 'i386'
X86_64  = 'i686'
ARM32   = 'arm32'
ARM64   = 'arm64'
ARM_TB  = 'arm_tb'
MIPS32  = 'mips32'
MIPS64  = 'mips64'
HEXAGON = 'hexagon'
PPC32   = 'ppc32'
PPC64   = 'ppc64'
SPARC32 = 'sparc32'
SPARC64 = 'sparc64'
SYSTEMZ = 'systemz'
#x86 x64



def hex2bytes(s):
    rbytes = ''
    for i in range(0, len(s), 2):
        hx = s[i:i+2]
        rbytes += '\\x' + hx
    return rbytes

class Keystone:
    Arch="x86"
    def __init__(self):
        pass
    def archs(self):
        return {
            ARM32:   (KS_ARCH_ARM,     KS_MODE_ARM),
            ARM64:   (KS_ARCH_ARM64,   KS_MODE_LITTLE_ENDIAN),
            ARM_TB:  (KS_ARCH_ARM,     KS_MODE_THUMB),
            HEXAGON: (KS_ARCH_HEXAGON, KS_MODE_BIG_ENDIAN),
            MIPS32:  (KS_ARCH_MIPS,    KS_MODE_MIPS32),
            MIPS64:  (KS_ARCH_MIPS,    KS_MODE_MIPS64),
            PPC32:   (KS_ARCH_PPC,     KS_MODE_PPC32),
            PPC64:   (KS_ARCH_PPC,     KS_MODE_PPC64),
            SPARC32: (KS_ARCH_SPARC,   KS_MODE_SPARC32),
            SPARC64: (KS_ARCH_SPARC,   KS_MODE_SPARC64),
            SYSTEMZ: (KS_ARCH_SYSTEMZ, KS_MODE_BIG_ENDIAN),
            X86_16:  (KS_ARCH_X86,     KS_MODE_16),
            X86_32:  (KS_ARCH_X86,     KS_MODE_32),
            "x86":  (KS_ARCH_X86,     KS_MODE_32),
            "x64":  (KS_ARCH_X86,     KS_MODE_64),
            X86_64:  (KS_ARCH_X86,     KS_MODE_64),
            }
    def AsmtoShellCode(self,AsmCode):
            ks=Ks(*self.archs()[self.Arch])
            IntShellcode, num_instructions = ks.asm(AsmCode)
            raw_hex   = hexlify(bytearray(IntShellcode)).decode('utf-8')
            raw_bytes = hex2bytes(raw_hex)
            return raw_hex
    def pushString_x86(self,String,Arch,Register):
        AamList=[]
        AsmToCode=""
        if Arch=="i386":
            String = StringPressDao(String)
            Stringbytes = b2a_hex(String)
            while True:
                SticData = Stringbytes[-8:]
                if len(SticData)==8:
                        TempAsmCode="push 0x%s\n"%SticData    
                        AamList.append(TempAsmCode)
                elif len(SticData)<8:
                    if len(SticData)==6:
                        TempAsmCode="sub dword ptr[esp+0x3],0x61\n"
                        AamList.append(TempAsmCode)
                        TempAsmCode="push 0x61%s\n"%Stringbytes
                        AamList.append(TempAsmCode)
                    elif len(SticData)==4:
                        TempAsmCode="push %s\n"%(Register)
                        AamList.append(TempAsmCode)
                        if Register=="ecx":
                            RegisterX="cx"
                        elif Register=="ebx":
                            RegisterX="bx"
                        elif Register=="edx":
                            RegisterX="dx"
                        TempAsmCode="mov %s, 0x%s\n"%(RegisterX,Stringbytes)
                        AamList.append(TempAsmCode)
                        TempAsmCode="xor %s,%s\n"%(Register,Register)
                        AamList.append(TempAsmCode)
                    elif len(SticData)==2:
                        TempAsmCode="push %s\n"%(Register)
                        AamList.append(TempAsmCode)
                        TempAsmCode="add %s,0x%s\n"%(Register,Stringbytes)
                        AamList.append(TempAsmCode)
                        TempAsmCode="xor %s,%s\n"%(Register,Register)
                        AamList.append(TempAsmCode)
                    elif len(SticData)==0:
                        pass
                    break            
                Stringbytes=Stringbytes[:-8]
            for TempCodeAsm in AamList:
                AsmToCode=TempCodeAsm+AsmToCode
        return AsmToCode,len(String)