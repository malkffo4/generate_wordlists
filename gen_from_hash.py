#!/usr/bin/env python3

import hashlib
import random
import string

import hmac

def derive_password_secure(master_secret, domain, length=24):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    # Используем HMAC-SHA256 как основу
    key = bytes.fromhex(master_secret)
    msg = domain.encode()
    
    result = ""
    counter = 0
    while len(result) < length:
        # Создаем уникальный хеш для каждой итерации, если нужно больше символов
        attempt = hmac.new(key, msg + str(counter).encode(), hashlib.sha256).digest()
        for byte in attempt:
            if len(result) < length:
                # Используем байт хеша напрямую для выбора индекса
                result += chars[byte % len(chars)]
        counter += 1
    return result

def generate_password_from_hash(hash_str:str, length:int) -> str:
    r'''generate password from hash
    '''
    # alpha  = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'''
    # number = '''0123456789'''
    # punct  = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''

    # Convert hash to bytes
    try:
        seed_bytes = bytes.fromhex(hash_str)
    except ValueError:
        print('String is NOT hash')
        return ''
    
    # Use the hash of these bytes as a source of randomness
    try:
        hexdig = hashlib.sha256(seed_bytes).hexdigest()
    except Exception as err:
        print(err)
        return ''
    
    seed = int(hexdig, 16)
    rng = random.Random(seed)

    # Define valid characters
    # chars = alpha + number + punct
    chars = string.ascii_letters + string.digits + string.punctuation

    # Generating a password
    password = ''.join(rng.choice(chars) for _ in range(length))
    return password

def derive_password(master_secret: str, domain: str, length: int = 24) -> str:
    import hashlib, hmac

    key = bytes.fromhex(master_secret)
    msg = domain.encode()
    digest = hmac.new(key, msg, hashlib.sha256).digest()

    chars = string.ascii_letters + string.digits + string.punctuation
    rng = random.Random(int.from_bytes(digest, 'big'))

    return ''.join(rng.choice(chars) for _ in range(length))

def get_from_input() -> (str):
    '''
    1. getting hash from input
    2. getting length password from input
    3. return
    '''

    raw_pass_str = input('Enter your password: ')
    lp_str_tmp = input('length password: ')

    raw_pass_str = bytes(raw_pass_str, encoding='utf-8')
    hash_str = hashlib.sha256(raw_pass_str).hexdigest()
    # hash_str = raw_pass_str

    # Check, if nothing is entered, then set default 0
    try:
        lp_tmp = int(lp_str_tmp if lp_str_tmp != '' else '0')
    except ValueError:
        print(f'Error Value \'{lp_str_tmp}\'. Need a number.')
        exit(1)

    # set the default length to 24 if 0 is entered
    length_password = lp_tmp if lp_tmp != 0 else 24

    return hash_str, length_password

def main():
    hash, length_password = get_from_input()
    domain = input('input domain:')

    password_1 = generate_password_from_hash(hash, length=length_password)

    password_2 = derive_password(master_secret=hash, domain=domain, length=length_password)
    
    password_3 = derive_password_secure(hash, domain, length_password)

    print('---' * 7)
    if password_1 != '':
        print(password_1)

    if password_2 != '':
        print(password_2)
    
    if password_3 != '':
        print(password_3)

if __name__ == '__main__':
    main()
