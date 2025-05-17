#!/bin/bash
DISK=/dev/sdc
echo "[MOUNT] Mounting GodCore partitions..."

mkdir -p /mnt/efi /mnt/ubu_srv /mnt/ubu_gui /mnt/extboot /mnt/godcore

mount ${DISK}1 /mnt/efi
mount ${DISK}2 /mnt/ubu_srv
mount ${DISK}3 /mnt/ubu_gui
mount ${DISK}5 /mnt/extboot
mount ${DISK}6 /mnt/godcore

# Build GodCore structure
cd /mnt/godcore
mkdir -p boot emulate coldcode neuro identity shield logs dreams compression storage mutation_engine biocontrol temporal wifi spawn selfforge
