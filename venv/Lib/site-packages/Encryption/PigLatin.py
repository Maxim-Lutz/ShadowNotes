def PigEncode(message):
  word = ""
  data = []
  out = []
  message = message + " "
  for char in message:
    if char == " ":
      data.append(word)
      word = ""
    else:
      word += char
  for word in data:
    nword = ""
    for char in range(len(list(word))+1):
      if char == 0:
        start = list(word)[char]
      elif char == len(list(word)):
        nword += start + "ay"
      else:
        nword += list(word)[char]
    out.append(nword)
  nout = ""
  for word in out:
    nout += word + " "
  return nout

def PigDecode(message):
  word = ""
  data = []
  out = []
  message = message + " "
  for char in message:
    if char == " ":
      data.append(word)
      word = ""
    else:
      word += char
  for word in data:
    nword = ""
    word = word[:len(list(word))-2]
    for char in range(len(list(word))-1):
      if char == 0:
        nword += list(word)[len(list(word))-1]
      nword += list(word)[char]
    out.append(nword)
  nout = ""
  for word in out:
    nout += word + " "
  return nout