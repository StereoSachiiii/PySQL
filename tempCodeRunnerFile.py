from typing import Union


class ManagerDescriptor:
    def __get__(self, instance , owner):
        return BaseManager(owner)

    
class User:
    model_name = "User"
    objects = ManagerDescriptor()
    
    
    
class BaseManager:
    
    def __init__(self,model_class : Union[User] ):
        self.model_class = model_class
    
    def select(self,*args :any):
        print(f"SELECT {",".join(args)} FROM  {self.model_class.model_name}")
    
    def delete(self,*args:any,**kwargs:any):
        print(f"DELETE {", ".join(args)} , {", ".join([value for value in kwargs.values()])} FROM {self.model_class.model_name}")  


    
User.objects.select("name","age","type")
User.objects.delete("name",age="age")
        
    