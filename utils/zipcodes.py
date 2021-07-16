import re

def zipcode_in_address(formated_address):
    '''Returns the zipcode storage in the formated address by
    using Regex'''
    pattern = re.compile(r'[\d]{5}')
    zipcode = re.findall(pattern, formated_address)[0]

    return zipcode

