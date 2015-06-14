py-securestring
===============

A python implementation of Windows'SecureString's

#### Use cases:

```
PS > $ss1 = ConvertTo-SecureString "Your string" -AsPlainText -Force
PS > $ss1
System.Security.SecureString
PS > ConvertFrom-SecureString $ss1
# The above yields the encrypted string in hexadecimal form which may be passed
# to this module's decrypt() function in order to get the original string.

# Conversely, calling the encrypt() function will yield an output
# which is perfectly compatible with ConvertTo-SecureString:
PS > "Output of encrypt()" | ConvertTo-SecureString | $ss2
PS > $ss2
System.Security.SecureString
```

#### Usage example:

```python
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
```

#### Notes:
  1. SecureStrings in Windows, in it of themselves, are nothing more than plain strings stored in memory which is completely locked.
  2. ConvertFrom-SecureString uses the DAPI encryption technique to yield a hexadecimal-encoded string which encrypts the data from the locked memory.
  3. DAPI encrypts with the current user session in mind; therefore, decrypting ConvertFrom-SecureString's output can NOT be done by a different user than that which did the encryption in the first place, be it by the PowerShell commandlets or the methods in this module !!!
  4. Because of various user session parameters being used in the encryption process, both ConvertFrom-SecureString and this module's encrypt() function yield varying output at each call, thus comparing the outputs of two different encryptions, albeit of the same input, will fail.

#### Crypt32 documentation:
  * [Crypt32.dll::CryptProtectData](http://msdn.microsoft.com/en-us/library/windows/desktop/aa380261%28v=vs.85%29.aspx)
  * [Crypt32.dll::CryptUnprotectData](http://msdn.microsoft.com/en-us/library/windows/desktop/aa380882%28v=vs.85%29.aspx)
  * [Kernel32.dll::LocalFree](http://msdn.microsoft.com/en-us/library/windows/desktop/aa366730%28v=vs.85%29.aspx)
  * [System.Security.Cryptography.CAPI::CRYPTOAPI_BLOB](http://msdn.microsoft.com/en-us/library/windows/desktop/aa381414%28v=vs.85%29.aspx)


