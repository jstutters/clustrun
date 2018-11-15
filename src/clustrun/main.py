import json
import os
import signal
import sys
from datetime import datetime
from multiprocessing import Queue, current_process
from queue import Empty

import click

from .config import Config
from .hosts import read_hosts_file
from .report import make_report, print_report
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
@click.option('--no-sudo', 'use_sudo', flag_value='no', help='Execute tasks without sudo')
@click.option('--ask-ssh-pass', 'ask_ssh_pass', flag_value='yes', help='Ask for an SSH password')
@click.option('-f', '--config', 'config_file', type=click.File())
@click.option('-r', '--report', 'report_file', type=click.File('w'))
def run(hosts_file, setup_cmd_file, cmd_file, tasks_file, ssh_user, use_sudo,
        ask_ssh_pass, config_file, report_file):
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
    if ask_ssh_pass is not None:
        config.ask_ssh_pass = True
    else:
        config.ask_ssh_pass = False

    if config.ask_ssh_pass:
        config.ssh_pass = click.prompt('SSH password', hide_input=True)

    if config.sudo:
        config.sudo_pass = click.prompt('Sudo password', hide_input=True)

    start_time = datetime.now()

    if config.setup_cmd:
        setup_workers(config)

    global ctrlc_used
    ctrlc_used = False

    global q
    global workers
    q = make_queue(config.tasks)
    results = Queue()

    signal.signal(signal.SIGINT, int_handler)

    workers = launch_workers(config, q, results)

    wait_for_workers(workers)

    report = make_report(config, start_time, results)
    if report_file:
        json.dump(report, report_file)
    sys.stdout.flush()
    sys.stderr.flush()
    print_report(report)


def int_handler(signum, frame):
    """Rapidly empty the queue so we're left with only running tasks."""
    global ctrlc_used
    if not ctrlc_used:
        ctrlc_used = True
        if current_process().name == "MainProcess":
            click.secho("Cancelling all queued tasks...")
            while not q.empty():
                try:
                    q.get(timeout=1)
                    q.task_done()
                except Empty:
                    break
            wait_for_workers(workers)
    else:
        if current_process().name == "MainProcess":
            click.secho("Terminating workers...")
            for w in workers:
                w.terminate()
                w.join()


if __name__ == "__main__":
    run()
