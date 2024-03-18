import bech32
import argparse
import re
import json

# Address validation - make sure the user inputs a correct cosmos type address
def address_validation(address: str) -> bool:

    def validate_string(address: str) -> bool:
        regex_pattern = r'.*1[a-zA-Z0-9]{38}$'
        return re.match(regex_pattern, address) is not None        

    # Verify address checksum
    def verify_checksum(address: str) -> bool:
        _, decoded = bech32.bech32_decode(address)

        if decoded is not None:
            return len(decoded) == 32
        else:
            return False
        
    if validate_string(address) and verify_checksum(address):
        return True    
    else:
        return False

# Json load
def load_json_list(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def main():
    
    # Define global variables
    global address, to_prefix
    
    # Init parser
    parser = argparse.ArgumentParser(prog='Cosmos address converter',
                                     description='Converts the input address into any other cosmos compatible address')
    
    # Parser arguments
    parser.add_argument('--address', dest='address', default='', required=True, help='address to be converted')
    parser.add_argument('--to', dest='to_prefix', default='osmosis', help='to prefix. type "all" to convert to every cosmos chain at once.')
    
    args = parser.parse_args()
    address = args.address
    to_prefix = args.to_prefix

    if address_validation(address):

        # Decode the address
        try:
            prefix, canonical = bech32.bech32_decode(address)
        except Exception as err:
            print(f'Error parsing "{address}" as bech32 address: {err}')  

        # if 'all' prefix is selected
        if to_prefix == 'all':
            # Load prefixes stored in json file
            prefixes = load_json_list('bech32PrefixAccAddr.json')

            # Create a new addresses list to catch all
            new_address_list = []

            # Loop through prefixes and encode new addresses
            for prefix in prefixes:
                try:
                    new_address_list.append(bech32.bech32_encode(prefix, canonical))
                except Exception as err: 
                    new_address_list.append('error')

            # Print everything
            print(f'Original address  : {address}')
            print('----------------------------------------')
            for item in new_address_list:
                print(f'Converted address : {item}')

        # if custom prefix is selected (default=osmosis)
        else:    
            new_prefix = prefix.replace(prefix, to_prefix)

            # Encode the address
            try:
                new_address = bech32.bech32_encode(new_prefix, canonical)
            except Exception as err:
                print(f'Error converting "{address}" to "{to_prefix}" prefix: {err}')

            # Print the 2 addresses
            print(f'Original address  : {address}')
            print(f'Converted address : {new_address}')

    else:    
        print('Please input a valid cosmos type address!')
        exit()

# Main
if __name__ == "__main__":
    main()
