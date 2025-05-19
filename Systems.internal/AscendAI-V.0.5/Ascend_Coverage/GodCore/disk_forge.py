import os
import subprocess

VIRTUAL_DISK_PATH = "/mnt/data/ascend.vdisk"
MOUNT_POINT = "/mnt/ascend_disk"


def create_virtual_disk():
    try:
        # Create a 512GB sparse file (won't allocate all space upfront)
        if not os.path.exists(VIRTUAL_DISK_PATH):
            subprocess.run(["fallocate", "-l", "512G", VIRTUAL_DISK_PATH], check=True)
            subprocess.run(["mkfs.ext4", VIRTUAL_DISK_PATH], check=True)
            os.makedirs(MOUNT_POINT, exist_ok=True)
            subprocess.run(["mount", VIRTUAL_DISK_PATH, MOUNT_POINT], check=True)
            print(f"Disk created and mounted at {MOUNT_POINT}")
        else:
            print("Virtual disk already exists.")
    except Exception as e:
        print(f"[ERROR] Failed to create/mount virtual disk: {e}")


if __name__ == "__main__":
    create_virtual_disk()
