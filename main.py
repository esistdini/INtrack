import argparse
import random
import socket
import urllib3
import concurrent.futures
from alive_progress import alive_bar
from lib.wordpress_scanner import check_wordpress
from lib.gargoyle_scanner import check_gargoyle
from lib.gpon_scanner import check_gpon
from lib.webcamxp_scanner import check_webcamxp
from lib.vscode_sftp_worm import crawl_vscode_sftp

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def generate_ip():
    return f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

def check_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        try:
            s.connect((ip, port))
            return True
        except (socket.timeout, socket.error):
            return False

def process_ip(ip, args):
    if args.worm:
        if args.worm == 'vscode-sftp':
            crawl_vscode_sftp(ip, args.p)
            return ip

    if args.instance:
        if args.instance == 'wordpress' and check_wordpress(ip, args.p):
            return ip
        elif args.instance == 'gargoyle' and check_gargoyle(ip, args.p):
            return ip
        elif args.instance == 'gpon' and check_gpon(ip, args.p):
            return ip
        elif args.instance == 'webcamxp' and check_webcamxp(ip, args.p):
            return ip
    else:
        if check_port(ip, args.p):
            return ip
    return None

def main():
    parser = argparse.ArgumentParser(description="Generate IP addresses and check for open ports or specific instances.")
    parser.add_argument("-n", type=int, required=True, help="Number of targets to find.")
    parser.add_argument("-p", type=int, default=None, help="Port to check.")
    parser.add_argument("-t", type=int, default=1, help="Number of threads to use.")
    parser.add_argument("-instance", type=str, help="Type of instance to check (e.g., 'wordpress', 'gargoyle', 'gpon').")
    parser.add_argument("-worm", type=str, help="Enable special script execution with a specified type (e.g., 'vscode-sftp').")

    args = parser.parse_args()

    found_targets = []

    with alive_bar(None, title="[Scanning Internet]", enrich_print=False) as instance_bar:
        while len(found_targets) < args.n:
            ip_addresses = [generate_ip() for _ in range(args.t * 10)]
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.t) as executor:
                results = list(executor.map(lambda ip: process_ip(ip, args), ip_addresses))
            found_targets.extend(filter(None, results))
            instance_bar(len(ip_addresses))
    print(f"\n[*] Total targets found: {len(found_targets)}")
    for targ in found_targets[:args.n]:
        print(targ)

if __name__ == "__main__":
    main()