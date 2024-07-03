from database.DB_connect import DBConnect
from model.genre import Genre
from model.track import Track


class DAO():

    @staticmethod
    def getGenre():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query= """select *
                from genre g 
                order by Name"""
        cursor.execute(query,)
        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(genere, mMin, mMax):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from track t 
                    where GenreId = %s and Milliseconds >= %s and Milliseconds <= %s"""
        cursor.execute(query, (genere, mMin, mMax, ))
        for row in cursor:
            result.append(Track(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdge(genere, mMin, mMax, idMap):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select tk1, tk2
                    from(select t.TrackId as tk1, count(*) as n1
                            from playlisttrack p, track t 
                            where p.TrackId = t.TrackId and t.GenreId = %s and t.Milliseconds >= %s and t.Milliseconds <= %s
                            group by t.TrackId) t1,
                        (select t.TrackId as tk2, count(*) as n2
                            from playlisttrack p, track t 
                            where p.TrackId = t.TrackId and t.GenreId = %s and t.Milliseconds >= %s and t.Milliseconds <= %s
                            group by t.TrackId) t2
                    where t1.n1 = t2.n2 and t1.tk1 < t2.tk2"""
        cursor.execute(query, (genere, mMin, mMax, genere, mMin, mMax,))
        for row in cursor:
            result.append((idMap[row['tk1']],
                           idMap[row['tk2']]))

        cursor.close()
        conn.close()
        return result

