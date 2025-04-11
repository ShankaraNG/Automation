# Code by Shankar
# This is code is used to generate keystore for your certificate
# It is imported and triggered by the certificate driver file
# It is used to take the properties from the configuration properties files present in the same directory
# Make sure to check the hardcoded path for the openssl libraires and the configuration.properites file change it if needed
# Make sure python has these libraries imported in the system


import subprocess
import os
import datetime
import configparser

def keystorewithfullchain(pathtofile,filename,keystorename,keystore_password):
    # Create a full chain of certificates
    fullchain= os.path.join(pathtofile, f"{filename}_fullchain.crt")
    certificate_crt= os.path.join(pathtofile, f"{filename}_certificate.pem")
    intermediate_crt= os.path.join(pathtofile, f"{filename}_intermediate_certificate.pem")
    root_crt= os.path.join(pathtofile, f"{filename}_root_certificate.pem")
    try:
        with open(fullchain, "wb") as f:
            with open(certificate_crt, "rb") as cert:
                f.write(cert.read())
            with open(intermediate_crt, "rb") as intermediate:
                f.write(intermediate.read())
            with open(root_crt, "rb") as root:
                f.write(root.read())

            print(f"Full chain created successfully at {fullchain}.")       
    except Exception as e:
        print(f"Error while creating full chain: {e}")
    # Define the OpenSSL command with the password option
    private_key_filename=os.path.join(pathtofile, f"{filename}.key")
    keystorename=os.path.join(pathtofile, f"{keystorename}.p12")
    openssl_path = r'"C:\\"Program Files"\\OpenSSL-Win64\\bin\\openssl.exe"'
    openssl_command = f'{openssl_path} pkcs12 -export -in {fullchain} -inkey {private_key_filename} -out {keystorename} -password pass:{keystore_password}'
    try:
        result = os.system(openssl_command)
        if result == 0:
            print("Keystore created successfully")
        else:
            raise Exception("An error occurred while running the OpenSSL command")
    except Exception as e:
        print(f"An error occurred while running the OpenSSL command: {e}")   


def keystorewithonlycertificate(pathtofile,filename,keystorename,keystore_password):
    # Define the OpenSSL command with the password option
    certificate_crt= os.path.join(pathtofile, f"{filename}_certificate.pem")
    private_key_filename=os.path.join(pathtofile, f"{filename}.key")
    keystorename=os.path.join(pathtofile, f"{keystorename}.p12")
    openssl_path = r'"C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe"'
    openssl_command = f'{openssl_path} pkcs12 -export -in {certificate_crt} -inkey {private_key_filename} -out {keystorename} -password pass:{keystore_password}'
    try:
        result = os.system(openssl_command)
        if result == 0:
            print("Keystore created successfully")
        else:
            raise Exception("An error occurred while running the OpenSSL command")
    except Exception as e:
        print(f"An error occurred while running the OpenSSL command: {e}")   

def converttojks(keytoolpath, pathtofile, keystorename, src_password, dest_password):
    src_keystore=os.path.join(pathtofile, f"{keystorename}.p12")
    dest_keystore=os.path.join(pathtofile, f"{keystorename}.jks")
    command = [
        keytoolpath, #add your keytool path
        "-importkeystore", 
        "-srckeystore", src_keystore, 
        "-srcstoretype", "PKCS12", 
        "-srcstorepass", src_password,
        "-destkeystore", dest_keystore, 
        "-deststoretype", "JKS", 
        "-deststorepass", dest_password
    ]

    # Run the command using subprocess
    try:
        subprocess.run(command, check=True)
        print(f"Keystore {src_keystore} converted to JKS successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def converttobks(keytoolpath, pathtofile, keystorename, src_password, dest_password, bc_provider_path):
    src_keystore=os.path.join(pathtofile, f"{keystorename}.p12")
    dest_keystore=os.path.join(pathtofile, f"{keystorename}.bks")    
    command = [
        keytoolpath, 
        "-importkeystore", 
        "-srckeystore", src_keystore, 
        "-srcstoretype", "PKCS12", 
        "-srcstorepass", src_password,   # Specify source keystore password
        "-destkeystore", dest_keystore, 
        "-deststoretype", "BKS", 
        "-deststorepass", dest_password, # Specify destination keystore password
        "-providerClass", "org.bouncycastle.jce.provider.BouncyCastleProvider", 
        "-providerPath", bc_provider_path  # Path to Bouncy Castle JAR file
    ]

    # Run the command using subprocess
    try:
        subprocess.run(command, check=True)
        print(f"Keystore {src_keystore} converted to BKS successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def converttojceks(keytoolpath, pathtofile, keystorename, src_password, dest_password):
    src_keystore=os.path.join(pathtofile, f"{keystorename}.p12")
    dest_keystore=os.path.join(pathtofile, f"{keystorename}.jceks")
    command = [
        keytoolpath, 
        "-importkeystore", 
        "-srckeystore", src_keystore, 
        "-srcstoretype", "PKCS12", 
        "-srcstorepass", src_password,   # Specify source keystore password
        "-destkeystore", dest_keystore, 
        "-deststoretype", "JCEKS", 
        "-deststorepass", dest_password  # Specify destination keystore password
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Keystore {src_keystore} converted to JCEKS successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def convert_pem_to_crt(pathtofile,filename):
    pem_file=os.path.join(pathtofile, f"{filename}_certificate.pem")
    crt_file=os.path.join(pathtofile, f"{filename}_certificate.crt")
    # openssl_path = r'"C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe"'
    # command = [
    #     openssl_path, "x509", 
    #     "-in", pem_file, 
    #     "-out", crt_file
    # ]
    
    # try:
    #     subprocess.run(command, check=True)
    #     print(f"Successfully converted {pem_file} to {crt_file}")
    # except subprocess.CalledProcessError as e:
    #     print(f"An error occurred: {e}")
    openssl_path = r'"C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe"'
    openssl_command = f'{openssl_path} x509 -in {pem_file} -out {crt_file}'
    try:
        result = os.system(openssl_command)
        if result == 0:
            print(f"Successfully converted {pem_file} to {crt_file}")
        else:
            raise Exception(f"An error occurred while running the OpenSSL command")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_pem_to_cer(pathtofile,filename):
    pem_file=os.path.join(pathtofile, f"{filename}_certificate.pem")
    cer_file=os.path.join(pathtofile, f"{filename}_certificate.cer")
    openssl_path = r'"C:\\Program Files\\OpenSSL-Win64\\bin\\openssl.exe"'
    openssl_command = f'{openssl_path} x509 -in {pem_file} -out {cer_file}'
    try:
        result = os.system(openssl_command)
        if result == 0:
            print(f"Successfully converted {pem_file} to {cer_file}")
        else:
            raise Exception(f"An error occurred while running the OpenSSL command")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_key_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    
    settings = {
        'save_directory': config.get('DEFAULT', 'save_directory'),
        'filename': config.get('DEFAULT', 'filename'),
        'keytoolpath': config.get('DEFAULT', 'keytoolpath'),
        'bc_provider_path': config.get('DEFAULT', 'bc_provider_path'),
        'keystore_password': config.get('DEFAULT', 'keystore_password'),
        'keystorename': config.get('DEFAULT', 'keystorename'),
        'keystoretypeRequired': config.get('DEFAULT', 'keystoretypeRequired'),
        'keystoreformatRequired': config.get('DEFAULT', 'keystoreformatRequired'),
        'keystoreindicator': config.get('DEFAULT', 'keystoreindicator').strip().lower() == 'true'
    }
    return settings
def mainkeystoredriver():    
    config_file = "E:\\Shankar\\Certificate\\configuration.properties"
    config = read_key_config(config_file)
    save_directory = config['save_directory']
    filename = config['filename']
    keytoolpath = config['keytoolpath']
    bc_provider_path = config['bc_provider_path']
    keystore_password = config['keystore_password']
    keystorename = config['keystorename']
    keystoretypeRequired = config['keystoretypeRequired']
    keystoreformatRequired = config['keystoreformatRequired']
    keystoreindicator = config['keystoreindicator']
    try:
        if(keystoreindicator):
            if(keystoretypeRequired=='fullchainkeystore'):
                print("Creating a full chain keystore")
                keystorewithfullchain(save_directory,filename,keystorename,keystore_password)
                if(keystoreformatRequired == "jks"):
                    converttojks(keytoolpath, save_directory, keystorename, keystore_password, keystore_password)
                    print("Keystore Created in the JKS format")
                elif(keystoreformatRequired == "p12"):
                    print("Keystore Created in the p12 format")
                elif(keystoreformatRequired == "bks"):
                    converttobks(keytoolpath, save_directory, keystorename, keystore_password, keystore_password, bc_provider_path)
                    print("Keystore Created in the bks format")
                elif(keystoreformatRequired == "jceks"):
                    converttojceks(keytoolpath, save_directory, keystorename, keystore_password, keystore_password)
                else:
                    raise Exception("Invalid Input for the keystoreformat")
            elif(keystoretypeRequired=='selfsignedkeystore'):
                keystorewithonlycertificate(save_directory,filename,keystorename,keystore_password)
                print("Creating only self signed certificate keystore")
                if(keystoreformatRequired == "jks"):
                    converttojks(keytoolpath, save_directory, keystorename, keystore_password, keystore_password)
                    print("Keystore Created in the JKS format")
                elif(keystoreformatRequired == "p12"):
                    print("Keystore Created in the p12 format")
                elif(keystoreformatRequired == "bks"):
                    converttobks(keytoolpath, save_directory, keystorename, keystore_password, keystore_password, bc_provider_path)
                    print("Keystore Created in the bks format")
                elif(keystoreformatRequired == "jceks"):
                    converttojceks(keytoolpath, save_directory, keystorename, keystore_password, keystore_password)
                    print("Keystore Created in the jceks format")
                else:
                    raise Exception("Invalid Input for the keystoreformat")
            else:
                raise Exception("Invalid Input for the keystoretypeRequired")
        elif(not keystoreindicator):
            if(keystoretypeRequired== "cer"):
                convert_pem_to_cer(save_directory,filename)
                print("certificates converted into cer format")
            elif(keystoreformatRequired == "pem"):
                print("certificates converted into pem format")
            elif(keystoreformatRequired == "crt"):
                    convert_pem_to_crt(save_directory,filename)
                    print("certificates converted into crt format")
            else:
                raise Exception("Invalid Input for the keystoretypeRequired")
    except Exception as e:
        print(f"Error: {e}")