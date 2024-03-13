import bech32
import argparse
import re

# # Address validation - make sure the user inputs a correct cosmos type address
# def address_validation(prefix: str, address: str) -> bool:

#     # Generate address regex
#     def generate_regex(prefix: str) -> str:
#         allowed_chars = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
#         return f"^{prefix}1([{allowed_chars}]+)$"

#     # Verify address checksum
#     def verify_checksum(address: str) -> bool:
#         _, decoded = bech32.bech32_decode(address)

#         if decoded is not None:
#             return len(decoded) == 32
#         else:
#             return False

#     def is_valid_address(regex: str, address: str) -> bool:
#         match = re.match(regex, address)
#         if match:
#             return verify_checksum(address)
#         else:
#             return False

#     regex = generate_regex(prefix)
#     validation = is_valid_address(regex, address)

#     return validation


def main():
    
    # Define global variables
    global address, to_prefix
    
    # Init parser
    parser = argparse.ArgumentParser(prog='Cosmos address converter',
                                     description='Converts the input address into any other cosmos compatible address')
    
    # Parser arguments
    parser.add_argument('--address', dest='address', default='', required=True, help='address to be converted')
    parser.add_argument('--to', dest='to_prefix', default='osmosis', help='to prefix')
    
    args = parser.parse_args()
    address = args.address
    to_prefix = args.to_prefix

    # Decode the address
    try:
        prefix, canonical = bech32.bech32_decode(address)
    except Exception as err:
        print(f'Error parsing "{address}" as bech32 address: {err}')  

    # Set new prefix (default = osmosis)
    new_prefix = prefix.replace(prefix, to_prefix)

    # Encode the address
    try:
        new_address = bech32.bech32_encode(new_prefix, canonical)
    except Exception as err:
        print(f'Error converting "{address}" to "{to_prefix}" prefix: {err}')

    print(f'Original address : {address}')
    print(f'Converted address: {new_address}')

# Main
if __name__ == "__main__":
    main()
