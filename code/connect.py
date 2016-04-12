import psycopg2
class connector(object):
    def __init__(self,dbname,hostname,username,passwd):
        try:
            self.conn = psycopg2.connect("dbname=%s user=%s host=%s password=%s"%(dbname,username,hostname,passwd))
        except:
            print "I am unable to connect to the database"
        self.cur = self.conn.cursor()
    def get_databases(self):
        self.cur.execute("""SELECT datname from pg_database""")
        res = self.cur.fetchall()
        print "\nShow me the databases:\n"
        for row in res:
            print "   ", row[0]


def connect():
    dbname = 'GraphX'
    hostname = 'localhost'
    username = 'postgres'
    passwd = 'alohomora'
    gX = connector(dbname,hostname,username,passwd)
    return gX
    
if __name__ == '__main__':
    dbname = 'GraphX'
    hostname = 'localhost'
    username = 'postgres'
    passwd = 'alohomora'
    gX = connector(dbname,hostname,username,passwd)
    gX.get_databases()
