import sys, os
sys.path.insert(1, '/home/ttiago/codes/college/ed2/trab2')

from models.Database import Database
from models.Menu import Menu
from models.User import User

db: Database = Database(13)
menu: Menu = Menu()
actionCode: int = -1


while actionCode != 0:
  actionCode = menu.fIndexer(db.createUser, db.tryToAuthenticate,
                            db.deleteUser, db.checkAllUsers)
  # os.system('clear')