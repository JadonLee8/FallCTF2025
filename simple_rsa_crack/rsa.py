from Crypto.Util.number import bytes_to_long, long_to_bytes

n = 22048729724951726101
e = 65537
def encrypt(plaintext: bytes) -> bytes:
  ciphertext = b''
  blocksize = n.bit_length() // 8
  for i in range(0, len(plaintext), blocksize):
    block = bytes_to_long(plaintext[i: i + blocksize])
    ciphertext += long_to_bytes(pow(block, e, n))

  return ciphertext

p = 3473904977
q = 6346958213
def decrypt(ciphertext: bytes) -> bytes:
  # Calculate the private key exponent d
  phi = (p - 1) * (q - 1)
  d = pow(e, -1, phi)

  blocksize = n.bit_length() // 8
  plaintext = b''
  for i in range(0, len(ciphertext), blocksize):
    block = bytes_to_long(ciphertext[i: i + blocksize])
    decrypted_block = pow(block, d, n)
    plaintext += long_to_bytes(decrypted_block)

  return plaintext

# Encrypted message
ciphertext = b'P\x8dX\xe9\x1a\xbd\nrG3\x85\xf6\xf9\xe2Vi\xd6\xb4\x98M\xb2L\xfd3'

def main():
  decrypted_message = decrypt(ciphertext)
  print("Decrypted message:", decrypted_message)

if __name__ == "__main__":
  main()