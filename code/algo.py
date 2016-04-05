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
    gX.conn.commit()p

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
