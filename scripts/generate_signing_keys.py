import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

def main():
    secrets_dir = r"c:\dev\projetos\datagrip\plugin\secrets"
    os.makedirs(secrets_dir, exist_ok=True)
    
    private_key_path = os.path.join(secrets_dir, "private-key.pem")
    cert_path = os.path.join(secrets_dir, "certificate-chain.crt")
    password_path = os.path.join(secrets_dir, "password.txt")
    
    password = b""
    
    # 1. Generate Private Key
    print("Generating RSA Private Key...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # 2. Serialize Private Key without encryption
    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    with open(private_key_path, "wb") as f:
        f.write(pem_private_key)
    print(f"Private key saved to {private_key_path}")
    
    # 3. Generate Self-Signed Certificate
    print("Generating Self-Signed Certificate...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "BR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "SP"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Sao Paulo"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Comunidade DataGrip Brasil"),
        x509.NameAttribute(NameOID.COMMON_NAME, "DataGrip Portuguese Pack"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    ).not_valid_after(
        # Valid for 10 years
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=3650)
    ).add_extension(
        x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()),
        critical=False
    ).sign(private_key, hashes.SHA256())
    
    # 4. Serialize Certificate
    pem_cert = cert.public_bytes(serialization.Encoding.PEM)
    with open(cert_path, "wb") as f:
        f.write(pem_cert)
    print(f"Certificate saved to {cert_path}")
    
    # 5. Save password
    with open(password_path, "w", encoding="utf-8") as f:
        f.write(password.decode("utf-8"))
    print(f"Password saved to {password_path}")

if __name__ == "__main__":
    main()
