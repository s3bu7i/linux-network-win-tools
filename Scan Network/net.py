from ipaddress import ip_address
from ipaddress import ip_network

exempt_ips = ["127.0.0.1","10.0.0.0/16"]
fake_db_allowed_ips = ["42.42.42.42","1.2.3.4"]

def allow_ip_address(ipaddress):
    if always_allow_ip_address(ipaddress) or ipaddress in fake_db_allowed_ips:
        return True
    return False

def always_allow_ip_address(ipaddress):
    for i in exempt_ips:
        if ip_address(ipaddress) in ip_network(ip):
            return True
        return False

