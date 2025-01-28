import bcrypt
from passlib.context import CryptContext




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)


def to_bits(*args):
  return tuple(s.encode('utf-8') for s in args)

def to_str(*args):
  return tuple(b.decode('utf-8') for b in args)

def get_password_hash(pwd: str) -> str:
  salt = bcrypt.gensalt()
  return to_str(bcrypt.hashpw(*to_bits(pwd), salt))[0]

def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
  return bcrypt.checkpw(*to_bits(plain_pwd, hashed_pwd))