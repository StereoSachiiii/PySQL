from typing import Union
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()


    
    
class ManagerDescriptor:
    def __get__(self, instance , owner):
        
         
        return BaseManager(owner)
    

class MetaModel(type):
    
    def __new__(cls,name,bases,attrs):        
        attrs['objects'] = ManagerDescriptor()
        query = "CREATE  TABLE IF NOT EXISTS User (name VARCHAR(30) NOT NULL PRIMARY KEY , age INT(10), gender VARCHAR(255) NOT NULL DEFAULT 'MALE')"     
        cursor.execute(query)
        return   super().__new__(cls,name,bases,attrs)

class BaseModel(metaclass=MetaModel):
    
    pass

    
class User(BaseModel):
    model_name = "User"


    
    
    
class BaseManager:
    
    def __init__(self,model_class : Union[User] ):
        self.model_class = model_class
    
    def select(self,*args :any):
        query = f"SELECT {",".join(args)} FROM  {self.model_class.model_name}"
        print(f"SELECT {",".join(args)} FROM  {self.model_class.model_name}")
        cursor.execute(query)
        return cursor.fetchall()
    
    def delete(self,*args:any,**kwargs:any):
        print(f"DELETE {", ".join(args)} , {", ".join([value for value in kwargs.values()])} FROM {self.model_class.model_name}")  
        
    def insert(self,*args,**kwargs):
        if args:
            placeholders = ", ".join(['?']*len(args))
            query = f"INSERT INTO {self.model_class.model_name} VALUES ({placeholders})"
            cursor.execute( query,args)
            
        if kwargs:
            keys = [str(key) for key in kwargs.keys()]
            values = [str(value) for value in kwargs.values()]
            
            keys = ", ".join((keys))
            placeholders_values = ",  ".join(['?']*len(values))
            
            query = f"INSERT INTO {self.model_class.model_name}({keys}) VALUES ({placeholders_values})"
            print(query,values)
            cursor.execute(query,values)


User.objects.insert(name="sachin",age=12)
print(User.objects.select("name","gender"))

        
    