import yaml
from clustrun.config import Config


def read_unified(f):
    yaml_config = yaml.load(f)
    config = Config()
    config.hosts = yaml_config.get('hosts')
    config.setup_cmd = yaml_config.get('setup_cmd')
    config.cmd_tplt = yaml_config.get('cmd_tplt')
    config.tasks = yaml_config.get('tasks')
    return config
