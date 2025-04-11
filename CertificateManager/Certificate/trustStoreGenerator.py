# Code by Shankar
# This is code is used to generate Trust Store for your certificate
# It is imported and triggered by the certificate driver file
# It is used to take the properties from the configuration properties files present in the same directory
# Make sure to check the hardcoded path for the openssl libraires and the configuration.properites file change it if needed
# Make sure python has these libraries imported in the system


import subprocess
import os
import datetime
import configparser

def truststorewithfullchain(keytoolpath, pathtofile,filename,truststorename,truststore_password, truststore_type, alias, bouncy_castle_provider_jar):
    def import_certificate(keytoolpath, cert_file, alias, truststorepath, truststore_password, truststore_type):
    # Form the keytool command
        command = [
            keytoolpath, "-import", "-v", "-trustcacerts",
            "-alias", alias, "-file", cert_file,
            "-keystore", truststorepath, "-storepass", truststore_password,
            "-storetype", truststore_type, "-noprompt"
        ]
    
        try:
            subprocess.run(command, check=True)
            print(f"Successfully imported {cert_file} into {truststorepath} with alias {alias}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while importing {cert_file}: {e}")
            
    def import_certificate_of_bks(keytoolpath, cert_file, alias, truststorepath, truststore_password, truststore_type, bouncy_castle_provider_jar):
    # Form the keytool command
        command = [
            keytoolpath, "-import", "-v", "-trustcacerts",
            "-alias", alias, "-file", cert_file,
            "-keystore", truststorepath, "-storepass", truststore_password,
            "-storetype", truststore_type, "-noprompt",
            "-providerpath", bouncy_castle_provider_jar,  # Path to Bouncy Castle JAR
            "-providerClass", "org.bouncycastle.jce.provider.BouncyCastleProvider"  # Use Bouncy Castle provider
            ]
    
        try:
        # Run the command
            subprocess.run(command, check=True)
            print(f"Successfully imported {cert_file} into {truststorepath} with alias {alias}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while importing {cert_file}: {e}")

    # Create a full chain of certificates
    certificate_crt= os.path.join(pathtofile, f"{filename}_certificate.pem")
    intermediate_crt= os.path.join(pathtofile, f"{filename}_intermediate_certificate.pem")
    root_crt= os.path.join(pathtofile, f"{filename}_root_certificate.pem")
    
    private_key_filename=os.path.join(pathtofile, f"{filename}.key")
    truststorepath=os.path.join(pathtofile, f"{truststorename}.{truststore_type}")
    
    certificates = [
        certificate_crt,        # Root certificate
        intermediate_crt, # Intermediate certificate
        root_crt       # Server certificate
    ]
    
    aliasnames = [
        alias,
        "intermediate",
        "root"
    ]
    
    if(truststore_type == "p12" or truststore_type == "jks" or truststore_type == "jceks"):
        for i in range(len(certificates)):
            alias_name = aliasnames[i]
            cert_file = certificates[i]
            import_certificate(keytoolpath, cert_file, alias_name, truststorepath, truststore_password, truststore_type)
            print(f"Import of the certificate to the the truststore is completed: {truststorepath}")
    elif(truststore_type == "bks"):
        for i in range(len(certificates)):
            alias_name = aliasnames[i]
            cert_file = certificates[i]
            import_certificate_of_bks(keytoolpath, cert_file, alias_name, truststorepath, truststore_password, truststore_type, bouncy_castle_provider_jar)
            print(f"Import of the certificate to the the truststore is completed: {truststorepath}")        
        
def truststorewithonlyselfsigned(keytoolpath, pathtofile,filename,truststorename,truststore_password, truststore_type, alias, bouncy_castle_provider_jar):

    def import_certificate_self(keytoolpath, cert_file, alias, truststorepath, truststore_password, truststore_type):
    # Form the keytool command
        command = [
            keytoolpath, "-import", "-v", "-trustcacerts",
            "-alias", alias, "-file", cert_file,
            "-keystore", truststorepath, "-storepass", truststore_password,
            "-storetype", truststore_type, "-noprompt"
        ]
    
        try:
            subprocess.run(command, check=True)
            print(f"Successfully imported {cert_file} into {truststorepath} with alias {alias}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while importing {cert_file}: {e}")
            
    def import_certificate_self_of_bks(keytoolpath, cert_file, alias, truststorepath, truststore_password, truststore_type, bouncy_castle_provider_jar):
    # Form the keytool command
        command = [
            keytoolpath, "-import", "-v", "-trustcacerts",
            "-alias", alias, "-file", cert_file,
            "-keystore", truststorepath, "-storepass", truststore_password,
            "-storetype", truststore_type, "-noprompt",
            "-providerpath", bouncy_castle_provider_jar,  # Path to Bouncy Castle JAR
            "-providerClass", "org.bouncycastle.jce.provider.BouncyCastleProvider"  # Use Bouncy Castle provider
            ]
    
        try:
        # Run the command
            subprocess.run(command, check=True)
            print(f"Successfully imported {cert_file} into {truststorepath} with alias {alias}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while importing {cert_file}: {e}")

    certificate_crt= os.path.join(pathtofile, f"{filename}_certificate.pem")
    
    private_key_filename=os.path.join(pathtofile, f"{filename}.key")
    truststorepath=os.path.join(pathtofile, f"{truststorename}.{truststore_type}")
    
    
    if(truststore_type == "p12" or truststore_type == "jks" or truststore_type == "jceks"):
        import_certificate_self(keytoolpath, certificate_crt, alias, truststorepath, truststore_password, truststore_type)
        print(f"Import of the certificate to the the truststore is completed: {truststorepath}")
    elif(truststore_type == "bks"):
        import_certificate_self_of_bks(keytoolpath, certificate_crt, alias, truststorepath, truststore_password, truststore_type, bouncy_castle_provider_jar)
        print(f"Import of the certificate to the the truststore is completed: {truststorepath}")        
        


def read_trust_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    
    settings = {
        'save_directory': config.get('DEFAULT', 'save_directory'),
        'filename': config.get('DEFAULT', 'filename'),
        'keytoolpath': config.get('DEFAULT', 'keytoolpath'),
        'bouncy_castle_provider_jar': config.get('DEFAULT', 'bc_provider_path'),
        'alias': config.get('DEFAULT', 'alias'),
        'truststorename': config.get('DEFAULT', 'truststorename'),
        'truststoretypeRequired': config.get('DEFAULT', 'truststoretypeRequired'),
        'truststoreformatRequired': config.get('DEFAULT', 'truststoreformatRequired'),
        'truststore_password': config.get('DEFAULT', 'truststore_password'),
        'truststoreindicator': config.get('DEFAULT', 'truststoreindicator').strip().lower() == 'true'
    }
    return settings

def maintruststoredriver():    
    config_file = "E:\\Shankar\\Certificate\\configuration.properties"
    config = read_trust_config(config_file)
    save_directory = config['save_directory']
    filename = config['filename']
    keytoolpath = config['keytoolpath']
    bouncy_castle_provider_jar = config['bouncy_castle_provider_jar']
    alias = config['alias']
    truststore_password = config['truststore_password']
    truststorename = config['truststorename']
    truststoretypeRequired = config['truststoretypeRequired']
    truststoreindicator = config['truststoreindicator']
    truststoreformatRequired = config['truststoreformatRequired']
    try:
        if(truststoreindicator):
            if(truststoreformatRequired=='fullchaintruststore'):
                print("Creating a full chain Trust Store")
                truststorewithfullchain(keytoolpath, save_directory,filename,truststorename,truststore_password, truststoretypeRequired, alias, bouncy_castle_provider_jar)
                print("Trust Store Created")
            elif(truststoreformatRequired=='selfsignedtruststore'):
                print("Creating a self signed Trust Store")
                truststorewithonlyselfsigned(keytoolpath, save_directory,filename,truststorename,truststore_password, truststoretypeRequired, alias, bouncy_castle_provider_jar)
                print("Trust Store Created")
            else:
                raise Exception("Invalid Input for the truststoretypeRequired")
        else:
            print("Trust store not required")
    except Exception as e:
        print(f"Error: {e}")

