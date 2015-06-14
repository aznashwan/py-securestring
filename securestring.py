# Copyright 2015, Nashwan Azhari.
# Licensed under the GPLv2, see LICENSE file for details.

"""
A pure Python implementation of the functionality of the ConvertTo-SecureString
and ConvertFrom-SecureString PoweShell commandlets.

Usage example:
from securestring import encrypt, decrypt

if __name__ == "__main__":
    str = "My horse is amazing"

    # encryption:
    try:
        enc = encrypt(str)
        print("The encryption of %s is: %s" % (str, enc))
    except Exception as e:
        print(e)

    # decryption:
    try:
        dec = decrypt(enc)
        print("The decryption of the above is: %s" % dec)
    except Exception as e:
        print(e)

    # checking of operation symmetry:
    print("Encryption and decryption are symmetrical: %r", dec == str)

    # decrypting powershell input:
    psenc = "<your output of ConvertFrom-SecureString>"
    try:
        dec = decrypt(psenc)
        print("Decryption from ConvertFrom-SecureString's input: %s" % dec)
    except Exception as e:
        print(e)

"""

from codecs import encode
from codecs import decode

from blob import Blob

from ctypes import byref
from ctypes import create_string_buffer
from ctypes import windll

protect_data = windll.crypt32.CryptProtectData
unprotect_data = windll.crypt32.CryptUnprotectData


def encrypt(input):
    """Encrypts the given string following the same syscalls as done by
    ConvertFrom-SecureString.

    Arguments:
    input -- an input string.

    Returns:
    output -- string containing the output of the encryption in hexadecimal.
    """
    # CryptProtectData takes UTF-16; so we must convert the data here:
    encoded = input.encode("utf-16")
    data = create_string_buffer(encoded, len(encoded))

    # create our various Blobs:
    input_blob = Blob(len(encoded), data)
    output_blob = Blob()
    flag = 0x01

    # call CryptProtectData:
    res = protect_data(byref(input_blob), u"", byref(Blob()), None,
                       None, flag, byref(output_blob))
    input_blob.free_blob()

    # check return code:
    if res == 0:
        output_blob.free_blob()
        raise Exception("Failed to encrypt: %s" % input)
    else:
        raw = output_blob.get_data()
        output_blob.free_blob()

        # encode the resulting bytes into hexadecimal before returning:
        hex = encode(raw, "hex")
        return decode(hex, "utf-8").upper()


def decrypt(input):
    """Decrypts the given hexadecimally-encoded string in conformity
    with CryptUnprotectData.

    Arguments:
    input -- the encrypted input string in hexadecimal format.

    Returns:
    output -- string containing the output of decryption.
    """
    # de-hex the input:
    rawinput = decode(input, "hex")
    data = create_string_buffer(rawinput, len(rawinput))

    # create out various Blobs:
    input_blob = Blob(len(rawinput), data)
    output_blob = Blob()
    dwflags = 0x01

    # call CryptUnprotectData:
    res = unprotect_data(byref(input_blob), u"", byref(Blob()), None,
                         None, dwflags, byref(output_blob))
    input_blob.free_blob()

    # check return code:
    if res == 0:
        output_blob.free_blob()
        raise Exception("Failed to decrypt: %s" + input)
    else:
        raw = output_blob.get_data()
        output_blob.free_blob()

        # decode the resulting data from UTF-16:
        return decode(raw, "utf-16")
