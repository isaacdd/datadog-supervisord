A simple supervisord process and uptime check.

Getting Started
------------------
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
6. Edit supervisord.yaml to have your server details and the processes you want to monitor.
7. Place supervisord.py and supervisord.yaml in the checks and configuration folders. Path to these folders can be viewed via the agent info command.
8. Happy supervising!

License
----------
MIT License

