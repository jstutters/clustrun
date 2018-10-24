from queue import Empty
import signal
import click
from fabric import Config as ConnectionConfig
from .hosts import read_hosts_file
from .tasks import read_cmd_file, read_tasks_file, make_queue
from .worker import launch_workers, setup_workers, wait_for_workers


@click.command()
@click.argument('tasks', nargs=-1)
@click.option('--hosts-file', 'hosts_file', default='hosts', help='Path to hosts file', type=click.File())
@click.option('--hosts', help='Comma-separated list of hosts', type=str)
@click.option('--cmd', 'cmd_tplt', help='Command template', type=str)
@click.option('--cmd-file', 'cmd_file', help='Path to command template file', type=click.File())
@click.option('--setup-cmd', 'setup_cmd', help='Setup commmand', type=str)
@click.option('--setup-cmd-file', 'setup_cmd_file', help='Path to setup command file', type=click.File())
@click.option('--tasks-file', 'tasks_file', help='Path to file listing tasks', type=click.File())
@click.option('--sudo-pass', 'sudo_pass', prompt=True, hide_input=True, confirmation_prompt=False)
def run(tasks, hosts_file, hosts, cmd_tplt, cmd_file, setup_cmd, setup_cmd_file, tasks_file, sudo_pass):
    """Run a list of tasks on using a pool of servers."""
    server_list = read_hosts_file(hosts_file)
    connection_config = ConnectionConfig(overrides={'sudo': {'password': sudo_pass}})

    if tasks_file:
        tasks = read_tasks_file(tasks_file)

    if cmd_file:
        cmd_tplt = read_cmd_file(cmd_file)

    if setup_cmd_file:
        setup_cmd = read_cmd_file(setup_cmd_file)

    if setup_cmd:
        setup_workers(server_list, connection_config, setup_cmd)

    global q
    q = make_queue(tasks)

    signal.signal(signal.SIGINT, int_handler)

    workers = launch_workers(server_list, q, connection_config, cmd_tplt)

    wait_for_workers(q, workers)



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
