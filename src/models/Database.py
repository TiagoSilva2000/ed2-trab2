import hashlib
from typing import List
from models.User import User


class Database:
  users: List[User] = []
  dbSize: int
  currSize: int

  def __init__(self, dbSize: int):
    user: User = User("", "", "", "")
    for x in range (dbSize):
      self.users.append(user)
    self.dbSize = dbSize
    self.currSize = 0

  def hashTable(self, username: str, password: str)-> int:
    pos:int = 0
    string: str = username + password
    for i in range(len(string)):
      pos += (ord(string[i]) * (i + 1) * ((i * i + self.currSize) % self.dbSize))

    return pos % self.dbSize

  def collisionTreatment(self, idx:int):
    return (idx + (idx * self.dbSize)) % self.dbSize

  def cmpPassword(self, storagedPassword: str, loginPassword: str):
    tmpLogin = hashlib.sha512(loginPassword.encode('utf-8'))

    return storagedPassword == tmpLogin.hexdigest()

  def authenticate(self, username: str, password: str)-> bool:
    idx:int = self.hashTable(username, password)
    it:int = 0

    while self.users[idx].getUsername() != username and it != 20:
      self.collisionTreatment(idx)
      it += 1

    if it == 20:
      return 0

    if self.cmpPassword(self.users[idx].getPassword(), password):
      return 1

  def removeUser(self, username: str, password: str)-> bool:
    idx:int = self.hashTable(username, password)
    it:int = 0

    while self.users[idx].getUsername() != username and it != 20:
      idx = self.collisionTreatment(idx)
      it += 1

    if it == 20:
      return False
    self.users[idx] = User("", "", "", "")
    return True

  def registerUser(self, newUser: User)-> bool:
    idx:int = self.hashTable(newUser.getUsername(), newUser.getPassword())
    it:int = 0

    while self.users[idx].getUsername() != "" and it != 20:
      idx = self.collisionTreatment(idx)
      it += 1

    if it == 20:
      print("There's something wrong with your hash table, boi")
      return False

    newUser.setPassword(newUser.hashPassword())
    self.users[idx] = newUser
    return True

  def createUser(self)-> bool:
    username:str = input("Insira seu nome de usuário: ")
    email:str = input("Insira o seu e-mail: ")
    password:str = input("Insira a sua senha: ")
    user:User = User(username, password, email, "default")

    return self.registerUser(user)

  def tryToAuthenticate(self)-> bool:
    username:str = input("Insira seu nome de usuário: ")
    password:str = input("Insira a sua senha: ")
    code:bool = self.authenticate(username, password)

    if code: print("found it!")
    else: print("these credentials don't match with an specific user")

    return True

  def deleteUser(self)-> bool:
    username:str = input("Insira seu nome de usuário: ")
    password:str = input("Insira a sua senha: ")
    code:bool = self.removeUser(username, password)

    if code:
      print("user deleted!")
      self.currSize -= 1
    else: print("the user can't be deleted")


    return True

  def checkAllUsers(self)-> bool:
    for i in range(len(self.users)):
      print(f"{i} - {self.users[i].getUsername()} - {self.users[i].getEmail()}")