import random
from CaesarCipher import CaesarEncode, CaesarDecode

def VigenereEncode(message):
  out = ""
  code = ""
  for char in list(message):
    if char.isalpha():
      shift = random.randint(0,25)
      out += CaesarEncode(char, shift)
      code += str(shift)
    else:
      code += " "
      out += char
  return (out, code)

def VigenereDecode(message, shift):
  out = ""
  data = list(message)
  data.append(" ")
  shift = list(shift)
  shift.append(" ")
  nshift = []
  num = ""
  for char in shift:
    if char != " ":
      num += char
    else:
      nshift.append(num)
      num = ""
  ndata = []
  word = ""
  for char in data:
    if char != " ":
      word += char
    else:
      ndata.append(word)
      word = ""
  for char in ndata:
    out += CaesarDecode(char, int(nshift[ndata.index(char)]))
  return out