
#   FOFA Inf
Fofa_Mail=""
Fofa_Keys=""

#   XRAY PATH
Xray=""

#   SQLMAP PATH
Sqlmap=""


def LoadConfig(configKey=""):
    """[summary]
    
    [description]
    
    Keyword Arguments:
        configKey {str} -- [description] (default: {""})
    
    Returns:
        [type] -- [description]
    """
    import json
    options = None
    with open("data/Config/config.json", mode="r", encoding="utf-8") as file:
        data = json.load(file, encoding='utf-8')
    if(configKey != ""):
        options = data[configKey]
    else:
        options = data
    return options
