# Copyright 2015, Nashwan Azhari.
# Licensed under the GPLv2, see LICENSE file for details.

from codecs import decode
from subprocess import check_output

from securestring import encrypt, decrypt

testinputs = [
    "Simple",
    "A longer string",
    "A!string%with(a4239lot#of$&*special@characters{[]})",
    "Quite a very much longer string meant to push the envelope",
    "fsdafsgdfgdfgdfgdfgsdfgdgdfgdmmghnh kv dfv dj fkvjjenrwenvfvvslfvnsljfvnlsfvlnsfjlvnssdwoewivdsvmxxvsdvsdv",
]


def test_encryption_decryption_symmetry():
    """Tests whether encryption and decryption is symmetrical."""
    for input in testinputs:
        try:
            assert decrypt(encrypt(input)) == input
        except Exception as e:
            print(e)
            assert False


def runpscommand(command):
    """Helper function which runs the given command with PowerShell
    and returns the output.
    """
    try:
        # NOTE: trailing newline characters must be removed here:
        return check_output(["powershell.exe", "-NoProfile",
                             "-NonInteractive", command]).replace(b"\r\n", b"")
    except:
        raise Exception("System error has occured.")


def test_decrypt_from_CFSS():
    """Tests whether decrypt() is able to decrypt the
    output of ConvertFrom-SecureString."""
    for input in testinputs:
        try:
            psenc = runpscommand("ConvertTo-SecureString \"%s\" -AsPlainText -Force | ConvertFrom-SecureString" % input)
            assert decrypt(psenc) == input
        except Exception as e:
            print(e)
            assert False


def test_convert_encrypted_to_securestring():
    """Tests whether the output of encrypt() is compatible with
    PowerShell's SecureStrings by feeding its output to ConvertTo-SecureString."""
    for input in testinputs:
        try:
            enc = encrypt(input)
            psres = runpscommand("\"%s\" | ConvertTo-SecureString" % enc)
            assert decode(psres, "utf-8") == "System.Security.SecureString"
        except Exception as e:
            print(e)
            assert False
