from SpiritCore.FCmd import *
from SpiritCore.System import *
from SpiritCore.Payload import *
from SpiritCore.Config import *
import fnmatch,os,imp

#34




def to_unicode(obj):
	return obj


class Framework(Cmd):
    completekey = "tab"
    prompt="%s >"
    promptName="Spirit"
    DisableBack=False


    DEFINE={}
    condition=[]
    Values = {}
    description = {}
    required = {}
    Choins={}


    # Modules Object
    modules = {}
    ModulesCount = 0
    ModulesList = []
    # Payload Object
    Payload = {}
    PayloadCount = 0
    PayloadList = []

    UseModules=False
    UsePayload=False
    ModulesParameter={}
    UseModulesObject=None
    UsePayloadObject=None
    Payloadparameter={}

    PayloadParameate={}



    extra_modules_dirs="exploit/windows/pss"
    
    def __init__(self):
        Cmd.__init__(self)
        self.mswindows = (sys.platform == "win32")
        self.prompt = "%s >"%self.promptName
    
    def Init(self):
        print_msg("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print_msg("=                                                           =")
        print_msg("=                     "+TextColor("ZSD   Spirit   Mike",COLO_YELLOW)+"                   =")
        print_msg("=               "+   TextColor("MichaelHenryRumsfeld@Gmail.com",COLO_RED)+"              =")
        print_msg("=                                                           =")
        print_msg("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        self.CheckLib()
        self.load_modules("%s/Modules/"%os.getcwd())
        self.load_Payload("%s/SpiritCore/Payloads/"%os.getcwd())
        try:
            self.cmdloop()
        except KeyboardInterrupt as Error:
            print_success("Bye Bye")
            exit()
    
    def CheckLib(self):
        print_msg("Check Import Python Modules ")
        try:
            try:
                try:
                    import readline
                except ImportError:
                    import pyreadline as readline
            except:
                print_error("Install readline")
                exit()
            #import impacket
            #import keystone
            #import capstone
            #import ctypes
        except Exception as error:
            print_error("Import Error:%s"%error)
            exit()
        else:
            print_success("Check PyModules Successfuly")


    ###########################################################
    #Modules Load
    def load_Payload(self, rootPath=''):
        """
        Load Empire modules from a specified path, default to
        installPath + "/lib/modules/*"
        """

        #print(rootPath)
        pattern = '*.py'
        print_msg("Loading Payload from: %s" % (rootPath))
        try:
            for root, dirs, files in os.walk(rootPath):
                for filename in fnmatch.filter(files, pattern):
                    filePath = os.path.join(root, filename)

                    # don't load up any of the templates
                    if fnmatch.fnmatch(filename, '*template.py'):
                        continue

                    # extract just the module name from the full path
                    moduleName = filePath.split(rootPath)[-1][0:-3]
                    #print(rootPath)

                    try:
                    # instantiate the module and save it to the internal cache
                        self.Payload[moduleName] = imp.load_source(moduleName, filePath).Payloads()
                        self.Payload[moduleName].Inti(self)
                        self.Payload[moduleName].Name=moduleName
                        self.ParameateTmpInfo = self.Payload[moduleName].Info.get("Options")
                        if self.ParameateTmpInfo:
                            for option in self.ParameateTmpInfo:
                                self.Payload[moduleName].r_option(*option)
                            self.Values={}
                    #self.modules[moduleName].Execute()
                    except Exception as Error:
                        ErrorInfo="Load %s ---- %s"%(moduleName,Error.__str__())
                        print_error(ErrorInfo)
                    else:
                        self.PayloadCount+=1
                        self.PayloadList.append(moduleName)
        except Exception as error:
            ErrorInfo = "Error:%s" % (error.__str__())
            print_error(ErrorInfo)
            exit()
        else:
            pass

    def load_modules(self, rootPath=''):
        """
        Load Empire modules from a specified path, default to
        installPath + "/lib/modules/*"
        """

        #print(rootPath)
        pattern = '*.py'
        print_msg("Loading modules from: %s" % (rootPath))
        try:
            for root, dirs, files in os.walk(rootPath):
                for filename in fnmatch.filter(files, pattern):
                    filePath = os.path.join(root, filename)

                    # don't load up any of the templates
                    if fnmatch.fnmatch(filename, '*template.py'):
                        continue

                    # extract just the module name from the full path
                    moduleName = filePath.split(rootPath)[-1][0:-3]
                    #print(rootPath)

                    try:
                    # instantiate the module and save it to the internal cache
                        self.modules[moduleName] = imp.load_source(moduleName, filePath).Module()
                        self.modules[moduleName].Init(self)
                        self.modules[moduleName].LoadStatus=True
                        self.modules[moduleName].Name=moduleName
                        self.ParameateTmpInfo = self.modules[moduleName].Info.get("Options")
                        if self.ParameateTmpInfo:
                            for option in self.ParameateTmpInfo:
                                self.r_option(*option)
                    #self.modules[moduleName].Execute()
                    except Exception as Error:
                        ErrorInfo="Load %s ---- %s"%(moduleName,Error.__str__())
                        print_error(ErrorInfo)
                    else:
                        self.ModulesCount+=1
                        self.ModulesList.append(moduleName)
        except Exception as error:
            ErrorInfo = "Error:%s" % (error.__str__())
            print_error(ErrorInfo)
            exit()
        else:
            print_success("Moules Loaded Count:%d"%self.ModulesCount)
    def r_option(self, name, value=None, required=False, description='',Choins=None):
        self.Values[name] = self.SetLoadvalue(value)
        self.required[name] = required
        self.description[name] = description
        if Choins!=None:
            self.Choins[name]=Choins
        else:
            self.Choins[name]=None


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
    
    ###############################################################################
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
                readline.parse_and_bind(self.completekey+": complete")
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro)+"\n")
            stop = None
            while not stop:
                line=""
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            if sys.version_info.major==2:
                                line = raw_input(self.prompt)
                                #print(line)
                            else:
                                line = str(input(self.prompt))   #stdout stdin Not Support TAB Key
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
    def default(self, line):
        """Called on an input line when the command prefix is not recognized.

        If this method is not overridden, it prints an error message and
        returns.

        """
        print_error('Unknown Command: %s\n'%line,time=0)




    def do_info(self,line):
        if self.UseModules==True:
            info='''Show INF
    Name:%s
    Author:%s
    Description:%s
            '''
            print_msg(info%(self.UseModulesObject.Info["Name"],self.UseModulesObject.Info["Author"],self.UseModulesObject.Info["Description"]))
            self.show_options()
    def do_back(self,line):
        print_success("Back Command")
        if self.DisableBack!=True:
            self.UseModules=False
            self.UsePayload=False
            self.UseModulesObject=None
            self.UsePayloadObject=None
            self.prompt = "%s > " % self.promptName

 ###########################
    # Command show
    #         use
    #         exit
    def do_use(self,line):
        print_msg("USE MODULES")
        try:
            ModulesObj=self.modules[line]
            if ModulesObj.LoadStatus!=True:
                print_error("Modules Status False")
        except:
            print_error("USE Failed")
        else:
            self.Values={}
            self.required={}
            self.description={}
            self.Choins={}
            self.condition=[]
            self.DEFINE={}
            self.UseModules=False
            self.UsePayload=False
            self.PayloadParameate={}
            self.UseModulesObject=None
            self.UsePayloadObject=None
            category = line.split('/')[0]
            try:
                self.prompt="%s %s(%s) >"%(self.promptName,category,TextColor(line.split('/')[-1],COLO_RED))
            except:
                self.prompt="%s (%s) >"%(self.promptName,line)
            self.UseModules=True
            self.UseModulesObject=ModulesObj
            #self.ModulesParameter =
            Tmp= self.UseModulesObject.Info.get("Options")
            if Tmp:
                for options in Tmp:
                    try:
                        self.r_option(*options)
                    except Exception as error:
                        print(error)

                try:
                    # print("d")
                    if self.UseModulesObject.Info["Payload"]:
                        self.UsePayload = True
                        self.UsePayloadObject = self.Payload[self.UseModulesObject.Info["Payload"][0]]
                        self.PayloadParameate = self.UsePayloadObject.GetParameate(self.UsePayloadObject.Name)
                        # print(self.UseModulesObject.Info["Payload"][0])

                except Exception as error:
                    #print(error)
                    self.UsePayload = False


                try:
                    if self.UseModulesObject.DEFINE:
                        self.condition=self.UseModulesObject.DEFINE.keys()
                        for key in self.condition:
                            try:
                                Tiao=self.UseModulesObject.DEFINE[key]
                            except:
                                pass
                            Tiao = self.UseModulesObject.DEFINE[key]
                            TiaoKey=list(Tiao.keys())[0]

                            if self.Values[TiaoKey]!=Tiao[TiaoKey]:
                                Obj = Parame()
                                Obj.Inti(self)
                                Obj.Name=key
                                #print(1)
                                #print( self.UseModulesObject.DEFINE.get(key))
                                for option in self.UseModulesObject.Info.get(key):
                                    try:
                                        Obj.r_option(*option)
                                    except Exception as error:
                                        print(error)
                                        helper='''
                                            Check Options Pameatre Formcat 
                                             "Op1":(
           < ("P1","Values",True,"Dst"),> !!!!!!!!!!!!!!!!!!!!!!!
            )

    
    DEFINE={
               "Op1": {"Parame1": "Values"}
     }
                                        '''
                                        print_error(helper)
                                self.DEFINE.update({TiaoKey:Obj})
                            else:
                                try:
                                    self.DEFINE.pop(TiaoKey)
                                except:
                                    pass



                except Exception as error:
                    print(error)


    def do_set(self,line):
        options = line.split()
        if len(options) < 2:
            return
        name = options[0]
        if name in self.Values:
            value = ' '.join(options[1:])
            self.Values[name] = value
            print_success('%s => %s'%(name,value))

        if self.UsePayload==True:
            if name in self.UsePayloadObject.Values:
                value = ' '.join(options[1:])
                self.UsePayloadObject.Values[name] = value
                print_success('%s => %s' % (name, value))
        try:
            if self.UseModulesObject.DEFINE:
                self.condition = self.UseModulesObject.DEFINE.keys()
                for key in self.condition:
                    Tiao = self.UseModulesObject.DEFINE[key]
                    TiaoKey = list(Tiao.keys())[0]
                    OpName=TiaoKey
                    if self.Values[TiaoKey] != Tiao[TiaoKey]:
                        if name in self.DEFINE[OpName].Values:
                            value = ' '.join(options[1:])
                            self.DEFINE[OpName].Values[name] = value
                            print_success('%s => %s' % (name, value))


        except Exception as error:
            #print(error)
            pass

        try:
            if self.UseModulesObject.DEFINE:
                self.condition = self.UseModulesObject.DEFINE.keys()
                for key in self.condition:
                    try:
                        Tiao = self.UseModulesObject.DEFINE[key]
                    except:
                        pass
                    Tiao = self.UseModulesObject.DEFINE[key]
                    TiaoKey = list(Tiao.keys())[0]

                    if self.Values[TiaoKey] != Tiao[TiaoKey]:
                        try:
                            if self.DEFINE[key].Name!=key:
                                print(1)
                        except:
                            Obj = Parame()
                            Obj.Inti(self)
                            Obj.Name = key
                            # print(1)
                            # print( self.UseModulesObject.DEFINE.get(key))
                            for option in self.UseModulesObject.Info.get(key):
                                try:
                                    Obj.r_option(*option)
                                except Exception as error:
                                    print(error)
                                    helper = '''
                                                                                                                    Check Options Pameatre Formcat 
                                                                                                                     "Op1":(
                                                                                   < ("P1","Values",True,"Dst"),> !!!!!!!!!!!!!!!!!!!!!!!
                                                                                    )


                                                                            DEFINE={
                                                                                       "Op1": {"Parame1": "Values"}
                                                                             }
                                                                                                                '''
                                    print_error(helper)
                            self.DEFINE.update({TiaoKey: Obj})
                            return
                        else:
                            pass
                    else:
                        try:
                            self.DEFINE.pop(TiaoKey)
                        except:
                            pass



        except Exception as error:
            #print(error)
            pass



    def complete_use(self, text, line, begidx, endidx):

        module_names = self.ModulesList
        language = None

        if language:
            module_names = [(module_name[len(language) + 1:]) for module_name in module_names if
                            module_name.startswith(language)]

        mline = line.partition(' ')[2]

        offs = len(mline) - len(text)

        module_names = [s[offs:] for s in module_names if s.startswith(mline)]

        return module_names

    def show_options(self, options=None):
        spacer = '  '
        if self.UseModules != True:
            return []
        if self.Values:
            pattern = '%s%%s  %%s  %%s  %%s' % (spacer)
            key_len = len(max(self.Values, key=len))
            if key_len < 4: key_len = 4
            try:
                val_len = len(max([to_unicode(self.Values[x]) for x in self.Values], key=len))
            except Exception:
                val_len = 13
            if val_len < 13: val_len = 13
            write('')
            write(pattern % ('Name'.ljust(key_len), 'Current Value'.ljust(val_len), 'Required', 'Description'))
            write(pattern % (self.ruler * key_len, (self.ruler * 13).ljust(val_len), self.ruler * 8, self.ruler * 11))
            for key in sorted(self.Values):
                #print_error(str(key))
                value = self.Values[key] if self.Values[key] != None else ""
                reqd = 'no' if self.required[key] is False else 'yes'
                desc = self.description[key]
                try:
                    write(pattern % (
                    key.ljust(key_len), to_unicode(str(value)).ljust(val_len), to_unicode(reqd).ljust(8), desc))
                except Exception as error:
                    print(error)
                    #self.clear()
            print('')
        else:
            print('\n%sNo options available for this module\n' % (spacer))
            return
        try:
            if self.UseModulesObject.DEFINE:
                self.condition = self.UseModulesObject.DEFINE.keys()
                for key in self.condition:
                    Tiao = self.UseModulesObject.DEFINE[key]
                    TiaoKey = list(Tiao.keys())[0]
                    OpName=TiaoKey
                    if self.Values[TiaoKey] != Tiao[TiaoKey]:
                        #print(1)
                        #if name in self.DEFINE[OpName].Values:
                        ##    self.DEFINE[OpName].Values[name] = value
                        write("======================  %s  ================================" % (
                            TextColor(self.DEFINE[OpName].Name,COLO_RED)))
                        pattern = '%s%%s  %%s  %%s  %%s' % (spacer)
                        key_len = len(max(self.DEFINE[OpName].Values, key=len))
                        if key_len < 4: key_len = 4
                        try:
                            val_len = len(max([to_unicode(self.DEFINE[OpName].Values[x]) for x in self.DEFINE[OpName].Values], key=len))
                        except Exception:
                            #print("d")
                            val_len = 13
                        if val_len < 13: val_len = 13
                        print('')
                        print(pattern % (
                        'Name'.ljust(key_len), 'Current Value'.ljust(val_len), 'Required', 'Description'))
                        print(
                            pattern % (
                            self.ruler * key_len, (self.ruler * 13).ljust(val_len), self.ruler * 8, self.ruler * 11))
                        for key in sorted(self.DEFINE[OpName].Values):
                            value = self.DEFINE[OpName].Values[key] if self.DEFINE[OpName].Values[key] != None else ""
                            reqd = 'no' if self.DEFINE[OpName].required[key] is False else 'yes'
                            desc = self.DEFINE[OpName].description[key]
                            try:
                                write(pattern % (
                                    key.ljust(key_len), to_unicode(value).ljust(val_len),
                                    to_unicode(reqd).ljust(8), desc))
                            except AttributeError:
                                pass
                                # self.clear()
                        print('')
        except Exception as error:
            print(error)
        try:
            if self.UsePayload == True:
                write("==========================Payload:%s================================" % (
                TextColor(self.UsePayloadObject.Name)))
                pattern = '%s%%s  %%s  %%s  %%s' % (spacer)
                key_len = len(max(self.PayloadParameate, key=len))
                if key_len < 4: key_len = 4
                try:
                    val_len = len(max([to_unicode(self.PayloadParameate[x]) for x in self.PayloadParameate], key=len))
                except Exception:
                    val_len = 13
                if val_len < 13: val_len = 13
                print('')
                print(pattern % ('Name'.ljust(key_len), 'Current Value'.ljust(val_len), 'Required', 'Description'))
                print(
                    pattern % (self.ruler * key_len, (self.ruler * 13).ljust(val_len), self.ruler * 8, self.ruler * 11))
                for key in sorted(self.PayloadParameate):
                    value = self.PayloadParameate[key] if self.PayloadParameate[key] != None else ""
                    reqd = 'no' if self.UsePayloadObject.required[key] is False else 'yes'
                    desc = self.UsePayloadObject.description[key]
                    try:
                        write(pattern % (
                        key.upper().ljust(key_len), to_unicode(value).ljust(val_len), to_unicode(reqd).ljust(8), desc))
                    except AttributeError:
                        pass
                        #self.clear()
                print('')
        except Exception as e:
            print_error(e)

    def complete_set(self, text, line, begidx, endidx):
        if len(line.split(' '))==3:
            try:
                parame=line.split(' ')[1]
                if self.Choins[parame]!=None:
                    #print_error("d")
                    ChoinsPame= self.Choins[parame]
                    end_line = ' '.join(line.split(' ')[1:])

                    mline = end_line.partition(' ')[2]
                    offs = len(mline) - len(text)
                    return [s[offs:] for s in ChoinsPame if s.startswith(mline)]
            except Exception as error:
                pass
        SetKey=[]
        for key in sorted(self.Values):
            SetKey.append(key)
        if self.UsePayload==True:
            for key in sorted(self.PayloadParameate):
                SetKey.append(key)
        try:
            if self.UseModulesObject.DEFINE:
                self.condition = self.UseModulesObject.DEFINE.keys()
                for key in self.condition:
                    Tiao = self.UseModulesObject.DEFINE[key]
                    TiaoKey = list(Tiao.keys())[0]
                    OpName = TiaoKey
                    if self.Values[TiaoKey] != Tiao[TiaoKey]:
                        for key in sorted(self.DEFINE[OpName].Values):
                            SetKey.append(key)

        except:
            pass
        return [x for x in SetKey if x.startswith(text)]

    def do_show(self,line):
        if line=="modules":
            print_msg("-----------Show Modules ---------------------------")
            for name in self.ModulesList:
                write(" "+name+"\n")
        self.show_options()

    def complete_show(self, text, line, begidx, endidx):
        args = line.split()
        if len(args) > 1 and args[1].lower() == 'modules':
            if len(args) > 2:
                return [x for x in self.loaded_modules if x.startswith(args[2])]
            else:
                return [x for x in self.loaded_modules]
        #options = ["modules", "payload"]
        if self.UseModules==True:
            options=["modules","options","payload"]
        else:
            options = ["modules", "payload"]
        return [x for x in options if x.startswith(text)]







    def do_exploit(self,line):
        if line == "h":
            print_msg("Exploit Helper ")
            helper='''
                Run Modules the Exploit Function
                        def Exploit(self):
                            pass
            '''
            write(helper)
            return
        try:
            self.UseModulesObject.Status=0
            self.UseModulesObject.ExploitInit()
            self.UseModulesObject.Exploit()
            if self.UseModulesObject.Status==0:
                print_success("Modules Run Successfuly")
            else:
                print_error("Error Code:%d"%self.UseModulesObject.Status)
        except Exception as error:
            print(error)

    def complete_exploit(self, text, line, begidx, endidx):
        #args = text.split()
        '''
        if len(args) > 1 and args[1].lower() == 'modules':
            if len(args) > 2:
                return [x for x in self.loaded_modules if x.startswith(args[2])]
            else:
                return [x for x in self.loaded_modules]
        #options = ["modules", "payload"]'''

        options=["j","h","l"]
        return [x for x in options if x.startswith(text)]

