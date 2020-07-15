# python-libscrt

libscrt - Decode session files

```
Usage: libscrt <session_file.ini> [<session_fileN.ini> ...]
``` 

The output of this command will be the sshpass command to be run for each session file

```
$ libscrt /home/jordi/sessions/demo_grouo/demo_host.ini
sshpass -p"passw0rd" ssh -p 22 root@1.2.3.4
````