# This class should control the output of checks and trigger different light modes.

import monitor.checker

def print_result(text, value):
    if value:
        print text + " is up"
    else:
        print text + " is down"

dns_net = monitor.checker.check_dns_net()
if dns_net:
    print_result("dns net", dns_net)
else:
    print_result("net", monitor.checker.check_general_net())
    print_result("modem", monitor.checker.check_host_port("192.168.1.254", 80))
print_result("local DNS", monitor.checker.check_host_port("192.168.1.2", 53))
print_result("loki", monitor.checker.check_host_via_ssh("192.168.1.2"))
print_result("cassini", monitor.checker.check_host_via_ssh("192.168.1.252"))
print_result("asgard_too", monitor.checker.check_host_port("192.168.1.253", 80))
print_result("techworld", monitor.checker.check_host_port("192.168.1.252", 64004))
print_result("loki web port", monitor.checker.check_host_port('192.168.1.2', 80))
print_result("freya", monitor.checker.check_host_via_ssh("192.168.1.20"))
print_result("freya web port", monitor.checker.check_host_port('192.168.1.20', 80))

# These should be in priority order: if net is down,
