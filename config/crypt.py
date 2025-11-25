import bcrypt

def criptografar(password):
   password_bytes = password.encode('utf-8')
   salt = bcrypt.gensalt()
   hashed = bcrypt.hashpw(password_bytes, salt)
   return hashed

def checar_password(password, hashed):
   password_bytes = password.encode('utf-8')
   return bcrypt.checkpw(password_bytes, hashed)