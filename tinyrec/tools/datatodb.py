
import psycopg2

class PGconnector:
    
    def __init__(self):
        pass
    
    def connect(self, hostaddr, dbname, user, passwd, port = "5432"):
        self.hostaddr = hostaddr
        self.dbname = dbname
        self.user = user
        self.passwd = passwd

        self.conn = psycopg2.connect(database = dbname, user = user, password = passwd, host=hostaddr, port = port) 
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        self.cursor.execute(sql)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

def insert_sql_jointer(table, keyvalue):
    collumns = []
    values = []
    for k,v in keyvalue.items():
        collumns.append(k)
        collumns.append(',')
        values.append('\'' + v + '\'')
        values.append(',')
    collumns.pop()
    values.pop()

    sql = "INSERT INTO " + table + " (" + "".join(collumns) + ") VALUES ("\
            + "".join(values) + ")"

    return sql

def insert_test(data_file_path):
    con = PGconnector()
    con.connect("127.0.0.1", "trecdb", "trecuser", "111111")
    with open(data_file_path) as data_file:
        count = 0
        for line in data_file:
            line = line.strip().split("::")
            record = {"userid":line[0],"movieid":line[1],"rate":line[2],"ratingtime":line[3]} 
            sql = insert_sql_jointer("ratings",record)
            con.execute(sql)
            count += 1
            if count % 1000 ==1 :
                con.commit()
                print count
    con.close()

if __name__ == "__main__":
    
    insert_test("/home/wjx/recsys/MovieLensDS/ratings.dat")




