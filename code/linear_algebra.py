from connect import connect
gX=connect()
cur = gX.cur

cur.execute("CREATE OR REPLACE FUNCTION mat_mul(A, B, C) ")
