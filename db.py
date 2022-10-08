from store_config import *
import mysql.connector
from mysql.connector import Error

class DB:
    def __init__(self, host = None, db = None, user = None, password = None, permanent = False):
        self.err = ""
        self.lastrowid = None
        self.permanent = permanent

        if host is None:
            host = DEF_HOST
        if db is None:
            db = DEF_DB
        if user is None:
            user = DEF_USER
        if password is None:
            password = DEF_PASS

        try:
            self.conn = mysql.connector.connect(host=host, database=db, user=user, password=password, charset = 'utf8')
        except mysql.connector.Error as e:
            self.err = e
            self.conn = None

    def is_connected(self):
        return not self.conn is None
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.permanent:
            self.disconnect()
    
    def disconnect(self):
        if self.is_connected():
            self.conn.close()
            self.conn = None

    def query(self, q):
        self.err = ""
        res = 0
        try:
            cursor = self.conn.cursor()
            cursor.execute(q)
            res = cursor.rowcount # returns number of rows
            self.lastrowid = cursor.lastrowid # returns the value generated for an AUTO_INCREMENT column
            self.conn.commit()
        except mysql.connector.Error as e:
            self.err = e
        finally:
            cursor.close()
        return res

    def select_query(self, q):
        self.err = ""
        res = []
        try:
            cursor = self.conn.cursor()
            cursor.execute(q)
            res = cursor.fetchall() # fetches query results as a list of tuple
        except mysql.connector.Error as e:
            self.err = e
        finally:
            cursor.close()
        return res

    def get_err(self):
        return self.err

    def get_lastrowid(self):
        return self.lastrowid
        
class StoreDB:
    def __init__(self, host = None, db = None, user = None, password = None):
        self.err = ""
        self.lastrowid = None
        self.db_handler = None  # obiekt połączenia z db

        if host is None:
            self.host = DEF_HOST
        else:
            self.host = host
        if db is None:
            self.db = DEF_DB
        else:
            self.db = db
        if user is None:
            self.user = DEF_USER
        else:
            self.user = user
        if password is None:
            self.password = DEF_PASS
        else:
            self.password = password

    def connect(self, perm = True):
        self.db_handler = DB(host=self.host, db=self.db, user=self.user, password=self.password, permanent=perm)
        if not self.db_handler.is_connected():
            self.err = self.db_handler.get_err()
            return False
        return True
        
    def disconnect(self):
        self.db_handler.disconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def get_err(self):
        return self.err

    def exec_query(self, q):
        self.err = ""
        if(self.db_handler is None or not self.db_handler.is_connected()) and not self.connect(False):  #jezeli nie ma połączenia i nie udało się nawiązać połączenia 
            return 0

        with self.db_handler:
            res = self.db_handler.query(q)
            if not res:
                self.err = self.db_handler.get_err()
            else:
                self.lastrowid = self.db_handler.get_lastrowid()
        return res

    def exec_select_query(self, q):
        if (self.db_handler is None or not self.db_handler.is_connected()) and not self.connect(False):
            return []
        
        with self.db_handler:
            res = self.db_handler.select_query(q)
            self.err = self.db_handler.get_err()
        return res

    def add_cat(self, parent_id, name):
        if parent_id is None:
            ps = "NULL"
        else:
            ps = str(parent_id)

        q = f"INSERT INTO `category` (`name`, `parent_id`) VALUES (\"{name}\", {ps})"

        if (self.exec_query(q) == 1):
            return self.lastrowid
        return None


    def change_cat(self, id, name=None, parent_id=False):
        param = ""
        if not name is None:
            param = "," + f"`name`=\"{name}\""
        if not parent_id is False:
            if parent_id is None:
                param = param + "," + "`parent_id` =\"NULL\""
            else:
                param = param + "," + f"`parent_id`= {parent_id}"
        param = param[1:]

        q = f"UPDATE `category` SET {param} WHERE `id`={id}"

        return (self.exec_query(q) == 1)


    def get_cat(self, id):
        q = f"SELECT `name`, `parent_id` FROM `category` WHERE `id`={id}"
        return self.exec_select_query(q)
    
    def get_cat_by_parent(self, parent_id):
        if parent_id is None:   # zwraca kategorie, które nie mają rodzica
            ps = "IS NULL"
        else:
            ps = "= " + str(parent_id)
        
        q = f"SELECT `id`, `name` FROM `category` WHERE `parent_id` {ps}"

        return self.exec_select_query(q)

    def add_product(self, name, desc, qty, price, cat_list):
        if qty <= 0:
            self.err = f"Niepoprawna liczba sztuk: {qty}"
            return False
        if price < 0.5:
            self.err = f"Niepoprawna cena: {price}"
            return False
        q = f"INSERT INTO `product` (`name`, `desc`, `qty`, `price`) \
            VALUES(\"{name}\", \"{desc}\", {qty}, {price})"
        
        if self.exec_query(q) != 1:
            return None
        
        lst = self.lastrowid

        if len(cat_list) == 0:
            return lst
        q = f"INSERT INTO `pr_cat`(`pr_id`,`cat_id`) VALUES"
        for i in cat_list:
            q = q + f"({lst}, {i}),"
        q = q[:-1]

        if (self.exec_query(q) == len(cat_list)):
            return lst
        return None


    def change_product(self, id, name=None, desc=None, qty=None, price=None):
        param = ""
        if not name is None:
            param = "," + f"`name`=\"{name}\""
        if not desc is None:
            param = param + "," + f"`desc`=\"{desc}\""
        if not qty is None:
            param = param + "," + f"`qty`={qty}"
        if not price is None:
            param = param + "," + f"`price`={price}"
        param = param[1:]

        q = f"UPDATE `product` SET {param} WHERE `id`={id}"
        print(q)
    

with StoreDB(db = "u202942_test") as d:
    print(d.get_err())
    print(d.get_cat(35))
    

d = StoreDB(db = "u202942_test")
print(d.get_cat(2))

d.change_cat(2,"dtghgtvjvfthj", 4)
print(d.get_err())

print(d.get_cat(2))
