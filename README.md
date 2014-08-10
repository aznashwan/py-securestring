py-securestring
===============

A python implementation of Windows'SecureString's


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

* Additional notes:
  1. SecureStrings in Windows, in it of themselves, are nothing more than plain strings stored in memory which is completely locked.
  2. ConvertFrom-SecureString uses the DAPI encryption technique to yield a hexadecimal-encoded string which encrypts the data from the locked memory.
  3. DAPI encrypts with the current user session in mind; therefore, decrypting ConvertFrom-SecureString's output can NOT be done by a different user than that which did the encryption in the first place, be it by the PowerShell commandlets or the methods in this module !!!
  4. Because of various user session parameters being used in the encryption process, both ConvertFrom-SecureString and this module's encrypt() function yield varying output at each call, thus comparing the outputs of two different encryptions, albeit of the same input, will fail.


Usage example:

```python
import securestring

if __name__ == "__main__":
	str = "My horse is amazing"

	# encryption
	try:
		enc = securestring.encrypt(str)
		print "The encryption of %s is:" % str
		print enc
	except Exception as e:
		print e

	# decryption
	try:
		dec = securestring.decrypt(enc)
		print "The decryption of the above is: " + dec
	except Exception as e:
		print e

	# checking of operation symmetry
	print "The output of decryption equals the input of encryption: ", dec == str

	# decrypting powershell input
	# NOTE: encryption is based on the current user session; please supply
	# your own input obtained from the above commands here:
	psenc = "01000000d08c9ddf0115d1118c7a00c04fc297eb01000000b1574fbfe3922549af0514935987635c00000000020000000000106600000001000020000000f924faefd299bb0c9bae16d444b901459587d002f0c5211071a90f555fe3d805000000000e8000000002000020000000c0bf9fc4ddcfdc52805ddb7706f613136c4680ba4e6f459ca6b954fe5d5689bc30000000493d1cb2b97d622dc7079b1d4be12d30ffcd27cd3d6d1ea9f5dbc490da66bfdff87c71ed95fc1e30cf27fa63e1afd2a740000000822707fb1eec2da45aa4743bde876b2cdac7f0482304400942204831597cee81f8aa18127312f6934e0022c3bba2902d5edde5b420806a43de76d2ffbfea9c22"
	try:
		dec = securestring.decrypt(psenc)
		print "Decryption from ConvertFrom-SecureString's input: " + dec
	except Exception as e:
		print e
```


* Related documentation:
  * [Crypt32.dll::CryptProtectData](http://msdn.microsoft.com/en-us/library/windows/desktop/aa380261%28v=vs.85%29.aspx)
  * [Crypt32.dll::CryptUnprotectData](http://msdn.microsoft.com/en-us/library/windows/desktop/aa380882%28v=vs.85%29.aspx)
  * [Kernel32.dll::LocalFree](http://msdn.microsoft.com/en-us/library/windows/desktop/aa366730%28v=vs.85%29.aspx)
  * [System.Security.Cryptography.CAPI::CRYPTOAPI_BLOB](http://msdn.microsoft.com/en-us/library/windows/desktop/aa381414%28v=vs.85%29.aspx)

* PS: you may also find the go implementation [here](https://github.com/aznashwan/go-securestring)
