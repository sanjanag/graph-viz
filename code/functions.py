import psycopg2
from connect import connect
gX = connect()
cur = gX.cur()

def matrix_multiply():
    CREATE TABLE IF NOT EXISTS matrix1
    (row_id INT NOT NULL,
     column_id INT NOT NULL,
     weight REAL NOT NULL,
     PRIMARY KEY(row_id,column_id));

    CREATE TABLE IF NOT EXISTS matrix2
    (row_id INT NOT NULL,
     column_id INT NOT NULL,
     weight REAL NOT NULL,
     PRIMARY KEY(row_id,column_id));
    
    CREATE or REPLACE FUNCTION multiply(matrix1,matrix2) RETURNS TABLE(row_id INT, column_id INT, weight REAL ) AS '
SELECT $1.row_id, $2.column_id, sum($1.weight* $2.weight)   WHERE $1.column_id = $2.row_id GROUP BY $1.row_id,$2.column_id;
' LANGUAGE SQL;
