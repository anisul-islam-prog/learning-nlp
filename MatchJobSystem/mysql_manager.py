import mysql.connector

USER = "root"
PASSWORD = ""
HOST = "127.0.0.1"
PORT = '3306'
DATABASE = "publications_db"

class MySQLManager:
    def __init__(self):
        self.cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)

    def insert(self, obj):       
        sttmt = "INSERT INTO publications_tab_2020(author, university, vector) VALUES (%(author)s, %(university)s, %(vector)s)"
        cursor = self.cnx.cursor()
        cursor.execute(sttmt, obj)
        self.cnx.commit()
        cursor.close()

    def delete_candidate(self):
        cursor = self.cnx.cursor()
        cursor.execute("delete from candidate")
        self.cnx.commit()
        cursor.close()

    def insert_candidate(self, obj): 
        sttmt = "INSERT INTO candidate(Candidate, University, Number_of_docs, Avg_sim, Average_Similarity, Image_Avg, Variance, Image_Var) VALUES (%(author)s, %(university)s, %(doc_count)s, %(avg_sim)s, %(mean)s, %(meanimage)s, %(var)s, %(varimage)s)"
        cursor = self.cnx.cursor()
        cursor.execute(sttmt, obj)
        self.cnx.commit()
        cursor.close()

    def select(self,year):
        sttmt = "SELECT author, university, vector FROM publications_tab_"+year
        cursor = self.cnx.cursor()
        cursor.execute(sttmt)

        res = []
        for (author, university, vector) in cursor:
            res.append({
                "author": author,
                "university": university,
                "vector": vector
            })

        self.cnx.commit()
        cursor.close()
        return res

    def close(self):
        self.cnx.close()
