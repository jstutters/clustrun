from datetime import datetime
from multiprocessing import Process
from queue import Empty
import click
from fabric import Connection


def log_date():
    return datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')


def worker(q, hostname, config, cmd_template):
    while True:
        c = Connection(hostname, config=config)
        try:
            t = q.get(timeout=5)
        except Empty:
            break
        start_time = datetime.now()
        print(log_date(), 'Running', t, 'on', hostname)
        cmd = cmd_template.format(t)
        try:
            c.sudo(cmd, hide='both')
        except Exception:
            duration = datetime.now() - start_time
            err_msg = '{0} Error during {1} on {2} after {3}'.format(
                log_date(), t, hostname, duration
            )
            click.secho(err_msg, fg='red')
        else:
            duration = datetime.now() - start_time
            finish_msg = '{0} Finished {1} on {2} after {3}'.format(
                log_date(), t, hostname, duration
            )
            click.secho(finish_msg, fg='green')
        q.task_done()
        c.close()


def setup_workers(server_list, connection_config, cmd):
    for h in server_list:
        print('Configuring ', h, '... ', end='', sep='', flush=True)
        c = Connection(h, config=connection_config)
        for l in cmd.split('\n'):
            c.sudo(l, hide='both')
        print('done')


def launch_workers(server_list, q, connection_config, cmd_template):
    workers = []
    for h in server_list:
        p = Process(target=worker, args=(q, h, connection_config, cmd_template))
        p.start()
        workers.append(p)
    return workers


def wait_for_workers(q, processes):
    q.join()
    for p in processes:
        p.join()
