import http.server
import re
import os
import hashlib
from node_mcu_update_server import update_manager

class NodeMCUUpdateServer(http.server.SimpleHTTPRequestHandler):
    def calculate_md5_sum(self, file_path):
        file_bytes = self.file_as_bytes(file_path)
        return hashlib.md5(file_bytes).hexdigest()

    def file_as_bytes(self, file):
        with open(file, "rb") as file_handle:
            return file_handle.read()

    def send_update_file_to_client(self, path_to_update):
        print("sending update file to device: " + path_to_update)
        file_name = os.path.basename(path_to_update)
        file_size = os.stat(path_to_update).st_size
        update_md5 = self.calculate_md5_sum(path_to_update)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition",
                         "attachment; filename=" + file_name)
        self.send_header("Content-Length", file_size)
        self.send_header("x-MD5", update_md5)
        self.send_response(200)
        self.end_headers()

        self.wfile.write(self.file_as_bytes(path_to_update))

    def is_valid_update_request(self):
        if self.headers["User-Agent"] == "ESP8266-http-Update" and \
           self.headers["x-ESP8266-STA-MAC"] and \
           self.headers["x-ESP8266-AP-MAC"] and \
           self.headers["x-ESP8266-free-space"] and \
           self.headers["x-ESP8266-sketch-size"] and \
           self.headers["x-ESP8266-version"] and \
           self.headers["x-ESP8266-chip-size"] and \
           self.headers["x-ESP8266-sdk-version"] and \
           self.headers["x-ESP8266-sketch-md5"]:
           return update_manager.device_version_string_is_valid(self.headers["x-ESP8266-version"])
        return False

    def do_GET(self):
        print("Received " + self.command + " from client address:" + str(self.client_address))
        print("with headers: ")
        print(self.headers)
        if self.is_valid_update_request():
            device_version = self.headers["x-ESP8266-version"]
            if update_manager.update_exists(device_version):
                path_to_update = update_manager.get_next_update_path(device_version)
                self.send_update_file_to_client(path_to_update)
            else:
                self.send_response(304)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
