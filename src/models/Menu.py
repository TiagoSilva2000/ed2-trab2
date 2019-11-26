class Menu:

  def __init__(self):
    pass

  def show(self)-> int:
    code:int = -1

    while code < 0 or code > 4:
      print("1 - Register an user\n" +
            "2 - Search for an user\n" +
            "3 - Remove an user\n" +
            "4 - Show all users\n"
            "0 - Exit\n")
      code = int(input("Select your option: "))
      if code < 0 or code > 4:
        print("Incorrect code!\n")

    return code

  def fIndexer(self, fn1, fn2, fn3, fn4)-> int:
    code:int = self.show()

    if code == 1: fn1()
    elif code == 2: fn2()
    elif code == 3: fn3()
    elif code == 4: fn4()

    return code