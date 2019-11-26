import sys, os, copy
sys.path.insert(1, '/home/ttiago/codes/college/ed2/trab2')

from models.Database import Database
from models.Menu import Menu
from models.User import User

def isPrime(number:int)->bool:
  for i in range(2, number):
    if number % i == 0:
      return False
  return True

def getNextPrime(dbSize:int):
  number:int = copy.copy(dbSize)
  while (not isPrime(number)):
    number += 1

  return number

ratio:float = 0
actionCode: int = -1
dbSize: int = int(input("insira o tamanho do seu banco de dados: "))
dbSize += dbSize // 2
dbSize = getNextPrime(dbSize)
db: Database = Database(dbSize)
menu: Menu = Menu()

while actionCode != 0:
  actionCode = menu.fIndexer(db.createUser, db.tryToAuthenticate,
                            db.deleteUser, db.checkAllUsers)
  if actionCode != 0:
    input("")
  os.system('clear')

if db.getOperations() != 0:
  ratio = db.getAccess() / db.getOperations()

print("Operação Finalizada! Média de acessos por operação igual a: {0:.2f}"
      .format(ratio))