class Result():
    def __init__(self, hostname, task, stdout, stderr, exit_code, duration):
        self.hostname = hostname
        self.task = task
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code
        self.duration = duration

    def __repr__(self):
        return 'Result({0.hostname!r}, {0.task!r}, {0.duration!r}, {0.stdout!r})'.format(self)
