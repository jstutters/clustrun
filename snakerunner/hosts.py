from threading import Semaphore
from .server import Server


def read_hosts_file(hosts_file):
    return [l.strip() for l in hosts_file.readlines()]
