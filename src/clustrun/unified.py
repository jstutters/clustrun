import yaml
from clustrun.config import Config
from clustrun.hosts import Host


def read_unified(f):
    yaml_config = yaml.safe_load(f)
    config = Config()
    config.hosts = [Host(**h) for h in yaml_config.get("hosts", list())]
    config.setup_cmd = yaml_config.get("setup_cmd", "")
    config.cmd_tplt = yaml_config.get("cmd_tplt", "")
    config.sudo = yaml_config.get("sudo", True)
    config.tasks = yaml_config.get("tasks", list())
    config.ssh_user = yaml_config.get("ssh_user", "")
    config.ask_ssh_pass = yaml_config.get("ask_ssh_pass", False)
    return config
