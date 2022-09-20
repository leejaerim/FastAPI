from mongoengine import Document, StringField,IntField,ListField

class Employee(Document):
     name = StringField(max_length=100)
     age = IntField()
     teams = ListField()