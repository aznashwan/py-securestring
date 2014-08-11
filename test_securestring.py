from subprocess import check_output
from securestring import encrypt, decrypt

testinputs = [
	"Simple",
	"A longer string",
	"A!string%with(a4239lot#of$&*special@characters{[]})",
	"Quite a very much longer string meant to push the envelope",
	"fsdafsgdfgdfgdfgdfgsdfgdgdfgdmmghnh kv dfv dj fkvjjenrwenvfvvslfvnsljfvnlsfvlnsfjlvnssdwoewivdsvmxxvsdvsdv",
]

# tests whether encryption and decryption are symmetrical operations
def test_encryption_decryption_symmetry():
	for input in testinputs:
		try:
			assert decrypt(encrypt(input)) == input
		except:
			assert False


def runpscommand(command):
	try:
		return check_output(["powershell.exe", "-NoProfile",
                    "-NonInteractive", command]).replace("\r\n", "")
	except:
		raise Exception("System error has occured.")

# tests whether decrypt() can handle input directly from ConvertFrom-SecureString
def test_decrypt_from_CFSS():
	for input in testinputs:
		try:
			psenc = runpscommand("ConvertTo-SecureString \"%s\" -AsPlainText -Force | ConvertFrom-SecureString" % input)
			assert decrypt(psenc) == input
		except:
			assert False

# tests whether the output of encrypt() is compatible with ConvertTo-SecureString
def test_convert_encrypted_to_securestring():
	for input in testinputs:
		try:
			enc = encrypt(input)
			psres = runpscommand("\"%s\" | ConvertTo-SecureString" % enc)
			assert psres == "System.Security.SecureString"
		except:
			assert False

