import psycopg2
from connect import connect
gX = connect()
cur = gX.cur
DEFAULT_WEIGHT = 10.0
DEFAULT_VALUE = 10

cur.execute('''CREATE TABLE IF NOT EXISTS nodes
       (id SERIAL PRIMARY KEY  NOT NULL,
       value INT);''')
print "Table 'nodes' created successfully"

cur.execute('''CREATE TABLE IF NOT EXISTS edges
        (row_id INT references nodes(id) NOT NULL,
         column_id INT  references nodes(id) NOT NULL,
         weight REAL NOT NULL,
         PRIMARY KEY(row_id,column_id));''')
print "Table 'edges' created successfully"

file_path = "../data/facebook_combined.txt"

with open(file_path) as f:
    for line in f:
            line= line.split()
            row_id = int(line[0])+1
            column_id = int(line[1])+1
            #print row_id,column_id
            try:
                cur.execute("INSERT INTO edges VALUES(%s, %s, %s)",(row_id,column_id,DEFAULT_WEIGHT))
                gX.conn.commit()
                #print "Upper",row_id,column_id
            except psycopg2.IntegrityError as e:
                gX.conn.rollback()
                try:
                    cur.execute("INSERT INTO nodes VALUES(%s, %s)",(column_id,DEFAULT_VALUE))
                    gX.conn.commit()
                except:
                    gX.conn.rollback()
                    #print "Node with id=%d already present"%(column_id)
                try:
                    cur.execute("INSERT INTO nodes VALUES(%s, %s)",(row_id,DEFAULT_VALUE))
                    gX.conn.commit()
                    #print "Upper",row_id,column_id,"1"
                except:
                    gX.conn.rollback()
                    #print "Node with id=%d already present"%(row_id)
                try:
                    cur.execute("INSERT INTO edges VALUES(%s, %s, %s)",(row_id,column_id,DEFAULT_WEIGHT))
                    gX.conn.commit()
                except:
                    gX.conn.rollback()
                    #print "Row already present"
                
gX.conn.commit()
gX.conn.close()
