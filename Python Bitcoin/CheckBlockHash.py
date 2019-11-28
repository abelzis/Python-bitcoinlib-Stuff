from bitcoin.rpc import RawProxy
import hashlib
import sys
import struct


p = RawProxy()

# handle command line arguments
if (len(sys.argv) > 1):
    if (sys.argv[1].lower() == "hash"):
        block = p.getblock(sys.argv[2])
    else:
        block = p.getblock(p.getblockhash(int(sys.argv[1])))
else:
    block = p.getblock(p.getbestblockhash())

# convert int to little endian hex
def convert_int_endian(num):
    num = struct.pack("<I", num).encode('hex')
    return num

# convert string to little endian hex
def convert_str_endian(hex):
    bin = hex.decode('hex')
    hex = bin[::-1].encode('hex_codec')
    return hex

# concatenate block info as string
header_hex = str(convert_str_endian(block['versionHex']) +
              convert_str_endian(block['previousblockhash']) +
              convert_str_endian(block['merkleroot']) +
              str(convert_int_endian(block['time'])) +
              convert_str_endian(str(block['bits'])) + 
              str(convert_int_endian(block['nonce'])))

header_bin = header_hex.decode('hex')   # convert to hex
hash = hashlib.sha256(hashlib.sha256(header_bin).digest()).digest() # hash
hash = hash[::-1].encode('hex_codec')   # convert to string

print("Hash in block: \t\t" + block['hash'])
print("Hash calculated: \t" + hash)

if (block['hash'] == hash):
    print("\nHash is CORRECT.")
else:
    print("\nHash is INCORRECT.")