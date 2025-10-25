from pwn import *

io = remote("fallctf.cybr.club", 443, ssl=True, sni="jumper")
io.interactive(prompt="")