from typing import Union
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()





# class metaField(type):
#     def __new__(cls,name,bases,attrs):
        
    
class Field:
    
    def __init__(self,field_type,primary_key=False,default=None,nullable=True,auto_increment=False):
        
        self.field_type = field_type
        self.default = default
        self.nullable = nullable
        self.primary_key = primary_key
        self.auto_increment = auto_increment
        
    
    def __get__(self,instance,owner):
        
        if instance is None:
            
            return self
        
        return instance.__dict__[self.name]
    
    def __set__(self,instance,value):
        
        instance.__dict__[self.name]= value
        
           
    
    

class ManagerDescriptor:
    def __get__(self, instance , owner):         
        return BaseManager(owner)

class MetaModel(type):
    
    def __new__(cls,name,bases,attrs):  
              
        attrs['objects'] = ManagerDescriptor()  
        attrs['_name'] = name
        class_attributes = [attribute for attribute in attrs.keys() if  isinstance(attrs[attribute],Field)]
        
        all_columns=[]
        if not name=="BaseModel":
            query_build=[]
            query_build.append(name)
            for class_attribute in class_attributes:
                field=[]
                              
                attrs[class_attribute].__dict__['name'] =  class_attribute
                field.append(class_attribute)
                field.append(attrs[class_attribute].field_type)
                
                if not attrs[class_attribute].nullable:
                    nullable = "NOT NULL"
                    field.append(nullable)
                
                    
                if  attrs[class_attribute].primary_key:
                    primary_key = "PRIMARY KEY"
                    field.append(primary_key)
                
                if attrs[class_attribute].auto_increment:
                    auto_increment = "AUTO INCREMENT"
                    field.append(auto_increment) 
                    
                if attrs[class_attribute].default:
                    default = f"DEFAULT '{attrs[class_attribute].default}'"
                    field.append(default)
                    
                query_build = " ".join(field)
                all_columns.append(query_build) 
            all_columns = ", ".join(all_columns)  
            print(all_columns)
            
            
                
            query = f"CREATE  TABLE  {name} ({all_columns})" 
            print(query)  
            cursor.execute(str(query))
            conn.commit()
        
        return   super().__new__(cls,name,bases,attrs)

class BaseModel(metaclass=MetaModel):
    
    pass

    
class Users(BaseModel):
   
    name = Field("VARCHAR(10)",primary_key=True, nullable=False)
    age = Field("INT")
    gender = Field("VARCHAR(10)",primary_key=False,default="Male", nullable=False)
    

# class Product(BaseModel):
    
#     id = Field("INT",primary_key=True,nullable=False)
#     name = Field("VARCHAR(10)")
    
    
    
class BaseManager:
    
    def __init__(self,model_class : Union[Users] ):
        self.model_class = model_class
    
    def select(self,*args :any):
        query = f"SELECT {",".join(args)} FROM  {self.model_class._name}"
        print(f"SELECT {",".join(args)} FROM  {self.model_class._name}")
        cursor.execute(query)
       
        print(query_results := cursor.fetchall() )
        
                  
    
    def delete(self,*args:any,**kwargs:any):
        print(f"DELETE {", ".join(args)} , {", ".join([value for value in kwargs.values()])} FROM {self.model_class.model_name}")  
        
    def insert(self,*args,**kwargs):
        if args:
            placeholders = ", ".join(['?']*len(args))
            query = f"INSERT INTO {self.model_class._name} VALUES ({placeholders})"
            cursor.execute( query,args)
            conn.commit()
            
        if kwargs:
            keys = [(key) for key in kwargs.keys()]
            values = [(value) for value in kwargs.values()]
            
            keys = ", ".join((keys))
            placeholders_values = ",  ".join(['?']*len(values))
            
            query = f"INSERT INTO {self.model_class._name}({keys}) VALUES ({placeholders_values})"
            print(query,values)
            cursor.execute(query,values)
            conn.commit()
            
    def all(self,*args,**kwargs):
            print(query := f"SELECT * FROM {self.model_class._name}")
            cursor.execute(query)
            rows = cursor.fetchall()

            objects_array = []
            
            attributes = [attribute.name for attribute in self.model_class.__dict__.values() if isinstance(attribute,Field)]
            
            print(attributes)
            for row in rows:
                key_values = zip(attributes,row)
                user = Users()
                for key,value in key_values:
                    
                    
                    user.__dict__[key] = value 
                objects_array.append(user)
                

            return objects_array



Users.objects.insert(name="sachin",age=12)
Users.objects.insert("Akisha",12,"Female")
Users.objects.insert("hernandez",32,"Female")

print(Users.objects.select("*"))
all_users = Users.objects.all()
print(all_users[0].name)
        
    