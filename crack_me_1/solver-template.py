from pwn import *

context.log_level = "debug"
io = remote("fallctf.cybr.club", 443, ssl=True, sni="crackme1")
io.interactive(prompt="")
