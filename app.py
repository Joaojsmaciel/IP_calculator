from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

def get_ip_class(ip):
    first_octet = int(str(ip).split('.')[0])
    if 1 <= first_octet <= 126:
        return 'A'
    elif 128 <= first_octet <= 191:
        return 'B'
    elif 192 <= first_octet <= 223:
        return 'C'
    elif 224 <= first_octet <= 239:
        return 'D'
    elif 240 <= first_octet <= 255:
        return 'E'
    return 'Desconhecida'

def get_default_mask(ip_class):
    masks = {
        'A': '255.0.0.0',
        'B': '255.255.0.0',
        'C': '255.255.255.0',
        'D': '255.255.255.255',
        'E': '255.255.255.255'
    }
    return masks.get(ip_class, 'Desconhecida')

def get_cidr_from_mask(mask):
    return sum([bin(int(x)).count('1') for x in mask.split('.')])

def get_binary_mask(mask):
    return '.'.join([format(int(x), '08b') for x in mask.split('.')])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    ip = request.form['ip']
    try:
        ip_obj = ipaddress.ip_address(ip)
        ip_class = get_ip_class(ip_obj)
        default_mask = get_default_mask(ip_class)
        cidr = get_cidr_from_mask(default_mask)
        
        rede = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)
        primeiro_host = list(rede.hosts())[0]
        ultimo_host = list(rede.hosts())[-1]
        
        return render_template('index.html',
                           resultado=True,
                           ip=ip,
                           cidr=cidr,
                           mascara=default_mask,
                           mascara_binaria=get_binary_mask(default_mask),
                           classe=ip_class,
                           rede=rede.network_address,
                           broadcast=rede.broadcast_address,
                           total_hosts=rede.num_addresses - 2,
                           primeiro_host=primeiro_host,
                           ultimo_host=ultimo_host)
    except ValueError as e:
        return render_template('index.html', erro=str(e))

if __name__ == '__main__':
    app.run(debug=True)
