import sqlite3
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
file_path = "database/db.sqlite3"
con = sqlite3.connect(file_path)
cur = con.cursor()
now = datetime.now()





class Database:
    @staticmethod
    def execute(user_id,expiration_date):
        search_query = f" SELECT * FROM user WHERE id ={user_id}"
        search = cur.execute (search_query)
        if len(search.fetchall()) > 0:
            print("Ce client est dêjà enregistré")
            return True
        query = f"INSERT INTO user VALUES ({user_id},'{expiration_date}')"
        print(query)
        cur.execute(query)
        con.commit()
        for loop in cur:
            print(loop)
    @staticmethod
    def ajout_parrain(user_id):
        search_query = f" SELECT * FROM parrains WHERE id ={user_id}"
        search = cur.execute(search_query)
        elements = len(search.fetchall())
        if elements > 0:

            query = f"UPDATE parrains SET somme = somme +4 WHERE id = {user_id} "
            cur.execute(query)
            con.commit()
            return
        else:
            insert_query = f"INSERT INTO parrains VALUES ({user_id},{4})"
            cur.execute(insert_query)
            con.commit()
            return
    @staticmethod
    def reset_parrain(user_id):
        search_query = f" SELECT * FROM parrains WHERE id ={user_id}"
        search = cur.execute(search_query)
        elements = len(search.fetchall())
        if elements > 0:
            query = f"UPDATE parrains SET somme = 0 WHERE id = {user_id} "
            cur.execute(query)
            con.commit()
            return
        else:
            return False




    @staticmethod
    def prolong(user_id):
        search_query = f" SELECT * FROM user WHERE id ={user_id}"
        search =cur.execute(search_query)
        date = (cur.fetchall()[0][1])

        a=date.replace("-","/")

        date_object = datetime.strptime(a, '%Y/%m/%d').date()
        new_date = date_object + relativedelta(months=+1)

        query = f"UPDATE user SET expiration_date ='{new_date}' WHERE id = {user_id} "
        command = cur.execute(query)
        con.commit()
        return new_date
    @staticmethod
    def check_if_registered(user_id):
        date_time_str = now.strftime("%d/%m/%Y")
        date_db = datetime.strptime(date_time_str, '%d/%m/%Y').date()
        search_query = f" SELECT * FROM user WHERE id ={user_id}"
        delete_query ="DELETE FROM users WHERE id = (?)", [user_id]
        search = cur.execute(search_query)
        con.commit()
        response= search.fetchall()
        if len(response) > 0:
            a = response[0][1].replace("-", "/")
            date_object = datetime.strptime(a, '%Y/%m/%d').date()

            if  date_object <date_db+timedelta(days=-1) or date_object == date_db+timedelta(days=-1):
                cur.execute("DELETE FROM user WHERE id = (?)", [user_id])
                print("Enlèvement")
                con.commit()
                return True
            else:
                return False
        return False
    @staticmethod
    def add_test_user(user_id, expiration_date):
        blacklist_search_query = f"SELECT * FROM passed_test WHERE id ={user_id}"
        a = cur.execute(blacklist_search_query)
        if len(a.fetchall()) > 0:
            return 5
        search_query = f" SELECT * FROM test_user WHERE id ={user_id}"
        search = cur.execute(search_query)
        if len(search.fetchall()) > 0:

            return True
        query = f"INSERT INTO test_user VALUES ({user_id},'{expiration_date}')"
        cur.execute(query)
        con.commit()

        return False
    @staticmethod
    def check_if_registered_test(user_id):
        date_time_str = now.strftime("%d/%m/%Y")
        date_db = datetime.strptime(date_time_str, '%d/%m/%Y').date()
        search_query = f" SELECT * FROM test_user WHERE id ={user_id}"
        delete_query = f" DELETE  FROM test_user WHERE id ={user_id}"
        search = cur.execute(search_query)
        con.commit()
        response = search.fetchall()
        if len(response) > 0:
            a = response[0][1].replace("-", "/")
            date_object = datetime.strptime(a, '%Y/%m/%d').date()

            if date_object < date_db + timedelta(days=-1) or date_object == date_db + timedelta(days=-1):
                print("date_db")
                print("true", user_id)
                cur.execute(delete_query)
                return 5
            else:
                return False
        return False
    @staticmethod
    def blacklist_test(user_id):
        query = f"INSERT INTO passed_test VALUES({user_id})"
        cur.execute(query)
    @staticmethod
    def end_date(user_id):
        date_time_str = now.strftime("%d/%m/%Y")
        date_db = datetime.strptime(date_time_str, '%d/%m/%Y').date()
        search_query = f" SELECT * FROM user WHERE id ={user_id}"
        search = cur.execute(search_query)
        con.commit()
        response = search.fetchall()

        if len(response) > 0:
            a = response[0][1].replace("-", "/")
            date_object = datetime.strptime(a, '%Y/%m/%d').date()

            if date_object < date_db + timedelta(days=7) or date_object == date_db + timedelta(days=7):
                return response[0][1]
            else:
                return False
        return False







