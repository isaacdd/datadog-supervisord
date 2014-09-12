from checks import AgentCheck

import xmlrpclib

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '9001'
STATUS_MAP = {
    'STOPPED': AgentCheck.CRITICAL,
    'STARTING': AgentCheck.OK,
    'RUNNING': AgentCheck.OK,
    'BACKOFF': AgentCheck.UNKNOWN,
    'STOPPING': AgentCheck.WARNING,
    'EXITED': AgentCheck.CRITICAL,
    'FATAL': AgentCheck.CRITICAL,
    'UNKNOWN': AgentCheck.UNKNOWN
}


class SupervisordCheck(AgentCheck):

    def check(self, instance):
        server = self._connect(instance)
        proc_names = instance.get('proc_names', [])
        for proc_name in proc_names:
            proc_info = server.supervisor.getProcessInfo(proc_name)
            status = STATUS_MAP[proc_info['statename']]
            uptime = proc_info['now'] - proc_info['start']
            tags = ['supervisord', 'proc_name:%s' % proc_info['name']]
            self.service_check('supervisord.process.check', status, tags=tags)
            self.gauge('supervisord.process.uptime', uptime, tags=tags)

    def _connect(self, instance):
        host = instance.get('host', DEFAULT_HOST)
        port = instance.get('port', DEFAULT_PORT)
        user = instance.get('user', None)
        password = instance.get('pass', None)
        auth = '%s:%s@' % (user, password) if user and password else ''
        return xmlrpclib.Server('http://%s%s:%s/RPC2' % (auth, host, port))
