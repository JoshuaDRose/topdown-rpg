try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser # ver. < 3.0


class Configure(ConfigParser):
    """
        Config parser permits the instantiation of
        .ini file formats as a file-io object
    """
    def __init__(self, path):
        """ Configure constructure should be able to load ConfigParser methods """
        ConfigParser.__init__(self)
        self.path = path


