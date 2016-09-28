import hashlib

data = 'This a md5 test!'
hash_md5 = hashlib.md5(data)
md5_val = hash_md5.hexdigest()
print md5_val, len(md5_val)

sha1 = hashlib.sha1()
sha1.update(data)
sha1_val = sha1.hexdigest()
print sha1_val, len(sha1_val)
print dir(sha1)
