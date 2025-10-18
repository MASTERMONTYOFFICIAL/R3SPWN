import requests
import argparse
import threading
import random
import sys
import time

# Define colors
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
GRAY = "\033[0;37m"
RESET = "\033[0m"


USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
        ]

agent = random.choice(USER_AGENTS)

def save_output(result, output_file):
    clean_result = result.replace(GREEN, "").replace(RED, "").replace(RESET, "")
    with open(output_file, 'a') as f:
        f.write(clean_result + "\n")

def findvuln(domain, payload, redirect, output):
    try:
        header_name = payload.strip()
        headers = {
            "User-Agent": agent,
            header_name: redirect  
        }
        
        target_url = domain.strip()

        res = requests.get(target_url, headers=headers, timeout=8, allow_redirects=False) 
        

        if redirect in res.text and res.status_code == 200 or res.status_code == 302 or res.status_code == 301 :
            result = (
                f"\n{GREEN}VULNERABLE:{RESET} {domain}\n"
                f"{GREEN}HEADER:{RESET} {header_name}\n"
                f"{GREEN}PAYLOAD : {RESET} {redirect}\n"
                f"{GREEN}STATUS:{RESET} {res.status_code}\n"
            )
            if header_name == "cors":
                filter_result = (
                f"\n{GRAY}---FOUND CORS MISCONFIGURATION---{RESET}"
                f"{result}"
                )
            else:
                filter_result = (
                f"\n---FOUND HOST-HEADER INJECTION---\n"
                f"{result}"
            )
            print(filter_result)
            save_output(result, output)
        else:
            print(f"NOT VULNERABLE: {domain}\n{header_name}:{redirect}\n")

    except requests.RequestException :
        print(f"NOT FETCH : {domain}")


          
def banner():
    RED = "\033[0;31m"
    GRAY = "\033[0;37m"
    RESET = "\033[0m"

    print(f"\n{RED}")
    print(r"""
    $$$$$$$\   $$$$$$\   $$$$$$\  $$$$$$$\  $$\      $$\ $$\   $$\ 
    $$  __$$\ $$ ___$$\ $$  __$$\ $$  __$$\ $$ | $\  $$ |$$$\  $$ |
    $$ |  $$ |\_/   $$ |$$ /  \__|$$ |  $$ |$$ |$$$\ $$ |$$$$\ $$ |
    $$$$$$$  |  $$$$$ / \$$$$$$\  $$$$$$$  |$$ $$ $$\$$ |$$ $$\$$ |
    $$  __$$<   \___$$\  \____$$\ $$  ____/ $$$$  _$$$$ |$$ \$$$$ |
    $$ |  $$ |$$\   $$ |$$\   $$ |$$ |      $$$  / \$$$ |$$ |\$$$ |
    $$ |  $$ |\$$$$$$  |\$$$$$$  |$$ |      $$  /   \$$ |$$ | \$$ |
    \__|  \__| \______/  \______/ \__|      \__/     \__|\__|  \__| 

    [Automation script for host header injection and cors misconfiguration]                                              
    """)
    print(f"{RESET}")
    
    BOX_WIDTH = 48
    
    author_line = f"{GRAY}Author:{RESET} Zeropwned"
    linkedin_line = f"{GRAY}LinkedIn:{RESET} Durgeshwer Singh"
    
    print(" " * 6 + f"{RED}╔" + "═" * BOX_WIDTH + f"╗{RESET}")
    print(" " * 6 + f"{RED}║{RESET}" + author_line.ljust(BOX_WIDTH + len(GRAY) + len(RESET) - 13) + f"{RED}║{RESET}")
    print(" " * 6 + f"{RED}║" + "─" * BOX_WIDTH + f"║{RESET}")
    print(" " * 6 + f"{RED}║{RESET}" + linkedin_line.ljust(BOX_WIDTH + len(GRAY) + len(RESET) - 13) + f"{RED}║{RESET}")
    print(" " * 6 + f"{RED}╚" + "═" * BOX_WIDTH + f"╝{RESET}")
    print("\n")


def main():
    try:
        banner()
        
        parser = argparse.ArgumentParser(prog="responsepwn",
                                        description="Powerful simple script for host-header injection and cors misconfiguration.")
        parser.add_argument("-d", "--domain", help="Finding Vulnerability in single target.")
        parser.add_argument("-uL", "--list", help="List of urls to hunt.")
        parser.add_argument("-r", "--redirect", default="evil.com", 
                            help="For Redirecting host (default: evil.com).")
        parser.add_argument("-o", "--output", default="results.txt", 
                            help="Save results in a file (default: results.txt).")

        args = parser.parse_args()

        if not args.list and not args.domain:
            print(f"{RED}Error: You must specify a single domain (-d) or a list of domains (-dL).{RESET}")
            parser.print_help()
            return

        wordlist_path = "wordlist.txt"
        try:
            with open(wordlist_path, 'r') as f:
                payloads = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"{RED}Error: wordlist file '{wordlist_path}'.{RESET}")
            return

        if not payloads:
            print(f"{RED}Error: wordlist is empty. Please check '{wordlist_path}'.{RESET}")
            return
            
        if not args.redirect:
            args.redirect = "evil.com"

        targets = []
        if args.domain:
            targets.append(args.domain)
        if args.list:
            try:
                with open(args.list, 'r') as f:
                    targets.extend([line.strip() for line in f if line.strip()])
            except FileNotFoundError:
                print(f"{RED}Error: Domain list file '{args.list}' not found!{RESET}")
                return
        
        threads = []
        print(f"\n{GREEN}Starting scan on {len(targets)} targets with {len(payloads)} headers ...{RESET}\n")
        time.sleep(1)
        print(f'{BLUE}"""Checks for Host and Origin using common headers."""{RESET}')
        
        for target in targets:
            for payload in payloads:
                t = threading.Thread(target=findvuln, 
                                     args=(target, payload, args.redirect, args.output))
                threads.append(t)
                t.start()
        
        for t in threads:
            t.join()
        
        print(f"\n{GREEN}Scan finished. Results saved to {args.output}{RESET}")

    except KeyboardInterrupt:
        print(f"\n{RED}Bye Bye .... (Scan Interrupted){RESET}")
        sys.exit(0)

if __name__ == '__main__':
    main()