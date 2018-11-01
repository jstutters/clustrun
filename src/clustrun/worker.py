from datetime import datetime
from multiprocessing import Process
from queue import Empty

import click
from fabric import Connection

from clustrun.result import Result


def log_date():
    return datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')


def worker(q, rq, hostname, config):
    while True:
        c = Connection(hostname, config=config.connection)
        try:
            t = q.get(timeout=5)
        except Empty:
            break
        start_time = datetime.now()
        print(log_date(), 'Running', t, 'on', hostname)
        cmd = config.cmd_tplt.format(t)
        try:
            if config.sudo:
                r = c.sudo(cmd, hide='both')
            else:
                r = c.run(cmd, hide='both')
        except KeyboardInterrupt:
            break
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
        result = Result(
            hostname=hostname,
            task=t,
            stdout=r.stdout,
            stderr=r.stderr,
            exit_code=r.exited,
            duration=duration
        )
        rq.put(result)
        c.close()


def setup_workers(config):
    for h in config.hosts:
        print('Configuring ', h.hostname, '... ', end='', sep='', flush=True)
        c = Connection(h.hostname, config=config.connection)
        for l in config.setup_cmd.split('\n'):
            if config.sudo:
                c.sudo(l, hide='both')
            else:
                c.run(l, hide='both')
        print('done')


def launch_workers(config, q, rq):
    workers = []
    for h in config.hosts:
        for _ in range(h.n_jobs):
            p = Process(target=worker, args=(q, rq, h.hostname, config))
            p.start()
            workers.append(p)
    return workers


def wait_for_workers(processes, q):
    q.join()
    for p in processes:
        p.join()
