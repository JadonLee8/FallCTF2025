from pwn import *

io = remote("fallctf.cybr.club", 443, ssl=True, sni="sanity-check-too")
# read the pwntools docs to see how remote works :)
io.interactive(prompt="")
