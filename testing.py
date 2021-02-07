import hashlib
phrase = "Nobody inspects the spammish repetition"
hash1 = hashlib.sha224(phrase.encode('utf8')).hexdigest()
hash2 = hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()
hash3 = hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()

if hash1 == hash2:
   print('works')
if hash2 == hash3:
   print("it's transative")