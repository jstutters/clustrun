import re


class Host():
    def __init__(self, hostname, n_jobs=1):
        self.hostname = hostname
        self.n_jobs = n_jobs

    def __repr__(self):
        return 'Host({0!r}, n_jobs={1})'.format(self.hostname, self.n_jobs)


def read_hosts_file(hosts_file):
    exp = re.compile(r'^(?P<hostname>\S*){1}\s*(n=(?P<n_jobs>[0-9]+))?')
    host_list = [exp.match(l.strip()) for l in hosts_file.readlines()]
    hosts = []
    for h in host_list:
        host_args = {
            'hostname': h.group('hostname')
        }
        if h.group('n_jobs'):
            host_args['n_jobs'] = int(h.group('n_jobs'))
        hosts.append(Host(**host_args))
    return hosts
