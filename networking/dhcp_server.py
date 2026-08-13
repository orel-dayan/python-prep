import argparse
import ipaddress
import time
from collections import OrderedDict

from scapy.all import Ether, IP, UDP, BOOTP, DHCP, sendp, sniff