import sqlite3

# This key-value database is so fucked and needs a big rewrite!

class DataBase:
    def __init__(self, path:str) -> None:
        self.path = path
        
    def setup(self, *tables: str):
        length = len(list(tables))
        tables = list(tables) if not length == 0 else ["main"]

        with sqlite3.Connection(self.path) as file:
            db = file.cursor()
            for table in tables:
                db.execute(f'create table if not exists {table}(id unique, value)')
            file.commit()

    def get(self, id:str, table:str = "main"):
        id = id
        try:
            with sqlite3.Connection(self.path) as file:
                db = file.cursor()
                r = db.execute('select value from %s where id = ?'%table,(id, ))
                bruh = list(r)
                if len(bruh[0]) > 0:
                    return bruh[0][0]
                else:
                    return None
        except IndexError:
            return False
                


    def set(self, id:str, value, table:str = "main"):
        value = value
        with sqlite3.Connection(self.path) as file:
            db = file.cursor()
            if self.get(id=id, table=table) != False:
                db.execute('update %s set value = ? WHERE id = ?'%table, (value, id))
                # if self.get(id=id, table=table) != False else db.execute("insert into %s(id, value) values (?,?)"% table, (id, value))
            else:
                db.execute("insert into %s(id, value) values (?,?)"% table, (id, value))

            file.commit()
    def delete(self, id:str, table:str = "main"):
        with sqlite3.Connection(self.path) as file:
            db = file.cursor()
            db.execute(f'DELETE FROM "{table}" where "id" = ?', (id,))

            file.commit()


    def push(self, value, id:str, table:str = "main"):
        now = self.get(id=id, table=table)
        if now:
            if type(now) != list:
                return print("Error: value in the database should be 'list' or the value should be empty to push and pull items")
            else:
                now.append(value)
                self.set(id=id, value=now, table=table)
        else:
            array = [value]
            self.set(id=id, value=array, table=table)



    def pull(self, value, id:str, table:str = "main"):
        now = self.get(id=id, table=table)
        if now:
            if (type(now) != list):
                return print("Error: value in the database should be 'list' or the value should be empty to push and pull items")
            else:
                now.remove(value)
                self.set(id=id, value=now, table=table)
    def add(self,id:str,value: int,table:str = "main"):
        now = self.get(id=id, table=table)
        if now:
            if type(now) != int:
                return print("Error: value in the database should be 'int' or the value should be empty to add items")
            new = now + value
            self.set(id=id, table=table, value=new)
        else:
            self.set(id=id, table=table, value=value)
     

db = DataBase("DataBase.db")
