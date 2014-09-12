A simple supervisord process and uptime check. Check collects the following:

1. Service check on each process (Critical, OK, Unkown)
2. Uptime of each process
3. Process count by status metrics

Getting Started
---------------
1. Install or upgrade to Dataodg agent >= 5.0.
2. Configure `inet_http_server` in `/etc/supervisord.conf` (username and password are optional):

    ```
    [inet_http_server]
    port:localhost:9001
    username:user
    password:pass
    ```
3. Reload supervisor.
4. Clone this repository.
5. Install `xmlrpclib`.
6. Edit supervisord.yaml to have your server details and the processes you want to monitor.
7. Place supervisord.py and supervisord.yaml in the checks and configuration folders. Path to these folders can be viewed via the agent info command.
8. Restart Datadog agent.
9. Create alerts, query value widgets, event streams and graphs to monitor your processes.
10. Happy supervisoring!

Links and Resources
-------------------
1. [Datadog Agent on Github](https://github.com/DataDog/dd-agent/)
2. [Datadog Documentation](http://docs.datadoghq.com/)
3. [Supervisord XML-RPC API Documentation](http://supervisord.org/api.html)

License
-------
MIT License

