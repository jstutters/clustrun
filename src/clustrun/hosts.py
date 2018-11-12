import re


class Host():
    def __init__(self, hostname, port=22, n_jobs=1):
        self.hostname = hostname
        self.port = port
        self.n_jobs = n_jobs

    def __repr__(self):
        return 'Host({0!r}, port={1}, n_jobs={2})'.format(self.hostname, self.port, self.n_jobs)

    def to_dict(self):
        return {
            'hostname': self.hostname,
            'port': self.port,
            'n_jobs': self.n_jobs
        }


def read_hosts_file(hosts_file):
    exp = re.compile(r'^(?P<hostname>\S*){1}\s*(port=(?P<port>[0-9]+))?\s*(n=(?P<n_jobs>[0-9]+))?')
    host_list = [exp.match(l.strip()) for l in hosts_file.readlines()]
    hosts = []
    for h in host_list:
        host_args = {
            'hostname': h.group('hostname')
        }
        if h.group('port'):
            host_args['port'] = int(h.group('port'))
        if h.group('n_jobs'):
            host_args['n_jobs'] = int(h.group('n_jobs'))
        hosts.append(Host(**host_args))
    return hosts
