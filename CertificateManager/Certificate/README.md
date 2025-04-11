Certificate Manager Tool
Code by Shankar

The main driver file is the certificate.Driver.py
This is the file that needs to be triggered from the shell or the batch script present in the previous section
Please make sure the imports and the path are correct and is working according test end to end

Configuration.properties

This is the file where you need to mention the configuration of the certificate like
The subject, The type of cert file you require, Do you have intermediate certificate or not
You will also have the other options like do you require keystore or not etc. please have a look and fill it according to the instructions
present in the file

In every python file
There are harded coded path for the openssl librarires and for the configuration.properties files please make sure to adjust based on where you place
the files.
