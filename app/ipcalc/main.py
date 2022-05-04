#!/usr/bin/env python3
from flask import Flask, request
import sys
import ipaddress
import jinja2

app = Flask(__name__)
@app.route('/')
def hello_world():
    response = create_response_data(data="", file="default_template.j2")
    return '''{}'''.format(response)

@app.route('/calc')
def calc():
    # if key doesn't exist, returns None
    data = request.args.get('net')
    response = get_net_info(data)
    return '''{}'''.format(response)

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

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
