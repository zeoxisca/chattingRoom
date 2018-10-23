import hashlib
m2 = hashlib.md5()
m2.update('123'.encode('utf-8'))
h = m2.hexdigest()
print(h)