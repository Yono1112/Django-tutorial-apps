class Person:
    """This is documentation string"""
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")
        # selfで他のメソッドを呼び出せる
        # self.display_name()
        # self.display_age()

    def display_name(self):
        print(f"Name: {self.name}")

    def display_age(self):
        print(f"Age: {self.age}")
