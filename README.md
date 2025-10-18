# R3SPWN
💀 R3SPWN : Critical Vulnerability Auditor
🎯 Overview
R3SPWN (TResponse pwned) is a fast, multi-threaded command-line utility designed for auditing web applications for two critical security flaws: Host Header Injection and CORS Misconfiguration.

Unlike other tools that rely on separate modes, TRUSTR3S uses a single comprehensive wordlist of header names (Host, X-Forwarded-Host, Origin, etc.) to efficiently check all targets. It injects a payload into each header and scans the response body for reflection, indicating a potential vulnerability.

✨ Features
⚡ Multi-Threaded: Optimized for speed, enabling concurrent scanning of multiple targets and payloads.

🧩 Dual-Mode Wordlist: Uses a single wordlist.txt to test both Host Header Injection and CORS Misconfiguration.

Host Header Scan: Tests headers like X-Host for reflection.

CORS Scan: Tests the Origin header for reflection of the payload in the response body.

💾 Robust Output: Saves detailed, color-stripped results to a specified file.

🧑‍💻 Clean Interface: Features a unique, powerful ASCII banner and professional output.

[![GIF](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZTN3YTBoN254djNxdGl1emZyMDYzMnVrM2VxYjZ3OHR3MGI1dzdkaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5XPb0FvIqylqg/giphy.gif)

## 📦 Installation  

```bash
# Clone the repository
https://github.com/MASTERMONTYOFFICIAL/R3SPWN.git
cd R3SPWN
main.py

# Install dependencies
pip3 install requests

# Scan a single URL
python main.py -d https://example.com -o output.txt

# Scan using list of urls
python main.py -uL live_urls.txt -r evil.com -o output.txt

```

👤 Author & Connect
<div align="center"> <h3>Zeropwned</h3> <a href="https://github.com/MASTERMONTYOFFICIAL"> <img src="https://img.shields.io/badge/GitHub-MASTERMONTYOFFICIAL-100000?style=for-the-badge&logo=github" alt="GitHub Badge"/> </a> <a href="https://www.linkedin.com/in/durgeshwer-singh-01b43a377?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app"> <img src="https://img.shields.io/badge/LinkedIn-Durgeshwer_Singh-0077B5?style=for-the-badge&logo=linkedin" alt="LinkedIn Badge"/> </a> </div>
