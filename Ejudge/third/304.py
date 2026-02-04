class StringHandler:
    def __init__(self):
        self.text = ""

    def getString(self):
        self.text = input()

    def printString(self):
        print(self.text.upper())


handler = StringHandler()
handler.getString()
handler.printString()
