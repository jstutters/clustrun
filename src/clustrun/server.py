from fabric import Connection, Config


class Server():
    def __init__(self, hostname, pool, sudo_pass):
        self.hostname = hostname
        self.pool = pool
        config = Config(overrides={'sudo': {'password': sudo_pass}})

    def run(self, cmd):
        print("running", cmd, "on", self.hostname)
        self.connection = Connection(hostname, config=config)
        res = self.connection.sudo(cmd, hide='both', pty=True)
        self.pool.release_server(self)
