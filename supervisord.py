import time

from checks import AgentCheck

import xmlrpclib

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '9001'
DEFAULT_SERVER = 'server'

OK = AgentCheck.OK
CRITICAL = AgentCheck.CRITICAL
UNKNOWN = AgentCheck.UNKNOWN

DD_STATUS = {
    'STOPPED': CRITICAL,
    'STARTING': OK,
    'RUNNING': OK,
    'BACKOFF': UNKNOWN,
    'STOPPING': CRITICAL,
    'EXITED': CRITICAL,
    'FATAL': CRITICAL,
    'UNKNOWN': UNKNOWN
}

PROCESS_STATUS = {
    CRITICAL: 'down',
    OK: 'up',
    UNKNOWN: 'unknown'
}

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def time_formatter(s):
    return time.strftime(TIME_FORMAT, time.localtime(s))


class SupervisordCheck(AgentCheck):

    def check(self, instance):
        server_name = instance.get('name', DEFAULT_SERVER)
        server = self._connect(instance)
        count = {
            AgentCheck.OK: 0,
            AgentCheck.CRITICAL: 0,
            AgentCheck.UNKNOWN: 0
        }

        # Report service checks and uptime for each process
        proc_names = instance.get('proc_names')
        if proc_names and len(proc_names):
            processes = [server.supervisor.getProcessInfo(p) for p in proc_names]
        else:
            processes = server.supervisor.getAllProcessInfo()

        for proc in processes:
            proc_name = proc['name']
            tags = ['supervisord',
                    'server:%s' % server_name,
                    'process:%s' % proc_name]

            # Report Service Check
            status = DD_STATUS[proc['statename']]
            msg = self._build_message(proc)
            count[status] += 1
            self.service_check('supervisord.process.check',
                               status, tags=tags, message=msg)
            # Report Uptime
            uptime = self._extract_uptime(proc)
            self.gauge('supervisord.process.uptime', uptime, tags=tags)

        # Report counts by status
        tags = ['supervisord', 'server:%s' % server_name]
        for proc_status in PROCESS_STATUS:
            self.gauge('supervisord.process.count', count[proc_status],
                       tags=tags + ['status:%s' % PROCESS_STATUS[proc_status]])

    def _connect(self, instance):
        host = instance.get('host', DEFAULT_HOST)
        port = instance.get('port', DEFAULT_PORT)
        user = instance.get('user', None)
        password = instance.get('pass', None)
        auth = '%s:%s@' % (user, password) if user and password else ''
        return xmlrpclib.Server('http://%s%s:%s/RPC2' % (auth, host, port))

    def _extract_uptime(self, proc):
        desc = proc['description']
        if proc['statename'] == 'RUNNING' and 'uptime' in desc:
            h, m, s = desc.split('uptime ')[1].split(':')
            return int(s) + 60 * (int(m) + 60 * int(h))
        else:
            start, stop, now = int(proc['start']), int(proc['stop']), int(proc['now'])
            return 0 if stop >= start else now - start

    def _build_message(self, proc):
        start, stop, now = int(proc['start']), int(proc['stop']), int(proc['now'])
        proc['now_str'] = time_formatter(now)
        proc['start_str'] = time_formatter(start)
        proc['stop_str'] = '' if stop == 0 else time_formatter(stop)

        return """Current time: %(now_str)s
Process name: %(name)s
Process group: %(group)s
Description: %(description)s
Error log file: %(stderr_logfile)s
Stdout log file: %(stdout_logfile)s
Log file: %(logfile)s
State: %(statename)s
Start time: %(start_str)s
Stop time: %(stop_str)s
Exit Status: %(exitstatus)s""" % proc
