# Code by Shankar
# This is the main driver Code which imports the other python files mentioned in the import section
# It will import and trigger the main driver function in each of the subsequent python files


import CSRAndKeyGeneration
import certificateGenerator
import keystoreGenerator
import trustStoreGenerator

def main():
    try:
        CSRAndKeyGeneration.maincsrdriver()
        certificateGenerator.maincertdriver()
        keystoreGenerator.mainkeystoredriver()
        trustStoreGenerator.maintruststoredriver()
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    main()

