import os
import time
import datetime
import signal
import sys
import unicornhat as unicorn
import threading

from jinja2 import Environment, FileSystemLoader
from monitor import checks,status,lightshow

STATUS = "/var/www/html/index.html"
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def run_checks(status):
    # status.flush()

    dns_net = checks.Check('Name Based Internet',checks.check_dns_net())
    status.add(dns_net)
    if not dns_net.status:
        ip_net = checks.Check('IP Based Internet',checks.check_general_net())
        dns_net.add_child(ip_net)
        if not ip_net.status:
            modem = checks.Check('Gateway',checks.check_host_port("192.168.1.254", 80))
            ip_net.add_child(modem)
    
    dns = checks.Check('Loki DNS', checks.check_host_port("192.168.1.2", 53))
    status.add(dns)
    loki_web = checks.Check('Loki Web Server', checks.check_host_port('loki', 80))
    status.add(loki_web)
    if not (dns.status and loki_web.status):
        loki = checks.Check('Loki', checks.check_host_via_ssh("192.168.1.2"))
        loki_web.add_child(loki)
    
    ap_two = checks.Check('Asgard_Too Wifi', checks.check_host_port("192.168.1.253", 80))
    status.add(ap_two)
    
    techworld = checks.Check('Apollo TechWorld Server', checks.check_host_port("apollo", 64004))
    status.add(techworld)
    if not techworld.status:
        cassini = checks.Check('Apollo', checks.check_host_port("apollo", 111))
        techworld.add_child(cassini)
    
    freya_web = checks.Check('Freya Web Server', checks.check_host_port('freya', 80))
    status.add(freya_web)
    if not freya_web.status:
        freya = checks.Check('Freya', checks.check_host_via_ssh("freya"))
        freya_web.add_child(freya)

def update_webfile():
    health_status = status.Status()

    run_checks(health_status)
    output_list = []
    tstamp = datetime.datetime.now()
    for check in health_status.checks:
        # Here I'll need to read the children to control the LED
        flatcheck = check.flatten()
        for c in flatcheck:
            output_list.append(c.to_dict())
    lightshow.set_lights(health_status)
    with open(STATUS, 'w') as output:
        output.write(j2_env.get_template('template.html').render(last_check = tstamp,
            content=output_list))

if __name__ == "__main__":
    unicorn.rotation(90)
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)

    counter = 0
    tracer = 0
    interval = 30
    tick = 0.5

    while True:
        try:
            lightshow.tracer_row(0, tracer%8)
            if counter == 0:
                t = threading.Thread(target=update_webfile)
                t.start()
            time.sleep(tick)
        except KeyboardInterrupt:
            break
        counter = (counter+1) % int(interval/tick)
        tracer = (tracer+1) % 8
    unicorn.off()
