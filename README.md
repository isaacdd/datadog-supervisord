A simple supervisord process and uptime check. Check collects the following:

1. Service check on each process (Critical, Warning, OK)
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
4. Reload supervisor.
5. Clone this repository.
6. Install `xmlrpclib`.
7. Edit supervisord.yaml to have your server details and the processes you want to monitor.
8. Place supervisord.py and supervisord.yaml in the checks and configuration folders. Path to these folders can be viewed via the agent info command.
9. Restart Datadog agent.
10. Create alerts, query value widgets, event streams and graphs to monitor your processes.

Happy supervisoring!

Links and Resources
-------------------
1. [Datadog Agent on Github](https://github.com/DataDog/dd-agent/)
2. [Datadog Documentation](http://docs.datadoghq.com/)
3. [Supervisord XML-RPC API Documentation](http://supervisord.org/api.html)

License
-------
MIT License

