import re
import logging

class SpeedTestParser(object):

    def parse(self):
        lines = self.text.split('\n')
        for i, line in enumerate(lines):
            if i == 2:
                self.extract_local_information(line)
            elif i == 3:
                self.extract_server_information(line)
            elif i == 5:
                self.extract_download(line)
            elif i == 7:
                self.extract_upload(line)
            elif i == 8:
                self.extract_share_url(line)

    def __init__(self, text):
        self.my_server_name = None
        self.my_server_domain = None
        self.my_ip = None

        self.server_name = None
        self.server_location = None
        self.server_distance = None
        self.server_distance_unit = None
        self.server_ping = None
        self.server_ping_unit = None

        self.download_speed = None
        self.download_unit = None

        self.upload_speed = None
        self.upload_unit = None

        self.share_url = None

        self.text = str(text).replace("Selecting best server based on latency...\n", "")

        self.parse()

    def extract_local_information(self, line):
        logging.debug("Extract local information --- %s" % line)
        regex = r"Testing from ([\w /-_]+) \(([\w\.]+)\) \(([0-9\.]+)\)"
        match = re.search(regex, line)
        if match:
            self.my_server_name = match.group(1)
            self.my_server_domain = match.group(2)
            self.my_ip = match.group(3)

    def extract_server_information(self, line):
        logging.debug("Extract server information --- %s" % line)
        regex = r"Hosted by (.+) \(([\w ]+)\) \[([[0-9\.]+) ([A-Za-z]+)\]: ([0-9\.]+) ([A-Za-z]+)"
        match = re.search(regex, line)
        if match:
            self.server_name = match.group(1)
            self.server_location = match.group(2)
            self.server_distance = match.group(3)
            self.server_distance_unit = match.group(4)
            self.server_ping = match.group(5)
            self.server_ping_unit = match.group(6)

    @staticmethod
    def extract_speed(prefix, line):
        logging.debug("Extract %s speed information --- %s" % (prefix, line))
        regex = r"" + prefix + ": ([0-9\.]+) ([A-Za-z/]+)"
        match = re.search(regex, line)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def extract_download(self, line):
        self.download_speed, self.download_unit = self.extract_speed("Download", line)

    def extract_upload(self, line):
        self.upload_speed, self.upload_unit = self.extract_speed("Upload", line)

    def extract_share_url(self, line):
        regex = r"Share results: (.*)"
        match = re.search(regex, line)
        if match:
            self.share_url = match.group(1)

    def __str__(self):
        string = "Local information: %s (%s) (%s)\n" % (self.my_server_name, self.my_server_domain, self.my_ip)
        string += "Server information: %s (%s) [%s %s]: %s %s \n" % (self.server_name, self.server_location,
                                                                  self.server_distance, self.server_distance_unit,
                                                                  self.server_ping, self.server_ping_unit)
        string += "Download information: %s %s\n" % (self.download_speed, self.download_unit)
        string += "Upload information: %s %s" % (self.upload_speed, self.upload_unit)
        string += "Share url: %s" % self.share_url
        return string