class Config():
    def __init__(self):
        self._hosts = []
        self._setup_cmd = ""
        self._cmd_tplt = ""
        self._tasks = []

    @property
    def hosts(self):
        return self._hosts
    
    @hosts.setter
    def hosts(self, v):
        if not isinstance(v, (list, tuple)):
            raise ValueError
        self._hosts = v

    @property
    def setup_cmd(self):
        return self._setup_cmd
    
    @setup_cmd.setter
    def setup_cmd(self, v):
        if not isinstance(v, str):
            raise ValueError
        self._setup_cmd = v

    @property
    def cmd_tplt(self):
        return self._cmd_tplt
    
    @cmd_tplt.setter
    def cmd_tplt(self, v):
        if not isinstance(v, str):
            raise ValueError
        self._cmd_tplt = v

    @property
    def tasks(self):
        return self._tasks
    
    @tasks.setter
    def tasks(self, v):
        if not isinstance(v, (list, tuple)):
            raise ValueError
        self._tasks = v
