# This class runs various checks and returns a specific code?
import socket
import subprocess

def check_host_port(host,port,timeout=1):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        pass
    return False

def check_dns_net():
    return check_host_port('www.google.com', 80)

def check_general_net():
    return check_host_port('8.8.8.8', 53)

def check_host_via_ssh(host):
    return check_host_port(host, 22)

def ping_host(host):
    ret = subprocess.call("ping -c 1 -t 1 %s" % host,
            shell=True,
            stdout=open('/dev/null', 'w'),
            stderr=subprocess.STDOUT)
    if ret == 0:
        return True
    else:
        return False
