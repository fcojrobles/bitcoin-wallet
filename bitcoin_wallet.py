import base58, ecdsa, hashlib, os

private_key = os.urandom(32)
print(f"Private Key: {private_key.hex()}")

sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
vk = sk.get_verifying_key()
public_key = b"\x04" + vk.to_string()  # Adding 0x04 byte to signify uncompressed public key
print(f"Public Key: {public_key.hex()}")

# Step 1: SHA-256 Hash of Public Key
sha256_hash = hashlib.sha256(public_key).digest()
 
# Step 2: RIPEMD-160 Hash of SHA-256
ripemd160 = hashlib.new('ripemd160', sha256_hash).digest()
 
# Step 3: Adding Network Byte (0x00 for Bitcoin)
network_byte = b'\x00' + ripemd160
 
# Step 4: Creating a Checksum by Double Hashing
checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
 
# Step 5: Adding Checksum to the Versioned RIPEMD-160 Hash
address = base58.b58encode(network_byte + checksum)
print(f"Wallet Address: {address.decode()}")
