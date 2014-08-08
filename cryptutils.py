from ctypes import *
from ctypes.wintypes import DWORD

protectdata = windll.crypt32.CryptProtectData
unprotectdata = windll.crypt32.CryptUnprotectData
localfree = windll.kernel32.LocalFree
copy = cdll.msvcrt.memcpy

# the basic blob structure we will be using for calling
# the above System functions
class blob(Structure):
	_fields_ = [("length", DWORD), ("data", POINTER(c_char))]

# this function will fetch all the gata from a given blob
def getblobdata(b):
	length = int(b.length)
	
	fetched = c_buffer(length)
	copy(fetched, b.data, length)

	freeblobdata(b)
	return fetched.raw

# this function will free the memory of the data field from a given blob
def freeblobdata(b):
	localfree(b.data)


# this function will encrypt a given string in accordance with the 
# ConvertFrom-SecureString commandlet and return the hex representation
def encrypt(input):
	# for some odd reason the cmdlet's calls encrypt the data with interwoven
	# nulls, for which we will account as follows:
	nulled = ""
	for char in input:
		nulled = nulled + char + "\x00"

	data = c_buffer(nulled, len(nulled))

	inputBlob = blob(len(nulled), data)
	entropyBlob = blob()
	outputBlob = blob()
	flag = 0x01

	res = protectdata(byref(inputBlob), u"", byref(entropyBlob), None, 
		None, flag, byref(outputBlob))
	if res == 0:
		freeblobdata(outputBlob)
		raise Exception("Failed to encrypt " + input)
	else:
		return getblobdata(outputBlob).encode("hex")

# this function will decrypt the output of ConvertFrom-SecureString
# and return the original string which was encrypted
def decrypt(input):
	rawinput = input.decode("hex")
	data = c_buffer(rawinput, len(rawinput))

	inputBlob = blob(len(rawinput), data)
	entropyBlob = blob()
	outputBlob = blob()
	dwflags = 0x01

	res = unprotectdata(byref(inputBlob), u"", byref(entropyBlob), None, 
		None, dwflags, byref(outputBlob))
	if res == 0:
		freeblobdata(outputBlob)
		raise Exception("Failed to decrypt " + input)
	else:
		clean = ""
		# as mentioned, the commandlets work with data with interwoven nulls,
		# for which we must account for by removing them at the end:
		for char in getblobdata(outputBlob):
			if char != "\x00":
				clean = clean + char
		return clean
