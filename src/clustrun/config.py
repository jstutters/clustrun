from fabric import Config as ConnectionConfig


class Config:
    def __init__(self):
        self._hosts = []
        self._setup_cmd = ""
        self._cmd_tplt = ""
        self._sudo = False
        self._tasks = []
        self._ssh_user = ""
        self._sudo_pass = ""
        self._ssh_pass = ""

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

    @property
    def sudo(self):
        return self._sudo

    @sudo.setter
    def sudo(self, v):
        if not isinstance(v, bool):
            raise ValueError
        self._sudo = v

    @property
    def sudo_pass(self):
        return self._sudo_pass

    @sudo_pass.setter
    def sudo_pass(self, v):
        if not isinstance(v, str):
            raise ValueError
        self._sudo_pass = v

    @property
    def ssh_pass(self):
        return self._ssh_pass

    @ssh_pass.setter
    def ssh_pass(self, v):
        if not isinstance(v, str):
            raise ValueError
        self._ssh_pass = v

    @property
    def ssh_user(self):
        return self._ssh_user

    @ssh_user.setter
    def ssh_user(self, v):
        if not isinstance(v, str):
            raise ValueError
        self._ssh_user = v

    @property
    def connection(self):
        overrides = {"user": self._ssh_user, "sudo": {"password": self._sudo_pass}}
        if self.ssh_pass:
            overrides["connect_kwargs"] = {"password": self._ssh_pass}
        return ConnectionConfig(overrides=overrides)

    def to_dict(self):
        return {
            "hosts": [h.to_dict() for h in self._hosts],
            "setup_cmd": self._setup_cmd,
            "cmd_tplt": self._cmd_tplt,
            "sudo": self._sudo,
            "tasks": self._tasks,
            "ssh_user": self._ssh_user,
        }
