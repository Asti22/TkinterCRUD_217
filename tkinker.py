import sqlite3
con =sqlite3.connect("tutorial.db")
cur = con.cursor()
#cur.execute("""CREATE TABLE movie
    #(title text, year int, score double)""")
_title=input("masukan judul movie:")
_year=input("masukan tahun relase:")
_rating=input("masukan rating movienya:")
cur.execute(""""
    INSERT INTO movie VALUES
        ('{}',{},{})
""".format(_title,_year,_rating))
con.commit()

