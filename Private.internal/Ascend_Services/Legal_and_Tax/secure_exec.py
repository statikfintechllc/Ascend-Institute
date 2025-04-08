import subprocess
import gnupg
import os

GPG_HOME = os.getenv("ASCEND_GPG_HOME", "/root/.gnupg")
AUTHORIZED_KEY = "394504B2D849D4A377036EBDB8B556DE69147BAA"
gpg = gnupg.GPG(gnupghome=GPG_HOME)

def secure_exec(command, signature_path, signed_text):
    with open(signature_path, "rb") as sig:
        verified = gpg.verify_data(sig, signed_text.encode())

    if verified and verified.fingerprint == AUTHORIZED_KEY:
        subprocess.run(command, shell=True)
        return True
    else:
        raise PermissionError("Signature validation failed.")
