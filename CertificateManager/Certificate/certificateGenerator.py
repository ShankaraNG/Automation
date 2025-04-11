# Code by Shankar
# This is code is used to generate the certificates based on the CSR and Key
# It is imported and triggered by the certificate driver file
# It is used to take the properties from the configuration properties files present in the same directory
# Make sure to check the hardcoded path for the openssl libraires and the configuration.properites file change it if needed
# Make sure python has these libraries imported in the system


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import CertificateBuilder, Name, NameAttribute, ExtensionNotFound, DNSName, IPAddress, SubjectAlternativeName
from cryptography.x509 import load_pem_x509_csr, load_pem_x509_certificate
from cryptography.hazmat.primitives import hashes
import datetime
import configparser
import os

# Function to add SANs to the certificate builder
def add_san_extension(cert_builder, san_list):
    san_extension = []
    for san in san_list:
        san_extension.append(DNSName(san))

    # Add the SAN extension to the certificate
    san_extension = SubjectAlternativeName(san_extension)
    cert_builder = cert_builder.add_extension(san_extension, critical=False)
    return cert_builder

def selfsignedcertificate(pathtofile,filename, san_check, san_dns):
    keyfilepath= os.path.join(pathtofile, f"{filename}.key")
    with open(keyfilepath, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    csrfilepath= os.path.join(pathtofile, f"{filename}.csr")
    with open(csrfilepath, 'rb') as csr_file:
        csr = load_pem_x509_csr(csr_file.read())

    subject = csr.subject
    print(f"CSR Subject: {subject}")
    
    certificate_builder = CertificateBuilder()
    # Use CSR's subject for self-signed certificate
    certificate_builder = certificate_builder.subject_name(subject)
    # Set issuer as the same subject for a self-signed certificate
    certificate_builder = certificate_builder.issuer_name(subject)
    # Use the public key from the CSR to generate the certificate
    certificate_builder = certificate_builder.public_key(csr.public_key())
    # Set certificate validity period 
    not_valid_before = datetime.datetime.utcnow()
    not_valid_after = not_valid_before + datetime.timedelta(days=365)
    certificate_builder = certificate_builder.not_valid_before(not_valid_before)
    certificate_builder = certificate_builder.not_valid_after(not_valid_after)
    # Set the serial number (could be any large number, for example 1000)
    certificate_builder = certificate_builder.serial_number(1000)
    if san_check:
        certificate_builder = add_san_extension(certificate_builder, san_dns)
    # Sign the certificate with the private key
    certificate = certificate_builder.sign(private_key=private_key, algorithm=hashes.SHA256())
    # Save the self-signed certificate to a file
    certfilepath= os.path.join(pathtofile, f"{filename}_certificate.pem")
    with open(certfilepath, 'wb') as cert_file:
        cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))
    print("Self-signed certificate generated successfully.")


def selfsignedcertificate_Withrootandintermediate_withoutCSRandKeyforrootandintermediate(pathtofile,filename, san_check, san_dns):
    # Function to generate a certificate from a CSR
    def generate_certificate_withoutCSRandKeyforrootandintermediate(csr, private_key, issuer_name, serial_number, valid_days, issuer_private_key, san_checker, san_dns):
        certificate_builder = CertificateBuilder()
        certificate_builder = certificate_builder.subject_name(csr.subject)
        certificate_builder = certificate_builder.issuer_name(issuer_name)
        certificate_builder = certificate_builder.public_key(csr.public_key())
        
        not_valid_before = datetime.datetime.utcnow()
        not_valid_after = not_valid_before + datetime.timedelta(days=valid_days)
        certificate_builder = certificate_builder.not_valid_before(not_valid_before)
        certificate_builder = certificate_builder.not_valid_after(not_valid_after)
        
        certificate_builder = certificate_builder.serial_number(serial_number)
        
        if san_checker:
            certificate_builder = add_san_extension(certificate_builder, san_dns)
        
        # Sign the certificate with the private key of the issuer (or self for root)
        if issuer_private_key:
            certificate = certificate_builder.sign(private_key=issuer_private_key, algorithm=hashes.SHA256())
        else:
            certificate = certificate_builder.sign(private_key=private_key, algorithm=hashes.SHA256())
        
        return certificate


    keyfilepath= os.path.join(pathtofile, f"{filename}.key")
    # Load the private key for the root CA from a file
    with open(keyfilepath, 'rb') as key_file:
        root_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    # Load the CSR for the end entity (leaf certificate)
    csrfilepath= os.path.join(pathtofile, f"{filename}.csr")
    with open(csrfilepath, 'rb') as csr_file:
        end_entity_csr = load_pem_x509_csr(csr_file.read())

    # Extract subject information from CSR (optional)
    subject = end_entity_csr.subject
    print(f"End Entity CSR Subject: {subject}")

    # Generate Root Certificate (Self-signed)
    root_subject = subject
    root_certificate = generate_certificate_withoutCSRandKeyforrootandintermediate(end_entity_csr, root_private_key, root_subject, serial_number=1000, valid_days=3650, issuer_private_key=None, san_checker=False, san_dns=san_dns)  # Root certificate valid for 10 years
    rootcertfilepath= os.path.join(pathtofile, f"{filename}_root_certificate.pem")
    with open(rootcertfilepath, 'wb') as root_cert_file:
        root_cert_file.write(root_certificate.public_bytes(serialization.Encoding.PEM))

    print("Root certificate generated successfully.")

    #Generate Intermediate Certificate signed by Root Certificate
    intermediate_private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    intermediate_csr = end_entity_csr
    intermediate_certificate = generate_certificate_withoutCSRandKeyforrootandintermediate(intermediate_csr, intermediate_private_key, root_subject, serial_number=2000, valid_days=1825, issuer_private_key=root_private_key, san_checker=False, san_dns=san_dns)
    intermmediatecertfilepath= os.path.join(pathtofile, f"{filename}_intermediate_certificate.pem")
    with open(intermmediatecertfilepath, 'wb') as intermediate_cert_file:
        intermediate_cert_file.write(intermediate_certificate.public_bytes(serialization.Encoding.PEM))
    print("Intermediate certificate generated successfully.")

    # Generate Server Certificate signed by Intermediate Certificate
    certfilepath= os.path.join(pathtofile, f"{filename}_certificate.pem")
    end_entity_certificate = generate_certificate_withoutCSRandKeyforrootandintermediate(end_entity_csr, root_private_key, root_subject, serial_number=3000, valid_days=365, issuer_private_key=intermediate_private_key, san_checker=san_check, san_dns=san_dns)
    with open(certfilepath, 'wb') as end_entity_cert_file:
        end_entity_cert_file.write(end_entity_certificate.public_bytes(serialization.Encoding.PEM))

    print("server certificate generated successfully.")

def selfsignedcertificate_Withrootandintermediate_withCERandKeyforrootandintermediate(pathtofile, filename, san_check, san_dns):

    def generate_certificate_withCERandKeyforrootandintermediate(csr, private_key, issuer_name, serial_number, valid_days, san_check, san_dns, issuer_private_key=None):
        certificate_builder = CertificateBuilder()
        certificate_builder = certificate_builder.subject_name(csr.subject)
        certificate_builder = certificate_builder.issuer_name(issuer_name)
        certificate_builder = certificate_builder.public_key(csr.public_key())
        
        not_valid_before = datetime.datetime.now(datetime.timezone.utc)
        not_valid_after = not_valid_before + datetime.timedelta(days=valid_days)
        certificate_builder = certificate_builder.not_valid_before(not_valid_before)
        certificate_builder = certificate_builder.not_valid_after(not_valid_after)
        
        certificate_builder = certificate_builder.serial_number(serial_number)
        
        if san_check:
            certificate_builder = add_san_extension(certificate_builder, san_dns)
        
        # Sign the certificate with the private key of the issuer (either root or intermediate)
        if issuer_private_key:
            certificate = certificate_builder.sign(private_key=issuer_private_key, algorithm=hashes.SHA256())
        else:
            certificate = certificate_builder.sign(private_key=private_key, algorithm=hashes.SHA256())
        
        return certificate

    # Load the private key for the intermediate CA
    intermediatekeyfilepath= os.path.join(pathtofile, f"{filename}_intermediate_private_key.key")
    with open(intermediatekeyfilepath, 'rb') as key_file:
        intermediate_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    # Load the CSR for the server certificate (leaf certificate)
    csrfilepath= os.path.join(pathtofile, f"{filename}.csr")
    with open(csrfilepath, 'rb') as csr_file:
        end_entity_csr = load_pem_x509_csr(csr_file.read())
    # Load the intermediate certificate
    intermmediatecertfilepath= os.path.join(pathtofile, f"{filename}_intermediate_certificate.pem")
    with open(intermmediatecertfilepath, 'rb') as cert_file:
        intermediate_certificate = load_pem_x509_certificate(cert_file.read())
    subject = end_entity_csr.subject
    print(f"End Entity CSR Subject: {subject}")

    # Generate Server Certificate signed by the Intermediate Certificate
    server_certificate = generate_certificate_withCERandKeyforrootandintermediate(end_entity_csr, intermediate_private_key, intermediate_certificate.subject, serial_number=3000, valid_days=365, san_check=san_check, san_dns=san_dns, issuer_private_key=intermediate_private_key)
    certfilepath= os.path.join(pathtofile, f"{filename}_certificate.pem")
    with open(certfilepath, 'wb') as server_cert_file:
        server_cert_file.write(server_certificate.public_bytes(serialization.Encoding.PEM))
    print("Server certificate signed by intermediate certificate generated successfully.")

def read_cer_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    
    settings = {
        'save_directory': config.get('DEFAULT', 'save_directory'),
        'filename': config.get('DEFAULT', 'filename'),
        'CertTypeRequired': config.get('DEFAULT', 'CertTypeRequired', fallback=None),
        'IntermediateCertFile': config.get('DEFAULT', 'IntermediateCertFile').strip().lower() == 'true',
        'IntermediateKeyFile': config.get('DEFAULT', 'IntermediateKeyFile').strip().lower() == 'true',
        'san_check': config.get('DEFAULT', 'san_check').strip().lower() == 'true',
        'san_dns': config.get('DEFAULT', 'san_dns').split(',')
    }
    return settings

def maincertdriver():    
    config_file = "E:\\Shankar\\Certificate\\configuration.properties"
    config = read_cer_config(config_file)
    save_directory = config['save_directory']
    filename = config['filename']
    CertTypeRequired = config['CertTypeRequired']
    IntermediateCertFile = config['IntermediateCertFile']
    IntermediateKeyFile = config['IntermediateKeyFile']
    san_check = config['san_check']
    san_dns = config['san_dns']
    try:
        if(not CertTypeRequired or CertTypeRequired.isspace()):
            raise ValueError("CertTypeRequired is missing or empty in the configuration file")
        else:
            if(CertTypeRequired == "SelfSignedCert"):
                selfsignedcertificate(save_directory,filename, san_check, san_dns)
            elif(CertTypeRequired == "CertOverIntermmediate"):
                if(IntermediateCertFile and IntermediateKeyFile):
                    print("Generating Certificate over Intermediate")
                    selfsignedcertificate_Withrootandintermediate_withCERandKeyforrootandintermediate(save_directory,filename, san_check, san_dns)
                else:
                    print("Generating Certificate over Intermediate by creating own root and intermmediate certificate")
                    selfsignedcertificate_Withrootandintermediate_withoutCSRandKeyforrootandintermediate(save_directory, filename, san_check, san_dns)
            else:
                raise Exception("The Input value for the the CertTypeRequired is invalid")
    except Exception as e:
        print(f"Error: {e}")