import os
import time
import datetime
import signal
import sys

from jinja2 import Environment, FileSystemLoader
from monitor import checks,status

STATUS = "/var/www/html/index.html"
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

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
    loki_web = checks.Check('Loki Web Server', checks.check_host_port('loki', 80))
    status.add(loki_web)
    
    ap_two = checks.Check('Asgard_Too Wifi', checks.check_host_port("192.168.1.253", 80))
    status.add(ap_two)
    
    cassini = checks.Check('Apollo', checks.check_host_via_ssh("apollo"))
    status.add(cassini)
    techworld = checks.Check('TechWorld Server', checks.check_host_port("apollo", 64004))
    status.add(techworld)
    
    freya = checks.Check('Freya', checks.check_host_via_ssh("freya"))
    status.add(freya)
    freya_web = checks.Check('Freya Web Server', checks.check_host_port('freya', 80))
    status.add(freya_web)


if __name__ == "__main__":
    health_status = status.Status()

    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    while True:
        try:
            run_checks(health_status)
            output_list = []
            # ostring = "%s\n" % datetime.datetime.now()
            tstamp = datetime.datetime.now()
            for check in health_status:
                output_list.append({'name': check.name, 'status': check.status})
            with open(STATUS, 'w') as output:
                output.write(j2_env.get_template('template.html').render(last_check = tstamp,
                    content=output_list))
            time.sleep(30)
        except KeyboardInterrupt:
            break
