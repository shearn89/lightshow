# This class should control the output of checks and trigger different light modes.

from flask import Flask
from monitor import checks,status

### Webserver Setup
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Pi!"

def print_result(text, value):
    if value:
        print text + " is up"
    else:
        print text + " is down"
###

### Checks setup
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
###

if __name__ == "__main__":
    print "running checks..."
    health_status = status.Status()
    run_checks(health_status)
    for check in health_status:
        print "%s: %s" % (check.name, 'up' if check.status else 'down')
    
    # app.debug = True
    # app.run(host='0.0.0.0',port=8080)
