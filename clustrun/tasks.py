from multiprocessing import JoinableQueue


def read_tasks_file(tasks_file):
    return [l.strip() for l in tasks_file.readlines()]


def read_cmd_file(cmd_file):
    return '\n'.join([l.strip() for l in cmd_file.readlines()])


def make_queue(tasks):
    q = JoinableQueue()
    for t in tasks:
        q.put(t)
    return q
