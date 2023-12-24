'''
@File    :   key_sys.py
@Time    :   2023/10/29 11:04:14
@Author  :   @灰尘疾客
@Site    :   https://www.gkcoll.xyz
@Desc    :   Main program.
'''

import time
import random
import os

from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify
from hashlib import md5

import vigenere as vg
import e

from base94 import b94, d94


def shuffle(s: str = ''.join([chr(i) for i in range(33, 127)])) -> str:
    '''
    Function:
        Disorganize a string.
    '''
    s = list(s)
    random.shuffle(s)
    return ''.join(s)


def str2int(s: str) -> int:
    '''
    Function: 
        Convert a string to an integer.

    Principle: 
        str -> bytes (encode by utf-8) -> int.
    '''
    # return int.from_bytes(s.encode('utf-8'), 'big')
    return int(hexlify(s.encode('utf-8')), 16)


def int2str(i: int) -> str:
    '''
    Function: 
        Convert an integer to a string.

    Principle: 
        int -> hex str -> bytes -> decode as utf-8.
    '''
    # Python does not support int to bytes conversion.
    hexstr = hex(i)[2:]
    # To convert hexadecimal to bytes, the length of hexstr must be an even number.
    hexstr = '0' * (len(hexstr) % 2) + hexstr
    # Or use bytes.fromhex().decode('utf-8')
    return unhexlify(hexstr).decode('utf-8')


def cut_string(string: str, length: int) -> list:
    '''
    Function:
        Cut the string into a list with equal length (specified) for all items.
    '''
    return [string[i:i + length] for i in range(0, len(string), length)]


def md5_digest(string: str) -> str:
    '''
    Function:
        Calculate the hexadecimal MD5 digest of the given string.
    '''
    return md5(string.encode('ASCII')).hexdigest()


class Key:

    def __init__(self,
                 step: int = '',
                 prec: int = '',
                 index: int = '',
                 chars: str = '',
                 password: str = ''):
        '''
        Class: Key
        
        Intro: The core of key system of Swift-Cavalier-Encrypt.

        Params: A Key object require 5 arguments (Optional).
            - step: Depth of constant e calculation.
            - prec: Precision of e's decimal part.
            - index: Position to get digit of e.
            - chars: Character set, consists of 94 printable characters in ASCII.
            - pwd_str: User-defined password, used for encrypt key and content.
        '''

        self.__step = step
        self.__prec = prec
        self.__index = index
        self.__chars = chars
        self.__ver = md5_digest(password)
        '''
        `pwd_str` plays the role of password, is a mandatory parameter, but will
        not be directly stored in plaintext in a Key object.

        During initialization, the Key object will directly call the
        `gen_key_string` method first to generate a key string, which avoids the
        need to pass parameters manually during subsequent accesses (referring 
        in the __str__ method called when accessing the printed Key object).
        '''

        if sum([bool(i) for i in [step, prec, index, chars, password]]) == 5:
            # Skip if bool value of one of the five arguments is False.
            self.key_string = self.gen_key_string(password)

    def save(self, filename: str = ''):
        content = '\n'.join(cut_string(self.key_string, 80))
        if not filename:
            filename = f'{int(time.time())}.k'
        else:
            if not filename.endswith('.k'):
                filename += '.k'

        with open(filename, 'a') as f:
            f.write(content)

    def gen_random(self):
        '''
        Method: Generate a new random Key objcet.

        Return: Key
        '''
        step = random.randint(1, 500)
        prec = random.randint(300, 2000)
        index = random.randint(prec - 200, prec)
        chars = shuffle()
        # The password is the middle ten digits of the chars.
        pwd_str = shuffle()[42:52]

        # Return the generated Key object and print its password in terminal.
        print(f'Please save your password:\n{pwd_str}')
        return Key(step, prec, index, chars, pwd_str)

    def gen_key_string(self, password: str, update: bool = True) -> str:
        '''
        Method: Generate a key string of the given Key object.
        
        Intro: This will normally be used for only one time of a Key object, 
        yes, the initialization. In other situation you need to call it, you may
        purpose to generate one for save (note that despite the generated value 
        is different to the key_string attribution of the Key object itself, the 
        recovery result return by Key().load() is same), but you need to enter 
        password manually.

        If you set `update` True, it will modify the value of self.key_string.
        '''
        if md5_digest(password) != self.__ver:
            raise Exception('Password Incorrect!')

        # Timestamp (Only integer part)
        t = int(time.time())

        # Set random seed:
        # Timestamp multiply the sum of every character's unicode number of
        # password string.
        random.seed(t * sum([ord(i) for i in password]))

        # Convert password string into number (later will use it for some
        # mathematical operations)
        pwd_int = str2int(password)

        # s: Include step, confuse by multiply timastamp and password number.
        s = self.__step * t * pwd_int

        # p: Include precision, like the previous variable seed, confuse by
        # multiply a number (sum of 10 random integer under the set seed).
        p = self.__prec * sum([random.randint(1, t) for _ in range(10)])

        # i: Include index, confuse by multiply s, p and pwd.
        i = s * p * self.__index * pwd_int

        # c: Include character set, the core of vigenere and base 94.
        # Stored as a integer.
        c = str2int(self.__chars)

        # Make a verification.
        # The value of code is the md5 digest of timestamp multiply pwd.
        code = int(md5_digest(f'{t * pwd_int}'), 16)

        # Join by a white space, pack all temporary data.
        package = ' '.join([b94(i) for i in [s, p, i, c, t, code]])
        vigenere = vg.encrypt(package, password)
        base64 = b64encode(vigenere.encode('utf-8'))

        key_str = str(base64)[2:-1]
        if update:
            self.key_string = key_str

        return key_str

    def __str__(self) -> str:
        return self.key_string

    def __repr__(self):
        return f"'{self.key_string}'"

    def load(self, x: str, password: str):
        '''
        Method: Recover a key string back to a Key object.

        Params:
            - x: A key string or the name of a key file.
            - password: The key to decrypt the key string.
        '''

        # If x is a file name, read its content.
        if x.endswith('.k'):
            if os.path.exists(x):
                with open(x, 'r') as f:
                    key_string = f.read().replace('\n', '').rstrip()
        else:
            key_string = x

        try:
            # Recover to package in one step.
            package = vg.decrypt(
                b64decode(key_string).decode('ASCII'), password).split(' ')
            pwd = str2int(password)
            # Recover the assignments, reduce mess index visit operations.
            s, p, i, c, t, v = [d94(i) for i in package]
        except:
            return None

        # Calculate a verification code according to the password again.
        code = int(md5_digest(f'{t * pwd}'), 16)

        # If code not equals to the code in the package, raise an exception.
        if code != v:
            raise Exception('Invalid Key or Password Incorrect!')

        # Set random seed, same as `gen` method.
        random.seed(t * sum([ord(i) for i in password]))

        # Recover parameters of Key.
        # For big number division, if you are sure that the operation result is
        # an integer, please use floor division instead of real division, and do
        # not use the `decimal.Decimal`. The former will get an inaccurate type,
        # which is float, and the latter may return a unexpected result: the
        # number is in scientific notation, the ending digits will be ignore.
        chars = int2str(c)
        step = int(s // t // pwd)
        prec = int(p // sum([random.randint(1, t) for _ in range(10)]))
        index = int(i // s // p // pwd)

        # Return a Key object.
        key_obj = Key(step, prec, index, chars, password)
        # The entered key string must be the key string of original Key object.
        key_obj.key_string = key_string

        return key_obj

    def encrypt(self, string: str, password: str) -> str:
        '''
        Method:
            Encryption function of Swift-Cavalier-Encrypt algorithm.

        Params:
            - string: Something to be encrypted.
            - password: Verify if user have right to execute this.
        '''
        if md5_digest(password) != self.__ver:
            raise Exception('Password Incorrect!')

        digit = int(e.get(self.__index, self.__step, self.__prec))
        coefficient = ((digit + 1)**(digit + 2))**(digit + 3)
        int_data = str2int(string)
        base_94_data = b94(int_data * coefficient, self.__chars)
        vg_key = b94((self.__step * self.__prec * self.__index)**2)

        return vg.encrypt(base_94_data, vg_key, self.__chars)

    def decrypt(self, string: str, password: str) -> str:
        '''
        Method:
            Decryption function of Swift-Cavalier-Encrypt algorithm.
        
        Params:
            - string: Something to be decrypted.
            - password: Verify if user have right to execute this.
        '''
        if md5_digest(password) != self.__ver:
            raise Exception('Password Incorrect!')

        try:
            vg_key = b94((self.__step * self.__prec * self.__index)**2)
            digit = int(e.get(self.__index, self.__step, self.__prec))
            coefficient = ((digit + 1)**(digit + 2))**(digit + 3)
            base_94_data = vg.decrypt(string, vg_key, self.__chars)
            try:
                int_data = int(d94(base_94_data, self.__chars) // coefficient)
            except:
                raise Exception(
                    'You may have passed in a non-ciphertext parameter.')
        except:
            raise Exception('Failed to decrypt.')
        return int2str(int_data)
