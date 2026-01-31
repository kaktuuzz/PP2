print(10 > 5)  #True
print(10 == 9) #False
print(10 < 0)  #False

class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))