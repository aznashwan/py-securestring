from ctypes import *
from ctypes.wintypes import DWORD

protectdata = windll.crypt32.CryptProtectData
unprotectdata = windll.crypt32.CryptUnprotectData
localfree = windll.kernel32.LocalFree
copy = cdll.msvcrt.memcpy

class blob(Structure):
	_fields_ = [("length", DWORD), ("data", POINTER(c_char))]

def getblobdata(b):
	length = int(b.length)
	
	fetched = c_buffer(length)
	copy(fetched, b.data, length)

	localfree(self.b)
	return fetched.raw

def freeblobdata(b):
	localfree(b.data)


def encrypt(input):
	data = c_buffer(input, len(input))
	inputBlob = blob(len(input), data)
	entropyBlob = blob()
	outputBlob = blob()
	dwflags = 0x01

	res = protectdata(byref(inputBlob), u"", byref(entropyBlob), None, None, dwflags, byref(outputBlob))
	if res == 0:
		freeblobdata(outputBlob)
		raise Exception("Failed to encrypt " + input)
	else:
		return getblobdata(outputBlob)

def decrypt(input):
	data = c_buffer(input, len(input))
	inputBlob = blob(len(input), data)
	entropyBlob = blob()
	outputBlob = blob()
	dwflags = 0x01

	res = unprotectdata(byref(inputBlob), u"", byref(entropyBlob), None, None, dwflags, byref(outputBlob))
	if res == 0:
		freeblobdata(outputBlob)
		raise Exception("Failed to decrypt " + input)
	else:
		return getblobdata(outputBlob)
