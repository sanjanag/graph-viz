import psycopg2
from connect import connect
gX = connect()
cur = gX.cur
DEFAULT_WEIGHT = 10.0
DEFAULT_VALUE = 10

cur.execute('''CREATE TABLE IF NOT EXISTS testnodes
       (id SERIAL PRIMARY KEY  NOT NULL,
       value INT);''')
print "Table 'nodes' created successfully"

cur.execute('''CREATE TABLE IF NOT EXISTS testedges
        (row_id INT references testnodes(id) NOT NULL,
         column_id INT  references testnodes(id) NOT NULL,
         weight REAL NOT NULL,
PRIMARY KEY(row_id,column_id));''')

print "Table 'edges' created successfully"
gX.conn.commit()

file_path = "../data/testdata"

with open(file_path) as f:
    for line in f:
            line= line.split()
            row_id = int(line[0])
            column_id = int(line[1])
            weight = int(line[2])
            
            try:
                cur.execute("INSERT INTO testedges VALUES(%s, %s, %s)",(row_id,column_id,weight))
                gX.conn.commit()
                cur.execute("INSERT INTO testedges VALUES(%s, %s, %s)",(column_id,row_id,weight))
                gX.conn.commit()
            except psycopg2.IntegrityError as e:
                gX.conn.rollback()
                try:
#                    print "inserting node"
                    cur.execute("INSERT INTO testnodes VALUES(%s, %s)",(column_id,DEFAULT_VALUE))
                    gX.conn.commit()
                except:
                    gX.conn.rollback()
                try:
                    cur.execute("INSERT INTO testnodes VALUES(%s, %s)",(row_id,DEFAULT_VALUE))
                    gX.conn.commit()
                except:
                    gX.conn.rollback()
                try:
                    cur.execute("INSERT INTO testedges VALUES(%s, %s, %s)",(row_id,column_id,weight))
                    gX.conn.commit()
                    cur.execute("INSERT INTO testedges VALUES(%s, %s, %s)",(row_id,column_id,weight))
                    gX.conn.commit()

                except:
                    gX.conn.rollback()
                
gX.conn.commit()
gX.conn.close()




'''
CREATE or replace FUNCTION multiply(abc,abc) RETURNS TABLE(row_id INT, column_id INT, weight REAL ) AS '
SELECT $1.row_id, $2.column_id, sum($1.weight* $2.weight)   WHERE $1.column_id = $2.row_id GROUP BY $1.row_id,$2.column_id;
' LANGUAGE SQL;
'''
'''
CREATE or REPLACE FUNCTION multiply(testedges,testedges) RETURNS result AS '
 insert into result (row_id,column_id,weight) select row_id,column_id,weight from (select $1.row_id, $2.column_id , sum($1.weight*$2.weight) as weight where $1.column_id = $2.row_id group by $1.row_id,$2.column_id) as A; select * from result;
    ' LANGUAGE SQL;
'''
insert into result (row_id,column_id,weight) select a.row_id as row_id, b.column_id as column_id, sum(a.weight*b.weight) as weight from testedges as a, testedges as b where a.column_id = b.row_id group by a.row_id,b.column_id; 
