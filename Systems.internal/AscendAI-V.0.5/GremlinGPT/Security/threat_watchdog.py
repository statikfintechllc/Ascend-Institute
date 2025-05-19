# threat_watchdog.py

import scapy.all as scapy
import logging

logger = logging.getLogger(__name__)


def packet_callback(packet):
    if packet.haslayer(scapy.IP):
        ip_layer = packet.getlayer(scapy.IP)
        logger.info(f"New Packet: {ip_layer.src} -> {ip_layer.dst}")


def start_sniffing():
    scapy.sniff(prn=packet_callback, store=0)
