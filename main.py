class Human:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def say_hello(self):
        print("Hello, I'm a human")

class Player(Human):
    def __init__(self, name):
        super().__init__(name)
    
class Fan(Human):
    def __init__(self, name):
        super().__init__(name)
    def say_hello(self):
        print("Hello, I'm a fan")

fan = Fan("John")
fan.say_hello()