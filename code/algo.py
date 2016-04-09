import psycopg2
import math
from connect import connect
gX = connect()
cur = gX.cur

def initialise_v():
    cur.execute('''CREATE TABLE IF NOT EXISTS V
    (row_id INT NOT NULL,
    column_id INT NOT NULL,
    weight REAL NOT NULL,
    PRIMARY KEY(row_id,column_id));''')
    gX.conn.commit()

    cur.execute('''select count(*) from nodes;''')
    num_nodes =  cur.fetchone()[0]
    for i in range(num_nodes):
        cur.execute("INSERT INTO V VALUES(%s, %s, %s)", (i+1, 1, 1.0/math.sqrt(num_nodes)))
    gX.conn.commit()

def create_A():
    cur.execute('''CREATE TABLE IF NOT EXISTS A
    (row_id INT NOT NULL,
    column_id INT NOT NULL,
    similarity REAL NOT NULL,
    PRIMARY KEY(row_id,column_id));''')
    gX.conn.commit()

    cur.execute("INSERT INTO A (row_id,column_id,similarity) SELECT row_id,column_id,1 FROM edges")
    gX.conn.commit()

def create_D():
    cur.execute('''CREATE TABLE IF NOT EXISTS D
    (id INT NOT NULL,
    value REAL NOT NULL,
    PRIMARY KEY(id));''')
    gX.conn.commit()

    cur.execute("insert into D (id,value) select row_id as id, sum(similarity) as value from A group by row_id")    
    gX.conn.commit()

def calc_Dinverse():
    cur.execute("update D set value = 1/value")
    gX.conn.commit()

def create_L():
    cur.execute("update A set similarity = similarity*(select value from D where D.id = A.row_id)")
    gX.conn.commit()

def create_VT():
    cur.execute('''CREATE TABLE IF NOT EXISTS VT
    (row_id INT NOT NULL,
    column_id INT NOT NULL,
    weight REAL NOT NULL,
    PRIMARY KEY(row_id,column_id));''')
    gX.conn.commit()


def calc_VT():
    cur.execute("insert into VT (row_id,column_id,weight) select row_id, column_id, weight from (select A.row_id as row_id, V.column_id as column_id, sum(A.similarity*V.weight) as weight from A,V where A.column_id=V.row_id group by A.row_id,V.column_id) as X")
    gX.conn.commit()
    cur.execute("select sum(VT.weight*VT.weight) from VT")
    norm = math.sqrt(cur.fetchone()[0])
    cur.execute("update VT set weight = weight/(select sum(VT.weight*VT.weight) from VT)")
    gX.conn.commit()
    
def create_delta():
    cur.execute('''CREATE TABLE IF NOT EXISTS delta
    (row_id INT NOT NULL,
    column_id INT NOT NULL,
    weight REAL NOT NULL,
    PRIMARY KEY(row_id,column_id));''')
    gX.conn.commit()

    cur.execute('''select count(*) from nodes;''')
    num_nodes =  cur.fetchone()[0]
    for i in range(num_nodes):
        cur.execute("INSERT INTO delta VALUES(%s, %s, %s)", (i+1, 1, 0))
    gX.conn.commit()

def create_deltaT():
    cur.execute('''CREATE TABLE IF NOT EXISTS deltaT
    (row_id INT NOT NULL,
    column_id INT NOT NULL,
    weight REAL NOT NULL,
    PRIMARY KEY(row_id,column_id));''')
    gX.conn.commit()

def calc_deltaT():
    cur.execute("insert into deltaT select VT.row_id, VT.column_id, abs(VT.weight-V.weight) as diff from VT, V where VT.row_id=V.row_id and VT.column_id= V.Column_id")



    
def iterate():
    iter = 0
    cur.execute("select count(*) from (select deltaT.row_id, deltaT.column_id, abs(deltaT.weight - delta.weight) as diff from deltaT, delta where deltaT.row_id=delta.row_id and deltaT.column_id=delta.column_id) as X where X.diff>.0001")
    count = cur.fetchone()[0]
    while(iter!=10 or count != 0):
        cur.execute("drop table V")
        gX.conn.commit()
        cur.execute("alter table VT rename to V")
        gX.conn.commit()
        cur.execute("drop table delta")
        gX.conn.commit()
        cur.execute("alter table deltaT rename to delta")
        gX.conn.commit()
        create_VT()
        calc_VT()
        create_deltaT()
        calc_deltaT()
        gX.conn.commit()
        iter += 1
'''
initialise_v()
create_A()
create_D()
calc_Dinverse()
create_L()
create_VT()
calc_VT()
create_delta()
create_deltaT()
calc_deltaT()'''
iterate()
