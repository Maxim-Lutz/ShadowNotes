def CaesarEncode(data,shift):
  out = ""
  for char in list(data):
    if not char.isalpha():
      out += char
    else:
      out += chr((ord(char) - 97 + shift) % 26 + 97)
  return out

def CaesarDecode(data, shift):
  out = ""
  for char in list(data):
    if not char.isalpha():
      out += char
    else:
      out += chr((ord(char)- 97 - shift) % 26 + 97)
  return out