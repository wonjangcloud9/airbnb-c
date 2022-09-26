class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        print("Woof!")
    
    def __str__(self):
        return self.name

jia= Dog("Jia")
print(dir(jia))