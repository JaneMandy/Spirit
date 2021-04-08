from SpiritCore.System import *

class Payload:
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