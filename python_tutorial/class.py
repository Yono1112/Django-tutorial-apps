class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")


# インスタンスを作成
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

# メンバ変数を出力
person1.display_info()
person2.display_info()
# f-string
print(f"person1.age: {person1.age}")
# format()
print("person1.name: {}".format(person1.name))
# 文字列の連結
print("person2.age: " + str(person2.age))
print("person2.name: " + person2.name)

# データ属性は標準でprivateではないから、直接アクセスできてしまう
person1.age = 50
person1.name = "Michel"
person1.display_info()

# データ属性はクラス内に存在しなくても、新たに作成できる
person1.isVerified = True
print(f"person1.isVerified: {person1.isVerified}")
person1.isVerified = False
print(f"person1.isVerified: {person1.isVerified}")
