# Code by Shankar
# This is code is used to generate CSR and Key and the first step in the certificate management process
# It is imported and triggered by the certificate driver file
# It is used to take the properties from the configuration properties files present in the same directory
# Make sure to check the hardcoded path for the openssl libraires and the configuration.properites file change it if needed
# Make sure python has these libraries imported in the system


from OpenSSL import crypto
import os
import configparser

# Generate a private key
def generate_private_key(save_dir, filename):
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    key_file_path = os.path.join(save_dir, f"{filename}.key")
    with open(key_file_path, "wb") as key_file:
        key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

    return key_file_path, key

def create_openssl_config_with_san(san_dns, save_dir, country, state, city, organization, commonname):
    config_file_path = os.path.join(save_dir, "openssl.cnf")
    with open(config_file_path, "w") as config:
        config.write(f"""
[ req ]
default_bits = 2048
distinguished_name = req_distinguished_name
req_extensions = req_ext
prompt = no

[ req_distinguished_name ]
C = {country}
ST = {state}
L = {city}
O = {organization}
CN = {commonname}

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
""")
        for i, dns in enumerate(san_dns, 1):
            config.write(f"DNS.{i} = {dns}\n")

    return config_file_path


def create_openssl_config(save_dir, country, state, city, organization, commonname):
    config_file_path = os.path.join(save_dir, "openssl.cnf")
    with open(config_file_path, "w") as config:
        config.write(f"""
[ req ]
default_bits = 2048
distinguished_name = req_distinguished_name
prompt = no

[ req_distinguished_name ]
C = {country}
ST = {state}
L = {city}
O = {organization}
CN = {commonname}

""")

    return config_file_path

# Step 3: Generate CSR with SAN using OpenSSL configuration file
def generate_csr_with_san(private_key_path, san_dns, save_dir, country, state, city, organization, commonname, filename, san_check):
    if(san_check):
        config_file_path = create_openssl_config_with_san(san_dns, save_dir, country, state, city, organization, commonname)
    else:
        config_file_path = create_openssl_config(save_dir, country, state, city, organization, commonname)

    try:
        csr_file_path = os.path.join(save_dir, f"{filename}.csr")
        openssl_path = r'"C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe"'
        command = f"{openssl_path} req -new -key {private_key_path} -out {csr_file_path} -config {config_file_path}"
        os.system(command)
        print(f"CSR generated and saved to {csr_file_path}")
        os.remove(config_file_path)

    except Exception as e:
        print(f"An error occurred while generating the CSR: {e}")


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    
    settings = {
        'save_directory': config.get('DEFAULT', 'save_directory'),
        'filename': config.get('DEFAULT', 'filename'),
        'san_check': config.get('DEFAULT', 'san_check').strip().lower() == 'true',
        'san_dns': config.get('DEFAULT', 'san_dns').split(','),
        'country': config.get('DEFAULT', 'country'),
        'state': config.get('DEFAULT', 'state'),
        'city': config.get('DEFAULT', 'city'),
        'organization': config.get('DEFAULT', 'organization'),
        'commonname': config.get('DEFAULT', 'commonname'),
        'opensslpath': config.get('DEFAULT', 'opensslpath')
    }
    return settings


def maincsrdriver():    
    config_file = "E:\\Shankar\\Certificate\\configuration.properties"
    config = read_config(config_file)
    save_directory = config['save_directory']
    filename = config['filename']
    san_check = config['san_check']
    san_dns = config['san_dns']
    country = config['country']
    state = config['state']
    city = config['city']
    organization = config['organization']
    commonname = config['commonname']
    try:
    # Code that may raise an exception
        private_key_path, private_key = generate_private_key(save_directory, filename)
        if(not private_key):
            raise Exception("Private key is missing or invalid!")
    except Exception as e:
        print(f"An error occurred while generating Private Key: {e}")
    try:
    # Code that may raise an exception
        generate_csr_with_san(private_key_path, san_dns, save_directory, country, state, city, organization, commonname, filename, san_check)
    except Exception as e:
        print(f"An error occurred while generating CSR: {e}")