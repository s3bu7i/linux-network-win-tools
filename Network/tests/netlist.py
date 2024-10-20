from ipaddress import IPv4Network

exemp_ips = ["127.0.0.1","10.0.0.0/16"]
fake_db_allowed_ips = ["42.42.42.42","1.2.3.4"]

def allow_ip_address(ipaddress):
    if always_allow_ip_address(ipaddress) or ipaddress in fake_db_allowed_ips:
        return True
    return False

def always_allow_ip_address(ipaddress):
    for exemp_ip in exemp_ips:
        all_ips = [str(ip) for ip in IPv4Network(exemp_ip) ]

        if ipaddress in all_ips:
            return True
        return False