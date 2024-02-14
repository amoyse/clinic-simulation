from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generate an RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Get the corresponding public key
public_key = private_key.public_key()

# Serialize private key to save it securely
pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(b'password')
)

# Save the private key to a file
with open('medrecords_private.pem', 'wb') as f:
    f.write(pem)

# Serialize public key to distribute it
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Save the public key to a file or distribute it to clients
with open('medrecords_public.pem', 'wb') as f:
    f.write(pem)
