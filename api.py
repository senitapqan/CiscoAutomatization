import telnetlib
import time
import re

import pandas as pd


class Switch:
    def __init__(self):
        self.correct_answers = {}
        self.cursor = None
        self.host = ""
        self.username = ""
        self.password = ""
        self.enable = ""

    def connect_to_switch(self, host, username, password, enable):
        self.host = host
        self.username = username
        self.enable = enable
        self.password = password
        try:
            self.cursor = telnetlib.Telnet(host)
            self.cursor.read_until(b"Username:")
            self.cursor.write(username.encode('ascii') + b"\n")

            self.cursor.read_until(b"Password:")
            self.cursor.write(password.encode('ascii') + b"\n")

            time.sleep(1)
            return [host, self]
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return None

    def check_ip_configuration(self, result):
        interface_pattern = re.compile(r'interface (\S+)[\s\S]+?ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)')
        matches = interface_pattern.finditer(result)
        lst = list()

        for match in matches:
            interface, ip, subnet_mask = match.groups()
            dct = {"Interface": interface, "IP": ip, "Subnet Mask": subnet_mask}
            lst.append(dct)

        return lst

    def check_routing(self, result):
        route_pattern = re.compile(r'ip route (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)')
        matches = route_pattern.finditer(result)
        lst = list()

        for match in matches:
            destination, next_hop = match.groups()
            dct = {"Destination": destination, "Next Hop" :  next_hop}
            lst.append(dct)

        return lst

    def check_vlan(self, result):
        vlan_pattern = re.compile(r'interface Vlan(\d+)[\s\S]+?ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)')
        matches = vlan_pattern.finditer(result)
        lst = list()

        for match in matches:
            vlan_id, ip, subnet_mask = match.groups()
            dct = {"VLAN ID" : vlan_id, "IP": ip, "Subnet Mask" : subnet_mask}
            lst.append(dct)

        return lst

    def get_parse(self):
        self.cursor.read_until(b">")
        self.cursor.write(b"enable\n")
        self.cursor.read_until(b"Password: ")
        self.cursor.write(self.enable.encode('ascii') + b"\n")
        self.cursor.read_until(b"#")

        command = "show run"
        self.cursor.write(command.encode("ascii") + b"\n")
        time.sleep(2)
        result = self.cursor.read_very_eager().decode('ascii')

        pattern = re.compile(r'\bhostname\b\s+(\S+)')
        match = pattern.search(result)

        hostname = match.group(1)

        while "--More--" in result:
            result = result.replace("--More--", "")
            result += "\n"
            self.cursor.write(b" ")
            time.sleep(0.5)
            cur = self.cursor.read_very_eager().decode('ascii')
            result += "\n" + cur

        print(result)
        self.cursor.write(b"disable\n")

        return result, hostname

    def perform_checks(self, category):
        result, hostname = self.get_parse()

        if category == "IP":
            result = self.check_ip_configuration(result)
        elif category == "Routing":
            result = self.check_routing(result)
        elif category == "VLAN":
            result = self.check_vlan(result)

        return result, hostname
