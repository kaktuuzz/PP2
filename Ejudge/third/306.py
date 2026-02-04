class Shape():
    def area(self):
        return 0
    
class Rectangle():
    def __init__(self, len, wid):
        self.len = len
        self.wid = wid

    def area(self):
        return self.len * self.wid
    
l, w = map(int, input().split())
rect = Rectangle(l, w)
print(rect.area())