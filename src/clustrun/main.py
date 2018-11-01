import math
import os
import signal
from queue import Empty
from multiprocessing import Queue

import click

from .config import Config
from .hosts import read_hosts_file
from .tasks import make_queue, read_cmd_file, read_tasks_file
from .unified import read_unified
from .worker import launch_workers, setup_workers, wait_for_workers


@click.command()
@click.option('-h', '--hosts', 'hosts_file',
              help='Path to hosts file', type=click.File())
@click.option('-s', '--setup', 'setup_cmd_file',
              help='Path to setup command file', type=click.File())
@click.option('-c', '--cmd', 'cmd_file',
              help='Path to command template file', type=click.File())
@click.option('-t', '--tasks', 'tasks_file',
              help='Path to file listing tasks', type=click.File())
@click.option('--ssh-user', 'ssh_user',
              help='SSH username', type=str, default=lambda: os.environ.get('USER', ''))
@click.option('--sudo', 'use_sudo', flag_value='yes', help='Execute tasks with sudo')
@click.option('--no-sudo', 'use_sudo', flag_value='no', help='Execute tasks with sudo')
@click.argument('config_file', type=click.File())
def run(hosts_file, setup_cmd_file, cmd_file, tasks_file, ssh_user, use_sudo, config_file):
    """Run a list of tasks on using a pool of servers."""
    config = Config()
    if config_file:
        config = read_unified(config_file)

    if hosts_file:
        config.hosts = read_hosts_file(hosts_file)
    if setup_cmd_file:
        config.setup_cmd = read_cmd_file(setup_cmd_file)
    if cmd_file:
        config.cmd_tplt = read_cmd_file(cmd_file)
    if tasks_file:
        config.tasks = read_tasks_file(tasks_file)
    if ssh_user:
        config.ssh_user = ssh_user
    if use_sudo is not None:
        config.sudo = use_sudo == 'yes'

    if config.sudo:
        config.sudo_pass = click.prompt('Sudo password', hide_input=True)

    if config.setup_cmd:
        setup_workers(config)

    global q
    q = make_queue(config.tasks)
    results = Queue()

    signal.signal(signal.SIGINT, int_handler)

    workers = launch_workers(config, q, results)

    wait_for_workers(workers, q)

    results_list = []
    while True:
        try:
            r = results.get(block=False)
        except Empty:
            break
        results_list.append(r)
    print(sum([r.duration.total_seconds() for r in results_list]) / len(results_list))


def int_handler(signum, frame):
    """Rapidly empty the queue so we're left with only running tasks."""
    global q
    while not q.empty():
        try:
            q.get(timeout=5)
            q.task_done()
        except Empty:
            break


if __name__ == "__main__":
    run()
