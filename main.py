# main.py
# DISCLAIMER: This script is for educational purposes only. Do not use against any system without explicit permission.
from urllib.parse import urlparse

def main():
    # ... existing code ...
    domain = args.domain

    # Sanitize domain input
    parsed = urlparse(domain)
    if parsed.scheme:
        domain = parsed.netloc
    else:
        domain = domain.strip().strip('/')

    # ... rest of your code ...

import argparse
from scanner import find_subdomains, scan_ports, find_directories
from utils import print_banner, print_results, save_results

def main():
    """
    Main function to parse arguments and orchestrate the scanning process.
    """
    print_banner()
    
    parser = argparse.ArgumentParser(description="Recon-Scanner: An educational VAPT tool.")
    
    # Required arguments
    parser.add_argument("-d", "--domain", required=True, help="The target domain to scan.")
    
    # Feature flags
    parser.add_argument("--subdomains", action="store_true", help="Enable subdomain enumeration.")
    parser.add_argument("--ports", action="store_true", help="Enable port scanning on found subdomains.")
    parser.add_argument("--dirsearch", action="store_true", help="Enable directory brute-forcing.")
    
    # Options
    parser.add_argument("-w", "--wordlist", help="Path to a wordlist for subdomain or directory search.")
    parser.add_argument("-o", "--output", help="Save the results to a file.")

    args = parser.parse_args()

    domain = args.domain
    wordlist = args.wordlist
    output_file = args.output
    
    all_results = {}

    print(f"[*] Starting scan on: {domain}\n")

    if args.subdomains:
        if not wordlist:
            print("[!] Error: Subdomain enumeration requires a wordlist specified with -w/--wordlist.")
            return
        
        print("[*] Starting subdomain enumeration...")
        found_subdomains = find_subdomains(domain, wordlist)
        all_results["subdomains"] = found_subdomains
        print_results("Subdomains", found_subdomains)

        if args.ports and found_subdomains:
            print("[*] Starting port scanning on discovered subdomains...")
            # Note: For a real tool, you'd scan all subdomains. 
            # For this example, we'll scan the first few to keep it quick.
            ports_results = {}
            for sub in found_subdomains[:5]: # Limiting to 5 for demonstration
                print(f"    -> Scanning ports for {sub}...")
                # Scanning top 20 common ports for demonstration
                common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
                open_ports = scan_ports(sub, common_ports)
                if open_ports:
                    ports_results[sub] = open_ports
            all_results["open_ports"] = ports_results
            print_results("Open Ports", ports_results)

    if args.dirsearch:
        if not wordlist:
            print("[!] Error: Directory searching requires a wordlist specified with -w/--wordlist.")
            return
        
        # Check if port 80 or 443 is open on the base domain before searching
        print(f"[*] Starting directory search on http://{domain}...")
        found_dirs = find_directories(f"http://{domain}", wordlist)
        all_results["directories"] = found_dirs
        print_results("Found Directories/Files", found_dirs)

    if output_file:
        print(f"\n[*] Saving results to {output_file}...")
        save_results(output_file, all_results)
        print("[+] Results saved.")

if __name__ == "__main__":
    main()

