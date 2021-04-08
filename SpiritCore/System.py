import  sys
import  datetime
try:
    try:
        import readline
    except ImportError:
        import pyreadline as readline
    HAVE_READLINE = True
except:
    HAVE_READLINE = False
mswindows = (sys.platform == "win32")
COLORIZEMAP = {"[-]" : {"fg" : "red",     "attr" : "bold"},
               "[+]" : {"fg" : "green",   "attr" : "bold"},
               "[!]" : {"fg" : "red",     "attr" : "bold"},
               "[*]" : {"fg" : "blue",   "attr" : "bold"},
               "[?]" : {"fg" : "yellow",    "attr" : "bold"}}
COLO_RED        = {"fg" : "red",     "attr" : "bold"}
COLO_BLUE       = {"fg" : "blue",    "attr" : "bold"}
COLO_GREEN      = {"fg" : "green",    "attr" : "bold"}
COLO_YELLOW     = {"fg" : "yellow",    "attr" : "bold"}
VMAP = {"[-]"  : {"fg" : "magenta",   "attr" : "bold"},
        "[+]" : {"fg" : "magenta",   "attr" : "bold"},
        "[!]" : {"fg" : "magenta",   "attr" : "bold"},
        "[*]" : {"fg" : "magenta",   "attr" : "bold"},
        "[?]" : {"fg" : "magenta",   "attr" : "bold"}}

mswindows = (sys.platform == "win32")


class Parame:
    Name=""
    Object=None
    Values={}
    required={}
    description={}

    def GetParameate(self, Name):
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





def formattime(self,timestamp=None):
	if timestamp is None:
		timestamp = datetime.datetime.now()
	timestamp = str(timestamp)
	timestamp = timestamp.replace(' ', '.')
	return timestamp.replace(':', '.')
def TimeDate():
	timestamp = datetime.datetime.now()
	timestamp = str(timestamp)
	#timestamp = timestamp.replace(' ', '.')
	DATE=timestamp.split(" ")
	DateTime1=DATE[0].split("-")
	DateTime2=DATE[1].split(":")
	if int(DateTime2[0])<12:
		AMPM="AM"
	else:
		AMPM="PM"
	ret="%s:%s %s %s/%s/%s    "%(DateTime2[0],DateTime2[1],AMPM,DateTime1[1],DateTime1[2],DateTime1[0])
	return ret
#def print_time(Text):
	# "%s - %s"%(TimeDate(),Text)




def color(fg=None, bg=None, attr=None):
    attrs  = 'none bold faint italic underline blink fast reverse concealed'
    colors = 'grey red green yellow blue magenta cyan white'
    attrs  = dict((s,i) for i,s in enumerate(attrs.split()))
    colors = dict((s,i) for i,s in enumerate(colors.split()))
    fgoffset, bgoffset = 30,40
    cmd = ["0"]

    if fg in colors:
       cmd.append("%s" % (colors[fg] + fgoffset))
    if bg in colors:
        cmd.append("%s" % (colors[bg] + bgoffset))
    if attr:
        for a in attr.split():
            if a in attrs:
                cmd.append("%s" % attrs[a])

    return "\033[" + ";".join(cmd) + "m"

def TextColor(line,COLOR_ATT=COLO_GREEN):
    plen = len(line)
    index = -1
    text=line
    try:
        r = index + plen
        line = (color(**COLOR_ATT) +line +color() )
        return line
    except:
        return  text
def colorize(line):
    colormap=VMAP
    if colormap == COLORIZEMAP:
        colormap = VMAP
    else:
        colormap = COLORIZEMAP
    for pattern, attrs in colormap.items():
        plen = len(pattern)
        index = line.find(pattern)
        if colormap == VMAP:
            pattern = "[TF]"
        if index != -1:
            r = index + plen
            line = (line[:index] +
            color(**attrs) +
            pattern +
                        color() +
            line[r:])
            return line
    return line

def write( line,end="\n"):
    try:
        if mswindows:
            readline.GetOutputFile().write_color(colorize(line)+end)
        else:
            sys.stdout.write(colorize(line)+end)
    except LookupError:
         # We failed to print in color.  This is a problem looking up the encoding
        # Permanently disable color and continue
        print(line)

def print_error( line,time=1):
    if time==0:
        line= TimeDate()+""+line
    write("[-] " + line)

def print_success( line,time=1):
    if time==0:
        line= TimeDate()+""+line
    write("[+] " + line)

def print_warning( line,time=1):
    if time==0:
        line= TimeDate()+""+line
    write("[!] " + line)

def print_msg( line,time=1):
    if time==0:
        line= TimeDate()+""+line
    write("[*] " + line)