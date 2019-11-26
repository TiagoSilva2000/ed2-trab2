import sys, hashlib, copy
sys.path.insert(1, '/home/ttiago/codes/college/ed2/trab2/src')
from typing import List
from models.User import User

class Database:
  users: List[User] = []
  dbSize: int
  currSize: int
  colCounter:int
  itMax:int
  opCounter:int

  def __init__(self, dbSize: int):
    user: User = User("", "", "", "")
    for x in range (dbSize):
      self.users.append(user)
    self.dbSize = dbSize
    self.currSize = 0
    self.colCounter = 0
    self.opCounter = 0
    self.itMax = dbSize * 5

  def logInfo(self):
    value:float = self.currSize / self.dbSize
    colStr: str = str(f"Access: {self.colCounter}\n")

    return print("Occupation rate: {0:.2f}. "
                  .format(value) + colStr)

  def checkAllUsers(self)-> bool:
    for i in range(len(self.users)):
      print(f"{i} - {self.users[i].getUsername()} - {self.users[i].getEmail()}")
    print("\n")

  def addAccess(self, adder:int)-> None:
    self.colCounter += adder

  def getAccess(self): return self.colCounter

  def addOperation(self, adder:int)-> None:
    self.opCounter += adder

  def getOperations(self): return self.opCounter

  def hashTable(self, username: str, password: str)-> int:
    pos:int = 0
    string: str = username + password
    for i in range(len(string)):
      pos += (ord(string[i]) * (i + 1) * ((i * i + self.dbSize) % self.dbSize))

    return pos % self.dbSize

  def collisionTreatment(self, idx:int):
    self.addAccess(1)

    return self.hashTable(str(idx), str(idx))

  def cmpPassword(self, storagedPassword: str, loginPassword: str):
    tmpLogin = hashlib.sha512(loginPassword.encode('utf-8'))

    return storagedPassword == tmpLogin.hexdigest()

  def searchUser(self, username: str, password: str, wantedString:str)-> int:
    idx:int = self.hashTable(username, password)
    it:int = 0
    iniIdx:int = copy.copy(idx)
    self.addOperation(1)
    self.addAccess(1)

    while self.users[idx].getUsername() != wantedString and it != self.itMax:
      idx = self.collisionTreatment(idx)
      it += 1

      if iniIdx == idx:
        idx = -1
        print("The iteration came back to the same point where it started")
        break

    print(f"\nNúmero de colisões durante a procura: {it}")
    return idx, it

  def registerUser(self, newUser: User)-> bool:
    idx, it = self.searchUser(newUser.getUsername(),
                              newUser.getPassword(),
                              wantedString="")

    if it == self.itMax:
      print("There's something wrong with your hash table, boi")
      return False

    if self.users[idx].getUsername() != "":
      print("ERROR!")
      return False

    newUser.setPassword(newUser.hashPassword())
    self.users[idx] = newUser
    self.currSize += 1

    return True

  def createUser(self)-> bool:
    if self.currSize >= self.dbSize * 2/3:
      return print("Impossível inserir mais usuários nessa tabela")

    username:str = input("Insira seu nome de usuário: ")
    email:str = input("Insira o seu e-mail: ")
    password:str = input("Insira a sua senha: ")
    typo:str = input("Insira o seu tipo de usuário: ")
    user:User = User(username, password, email, typo)

    self.registerUser(user)
    return self.logInfo()

  def authenticate(self, username: str, password: str)-> bool:
    idx, it = self.searchUser(username, password, wantedString=username)

    if it == self.itMax:
      return None

    if self.cmpPassword(self.users[idx].getPassword(), password):
      return self.users[idx]
    return None

  def tryToAuthenticate(self)-> bool:
    username:str = input("Insert your username: ")
    password:str = input("Insert your password: ")
    user:User = self.authenticate(username, password)

    if user != None:
      print("Found it! " + " 1) Username: " + user.getUsername() +
            " 2) Email: " + user.getEmail())
    else:
      print("these credentials don't match with an specific user")

    return True

  def removeUser(self, username: str, password: str)-> bool:
    idx, it = self.searchUser(username, password, wantedString=username)

    if it == self.itMax:
      return False

    self.users[idx] = User("", "", "", "")
    return True

  def deleteUser(self)-> bool:
    username:str = input("Insert your username: ")
    password:str = input("Insert your password: ")
    code:bool = self.removeUser(username, password)

    if code:
      print("User deleted!\n")
      self.currSize -= 1
    else:
      print("The user can't be deleted\n")

    return True