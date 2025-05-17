#!/bin/bash
DISK=/dev/sdc
echo "[FORMAT] Formatting and labeling GodCore partitions..."

mkfs.vfat -F32 -n GRUB_BOOT ${DISK}1
mkfs.ext4 -L UBU_SRV ${DISK}2
mkfs.ext4 -L UBU_GUI ${DISK}3
mkfs.ext4 -L EXTENSION ${DISK}5
mkfs.ext4 -L GODCORE ${DISK}6
