import fdb
class Database():

    def __init__(self, name):
        self._conn = fdb.connect(
                    dsn = name,
                    user ='SYSDBA', password='masterkey', 
                    charset='UTF8' 
                    )
        self._cursor = self._conn.cursor()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
         return self._conn

    @property
    def cursor(self):
        return self._cursor

    @property
    def rowCount(self):
        return self.cursor.rowcount


    def commit(self):
        self.connection.commit()

    def execute(self, sql,params=None):
         self.cursor.execute(sql,params or ())

    def executeMany(self,sql,params = None):
        self.cursor.executemany(sql,params or ())

    def fetchAll(self):
        return self.cursor.fetchall()

    def fetchOne(self):
        return self.cursor.fetchone()

    def query(self,sql,params=None):
        self.cursor.execute(sql,params or ())
        return self.cursor.fetchAll()
        
    def CloseConnection(self):
        self.connection.close()
        
        
    def CloseCursor(self):
        self.cursor.close()
        
    
    def FetchGenerator(self,generatorName,increment = 1):
        sql = "Select Gen_ID("+generatorName+","+str(increment)+") from RDB$DATABASE"
        self.execute(sql)
        # aici intorc cu 0 ca sa nu imi aduca in tupple ci normal
        result = self.fetchOne()[0]
        return result

    


        