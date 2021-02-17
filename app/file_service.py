import random


def save_file(data: bytes, extension: str):
    name = get_random_string(10) + "." + extension
    file = open(name, "wb")
    file.write(data)
    file.close()
    return name


# TODO(any): implemant save file in cloud service

def get_random_string(length):
    # put your letters in the following string
    sample_letters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return result_str
