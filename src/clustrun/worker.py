from datetime import datetime
from multiprocessing import Process
from queue import Empty

import click
from fabric import Connection

from clustrun.result import Result


def log_date():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def worker(q, rq, hostname, config, port=22):
    while True:
        t = q.get(block=False)
        if t is None:
            # None is the sentinel to indicate all queued items have been
            # processed
            break
        start_time = datetime.now()
        print(log_date(), "Running", t, "on", hostname)
        cmd = config.cmd_tplt.format(t)
        r = None
        try:
            c = Connection(hostname, port=port, config=config.connection)
        except Exception:
            err_msg = "{0} Connection failed to {1}".format(log_date(), hostname)
            click.secho(err_msg, fg="red")
            break
        try:
            if config.sudo:
                r = c.sudo(cmd, hide="both", warn=True)
            else:
                r = c.run(cmd, hide="both", warn=True)
        except Exception as e:
            click.secho("Exception running command: " + str(e), fg="red")
            break
        else:
            duration = datetime.now() - start_time
            if r.exited == 0:
                finish_msg = "{0} Finished {1} on {2} after {3}".format(
                    log_date(), t, hostname, duration
                )
                click.secho(finish_msg, fg="green")
            else:
                err_msg = "{0} Error during {1} on {2} after {3}".format(
                    log_date(), t, hostname, duration
                )
                click.secho(err_msg, fg="red")
            result = Result(
                hostname=hostname,
                task=t,
                stdout=r.stdout,
                stderr=r.stderr,
                exit_code=r.exited,
                duration=duration,
            )
            rq.put(result)
        finally:
            q.task_done()
            c.close()
    click.echo("Worker on {0} is done".format(hostname))


def setup_workers(config):
    for h in config.hosts:
        print("Configuring ", h.hostname, "... ", end="", sep="", flush=True)
        c = Connection(h.hostname, config=config.connection)
        for l in config.setup_cmd.split("\n"):
            if config.sudo:
                c.sudo(l, hide="both")
            else:
                c.run(l, hide="both")
        print("done")


def launch_workers(config, q, rq):
    workers = []
    for h in config.hosts:
        for _ in range(h.n_jobs):
            p = Process(
                target=worker,
                args=(q, rq, h.hostname, config, h.port),
                name="clustrun.worker",
            )
            p.start()
            workers.append(p)
    return workers


def wait_for_workers(processes, results_queue):
    results = []
    while processes:
        while True:
            try:
                results.append(results_queue.get(block=False))
            except Empty:
                break
        for p in processes:
            p.join(0.1)
        processes = [p for p in processes if p.is_alive()]
    return results
