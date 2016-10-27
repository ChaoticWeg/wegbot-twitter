import ConfigParser

def read(_file):
    config = ConfigParser.ConfigParser()
    config.read(_file)

    result = {}
    for section in config.sections():
        result[section] = {}
    
        for option in config.options(section):
            result[section][option] = config.get(section, option)

    return result
