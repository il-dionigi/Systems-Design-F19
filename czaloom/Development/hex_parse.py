s = "cfde68656c6c6f20776f726c642130"

def charhex_to_int(c):
	if c == 'A' or c == 'a':
		return 10
	elif c == 'B' or c == 'b':
		return 11
	elif c == 'C' or c == 'c':
		return 12
	elif c == 'D' or c == 'd':
		return 13
	elif c == 'E' or c == 'e':
		return 14
	elif c == 'F' or c == 'f':
		return 15
	else:
		return int(c)

def get_letter(segment):
	ascii_ = 16*charhex_to_int(segment[0]) + charhex_to_int(segment[1])
	return chr(ascii_)
def get_number(segment):
	return 16*charhex_to_int(segment[0]) + charhex_to_int(segment[1])

def get_ID(segment):
	return [get_number(segment[0:2]),get_number(segment[2:4])]
def get_Message(segment):
	MSG = ""
	for i in range(4,30,2):
		MSG = MSG + get_letter(segment[i:i+2])
	return MSG

ID = get_ID(s)
MSG = get_Message(s)
	
print(ID)
print(MSG)