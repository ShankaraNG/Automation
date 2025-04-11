#!/bin/bash

######################################################################################
## Certificate Manager Shell Script                                                 ##
## Script by Shankar                                                                ##
## Date: 09-AUG-2023                                                                ##
######################################################################################

# Function 1: Using OpenSSL to check certificate
check_cert_openssl() {
    HOST=$1
    PORT=$2
    inputpath=$3
    outputpath=$4
    certname=$5
    keyname=$6
    keystorecheck=$7
    keystorename=$8
    truststorecheck=$9
    truststorename=${10}
    
    echo "Checking certificate using OpenSSL for $HOST:$PORT"
    echo | openssl s_client -connect ${HOST}:${PORT} </dev/null 2>/dev/null | \
    openssl x509 -noout -issuer -subject -dates > certificateoutput.txt
    
    expirydate=$(grep notAfter certificateoutput.txt | awk -F"=" '{print $2}' | awk '{print $1" "$2" "$4}')
    expirydateinseconds=$(date -d "$expirydate" +%s)
    currentdateinseconds=$(date -d now +%s)
    seconds_expire=$(expr $expirydateinseconds - $currentdateinseconds)
    covert_todays=$(expr $seconds_expire / 86400)

    if [[ "$covert_todays" == 10 ]]; then
        # Mention the Path to your Python Script
        python certificateDriver.py

        if [[ "$keystorecheck" == "False" ]]; then
            # Backup old cert files
            cd "$outputpath"
            mkdir "certbackup_$(date +%d-%m-%Y)"
            chmod 775 "certbackup_$(date +%d-%m-%Y)"
            cp * "$outputpath/certbackup_$(date +%d-%m-%Y)/"
            mv "$certname" "$outputpath"
            mv "$keyname" "$outputpath"
            echo "certificate and key are moved to the required path"
        elif [[ "$keystorecheck" == "True" ]]; then
            cd "$outputpath"
            mkdir "certbackup_$(date +%d-%m-%Y)"
            chmod 775 "certbackup_$(date +%d-%m-%Y)"
            cp * "$outputpath/certbackup_$(date +%d-%m-%Y)/"
            mv "$keystorename" "$outputpath"
            echo "Keystore is moved to the required path"
        elif [[ "$keystorecheck" == "True" && "$truststorecheck" == "True" ]]; then
            cd "$outputpath"
            mkdir "certbackup_$(date +%d-%m-%Y)"
            chmod 775 "certbackup_$(date +%d-%m-%Y)"
            cp * "$outputpath/certbackup_$(date +%d-%m-%Y)/"
            mv "$keystorename" "$outputpath"
            mv "$truststorename" "$outputpath"
            echo "Trust Store and Keystore are moved to the required path"
        else
            echo "Invalid Input for certificate check"
        fi
    else
        echo "There is still time for the certificate to expire"
    fi
}

# Function 2: Using cURL to check certificate
check_cert_curl() {
    URL=$1
    inputpath=$2
    outputpath=$3
    certname=$4
    keyname=$5
    keystorecheck=$6
    keystorename=$7
    truststorecheck=$8
    truststorename=$9
    
    echo "Checking certificate using curl for $URL"
    curl -svo /dev/null -k "$URL" 2>&1 | \
    egrep 'subject:|issuer:|start date:|expire date:|SSL connection using' > certificateoutput.txt
    
    expirydate=$(grep -i "expire date:" certificateoutput.txt | awk -F"expire date:" '{print $2}' | awk '{print $1" "$2" "$4}')
    expirydateinseconds=$(date -d "$expirydate" +%s)
    currentdateinseconds=$(date -d now +%s)
    seconds_expire=$(expr $expirydateinseconds - $currentdateinseconds)
    covert_todays=$(expr $seconds_expire / 86400)

    if [[ "$covert_todays" == 10 ]]; then
        # Mention the Path to your Python Script
        python certificateDriver.py

        if [[ "$keystorecheck" == "False" ]]; then
            # Backup old cert files
            cd "$outputpath"
            mkdir "certbackup_$(date +%d-%m-%Y)"
            chmod 775 "certbackup_$(date +%d-%m-%Y)"
            cp * "$outputpath/certbackup_$(date +%d-%m-%Y)/"
            mv "$certname" "$outputpath"
            mv "$keyname" "$outputpath"
            echo "certificate and key are moved to the required path"
        elif [[ "$keystorecheck" == "True" ]]; then
            cd "$outputpath"
            mkdir "certbackup_$(date +%d-%m-%Y)"
            chmod 775 "certbackup_$(date +%d-%m-%Y)"
            cp * "$outputpath/certbackup_$(date +%d-%m-%Y)/"
            mv "$keystorename" "$outputpath"
            echo "Keystore is moved to the required path"
        elif [[ "$keystorecheck" == "True" && "$truststorecheck" == "True" ]]; then
            cd "$outputpath"
            mkdir "certbackup_$(date +%d-%m-%Y)"
            chmod 775 "certbackup_$(date +%d-%m-%Y)"
            cp * "$outputpath/certbackup_$(date +%d-%m-%Y)/"
            mv "$keystorename" "$outputpath"
            mv "$truststorename" "$outputpath"
            echo "Trust Store and Keystore are moved to the required path"
        else
            echo "Invalid Input for certificate check"
        fi
    else
        echo "There is still time for the certificate to expire"
    fi
}

###########User Input#####################
# URL to check
URL="https://google.co.in:443"
# Backend system check (False for HTTP/HTTPS interaction, True for direct TLS interaction)
BackendCheck="False"
# Input path where the certificate or keystore will be generated
inputpath="/app/monitoring/shankar/"
# Output path where you want the certificate or keystore to go
outputpath="/app/monitoring/shankar/"
# Certificate and private key names with the path
certname="/app/monitoring/shankar/shankar.cer"
keyname="/app/monitoring/shankar/shankar.key"
# Keystore check, if keystore is required put true and specify the path and keystorename
keystorecheck="True"
keystorename="/app/monitoring/shankar/shankar.jks"
# Truststore check, if truststore is required put true and specify the path and truststorename
truststorecheck="True"
truststorename="/app/monitoring/shankar/shankar_trust.jks"

# Check if the URL starts with "https://"
if [[ "$URL" == https://* ]]; then
    echo "URL starts with https://"
    check_cert_curl "$URL" "$inputpath" "$outputpath" "$certname" "$keyname" "$keystorecheck" "$keystorename" "$truststorecheck" "$truststorename"
elif [[ "$URL" != https://* && "$BackendCheck" == "False" ]]; then
    echo "URL does NOT start with https://"
    URL="https://$URL"  
    check_cert_curl "$URL" "$inputpath" "$outputpath" "$certname" "$keyname" "$keystorecheck" "$keystorename" "$truststorecheck" "$truststorename"
elif [[ "$URL" != https://* && "$BackendCheck" == "True" ]]; then
    # Extract host and port from the URL (for OpenSSL)
    host=$(echo "$URL" | sed -e 's/:.*//')
    port=$(echo "$URL" | sed 's/.*://')
    check_cert_openssl "$host" "$port" "$inputpath" "$outputpath" "$certname" "$keyname" "$keystorecheck" "$keystorename" "$truststorecheck" "$truststorename"
else
    echo "Invalid URL"
fi
