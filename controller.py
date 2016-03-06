# This class should control the output of checks and trigger different light modes.

import monitor.checker

class Check:
    def __init__(self, name, status, priority=0):
        self.name = name
        self.status = status
        self.priority = priority
    
class Status:
    def __init__(self):
        self.checks = []
        self.index = 0

    def add(self, check):
        self.checks.append(check)
    
    def __iter__(self):
        return self

    def next(self):
        try:
            result = self.checks[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

def print_result(text, value):
    if value:
        print text + " is up"
    else:
        print text + " is down"

def run_checks(status):
    dns_net = Check('Name Based Internet',monitor.checker.check_dns_net())
    status.add(dns_net)
    ip_net = Check('IP Based Internet',monitor.checker.check_general_net())
    status.add(ip_net)
    modem = Check('Modem',monitor.checker.check_host_port("192.168.1.254", 80))
    status.add(modem)
    
    dns = Check('Local DNS', monitor.checker.check_host_port("192.168.1.2", 53))
    status.add(dns)
    loki = Check('Loki', monitor.checker.check_host_via_ssh("192.168.1.2"))
    status.add(loki)
    loki_web = Check('Loki Web Server', monitor.checker.check_host_port('192.168.1.2', 80))
    status.add(loki_web)
    
    ap_two = Check('Asgard_Too Wifi', monitor.checker.check_host_port("192.168.1.253", 80))
    status.add(ap_two)
    
    cassini = Check('Cassini', monitor.checker.check_host_via_ssh("192.168.1.252"))
    status.add(cassini)
    techworld = Check('TechWorld Server', monitor.checker.check_host_port("192.168.1.252", 64004))
    status.add(techworld)
    
    freya = Check('Freya', monitor.checker.check_host_via_ssh("192.168.1.20"))
    status.add(freya)
    freya_web = Check('Freya Web Server', monitor.checker.check_host_port('192.168.1.20', 80))
    status.add(freya_web)

if __name__ == "__main__":
    print "running checks..."
    health_status = Status()
    run_checks(health_status)
    for check in health_status:
        print "%s: %s" % (check.name, 'up' if check.status else 'down')
