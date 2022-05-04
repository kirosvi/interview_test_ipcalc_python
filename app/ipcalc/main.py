#!/usr/bin/env python3
#-*- coding:UTF-8 -*-

import sys
import ipaddress
import jinja2
from http.server import HTTPServer, BaseHTTPRequestHandler

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        content = message
        return content.encode("utf8")

    def do_GET(self):
        self._set_headers()
        response = create_response_data(data="", file="default_template.j2")
        self.wfile.write(self._html(response))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len).decode('UTF-8')
        response = get_net_info(post_body)
        self.wfile.write(self._html(response))

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

def cal_ip(ip_net):
    ip_net_data = {}
    try:
        net = ipaddress.ip_network(ip_net, strict=False)
        ip_net_data["net_version"] = str(net.version)
        ip_net_data["private_address"] = str(net.is_private)
        ip_net_data["net_total_addr_num"] = str(net.num_addresses)
        ip_net_data["net_tatal_avbl_addr_num"] = str(len([x for x in net.hosts()]))
        ip_net_data["net_num"] = str(net.network_address)
        ip_net_data["net_init_addr"] = str([x for x in net.hosts()][0])
        ip_net_data["net_final_addr"] = str([x for x in net.hosts()][-1])
        ip_net_data["net_addr_range"] = str([x for x in net.hosts()][0]) + ' ~ ' + str([x for x in net.hosts()][-1])
        ip_net_data["net_addr_mask"] = str(net.netmask)
        ip_net_data["net_host_mask"] = str(net.hostmask)
        ip_net_data["net_bradcast_addr"] = str(net.broadcast_address)
        ip_net_data["error"] = False
    except ValueError:
        ip_net_data["error"] = 'your input format is incorrect, please check posted data!'

    return ip_net_data

def get_net_info(data):
    get_response_data = cal_ip(data)
    response = create_response_data(data=get_response_data, file="response_template.j2")
    return response

def create_response_data(data, file):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = file
    template = templateEnv.get_template(TEMPLATE_FILE)
    outputText = template.render(data=data)
    return outputText


if __name__ == "__main__":

    run(addr="0.0.0.0", port=8000)
