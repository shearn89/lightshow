# This class should control the output of checks and trigger different light modes.

import os
import time
import datetime
import signal
import sys
import threading

from twisted.web import server, resource
from twisted.internet import reactor,endpoints

from monitor import checks,status

STATUS = "/dev/shm/monitor-status.txt"

def run_checks(status):
    dns_net = checks.Check('Name Based Internet',checks.check_dns_net())
    status.add(dns_net)
    ip_net = checks.Check('IP Based Internet',checks.check_general_net())
    status.add(ip_net)
    modem = checks.Check('Modem',checks.check_host_port("192.168.1.254", 80))
    status.add(modem)
    
    dns = checks.Check('Local DNS', checks.check_host_port("192.168.1.2", 53))
    status.add(dns)
    loki = checks.Check('Loki', checks.check_host_via_ssh("192.168.1.2"))
    status.add(loki)
    loki_web = checks.Check('Loki Web Server', checks.check_host_port('192.168.1.2', 80))
    status.add(loki_web)
    
    ap_two = checks.Check('Asgard_Too Wifi', checks.check_host_port("192.168.1.253", 80))
    status.add(ap_two)
    
    cassini = checks.Check('Cassini', checks.check_host_via_ssh("192.168.1.252"))
    status.add(cassini)
    techworld = checks.Check('TechWorld Server', checks.check_host_port("192.168.1.252", 64004))
    status.add(techworld)
    
    freya = checks.Check('Freya', checks.check_host_via_ssh("192.168.1.20"))
    status.add(freya)
    freya_web = checks.Check('Freya Web Server', checks.check_host_port('192.168.1.20', 80))
    status.add(freya_web)

### Checks setup
class checkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.health_status = status.Status()
        self.signal = True
    
    def run(self):
        print "running checks..."
        run_checks(self.health_status)
        ## Lock this?
        ostring = "%s\n" % datetime.datetime.now()
        print "building string"
        for check in self.health_status:
            ostring += "%s: %s\n" % (check.name, 'up' if check.status else 'down')
        print "built"
        with open(STATUS, 'w') as output:
            output.write(ostring)
        print "written"
### end checks setup

class MonServer(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def render_GET(self, request):
        self.numberRequests += 1
        request.setHeader(b"content-type", b"text/plain")
        content = u"I am request #{}\n".format(self.numberRequests)
        return content.encode("ascii")

if __name__ == "__main__":
    tmanager = []
    t1 = checkThread()
    t1.start()

    endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(MonServer()))
    print "starting twisted server"
    reactor.run()
    print "joining sleep thread"
    t1.join()
