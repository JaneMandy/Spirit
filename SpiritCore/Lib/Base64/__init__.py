from base64 import *
import  sys
def Base64Encode(text):
    try:
        return str(b64encode(text), encoding = "utf-8")
    except:
        try:
            return str(b64encode(bytes(text, encoding="utf8")), encoding="utf-8")
        except:
            return b64encode(text)
def Base64Decode(text):
    if sys.version_info.major == 2:
        return b64decode(text)
    else:
        return str(b64decode(text), encoding = "utf-8")