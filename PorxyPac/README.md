## Setup Windows Proxy

1. Use **Internet Options** → **Links** → **LAN Option** → Use `http://127.0.0.1:1089/pac` as URL
2. Set Proxy Agent HTTP port to :1088, this is written in PAC file.
3. Tell Proxy Agent do NOT change the system proxy settings.

## Setup Caddy Server

1. `scoop install caddy` to install Caddy2 CLI
2. In this folder (where PAC file exists) `caddy run` and then visit http://127.0.0.1:1089/pac/ in browser to check if this is ok.
3. `caddy start` to launch a daemon caddy server
