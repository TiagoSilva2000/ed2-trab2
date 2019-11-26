import hashlib


class User:
  username: str
  password: str
  email: str
  typo: str

  def __init__(self, username, password, email, typo):
    self.username = username
    self.password = password
    self.email = email
    self.typo = typo

  def getUsername(self)-> str: return self.username

  def getEmail(self)-> str: return self.email

  def getPassword(self)-> str: return self.password

  def getTypo(self)->str: return self.typo

  def hashPassword(self):
    hashedPassword = hashlib.sha512(self.password.encode('utf-8'))

    return hashedPassword.hexdigest()

  def setPassword(self, password: str): self.password = password
