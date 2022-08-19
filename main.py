from cryptography.fernet import Fernet
#key= Fernet.generate_key()
#with open("mykey.key",'wb') as mykey:
#   mykey.write(key)
with open('mykey.key','rb') as mykey:
    key=mykey.read()
print(key)
f = Fernet(key)
with open('grades.csv','rb') as original_file:
    original=original_file.read()

encrypted=f.encrypt(original)
with open('enc_grades.csv','wb') as encrypted_file:
    encrypted_file.write(encrypted)

with open('enc_grades.csv','rb') as enc_file:
    enc=enc_file.read()
decrypted=f.decrypt(enc)
with open('dec_grades.csv','wb') as decrypted_file:
    decrypted_file.write(decrypted)