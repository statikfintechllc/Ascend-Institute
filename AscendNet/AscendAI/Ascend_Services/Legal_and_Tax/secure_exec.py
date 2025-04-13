import subprocess
import gnupg
import os

GPG_HOME = os.getenv("ASCEND_GPG_HOME", "/root/.gnupg")
AUTHORIZED_KEY = "394504B2D849D4A377036EBDB8B556DE69147BAA"
gpg = gnupg.GPG(gnupghome=GPG_HOME)

def secure_exec(command, signature, signed_message):
    # Verify signature
    verify = gpg.verify_data(signature, signed_message.encode())
    if verify and verify.fingerprint == AUTHORIZED_KEY_FINGERPRINT:
        print("[SECURE_EXEC] Valid CEO Signature. Executing command...")
        subprocess.run(command, shell=True)
    else:
        print("[SECURE_EXEC] Invalid signature. Execution blocked.")
        raise PermissionError("Unauthorized command attempt.")

# Example usage:
# secure_exec("python agent_launcher.py", "signed.sig", "Deploy agent to cluster")
