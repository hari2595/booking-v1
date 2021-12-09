import sqlite3
import pandas as pd

def app():
    print("Welcome to Streaming catalog system!")
    print("1. Create an account")
    print("2. Login into existing account")
    print("*" * 100)
    choice = int(input("Enter your choice: "))
    try:
        if choice == 1:
            print("1. Create Admin Account")
            print("2. Create User Account")
            print("Press any other Key to exit")
            print("*" * 100)
            choice1 = int(input("Enter your choice: "))
            print("*" * 100)

            if choice1 == 1:
                print("Lets create an admin account")
                username = input("Enter username: ")
                username = username.lower()
                password = input("Enter password: ")
                password = password.lower()
                print("*" * 100)
                create_admin(username, password)

            if choice1 == 2:
                print("Lets create an user account")
                username = input("Enter username: ")
                username = username.lower()
                password = input("Enter password: ")
                password = password.lower()
                print("*" * 100)
                create_user(username, password)

        if choice == 2:
            print("1. Login into Admin Account")
            print("2. Login into User Account")
            print("Press any Key to exit")
            print("*" * 100)
            choice1 = int(input("Enter your choice: "))
            print("*" * 100)

            if choice1 == 1:
                print("Welcome to admin login!")
                username = input("Enter username: ")
                username = username.lower()
                password = input("Enter password: ")
                password = password.lower()
                print("*" * 100)
                admin_login(username, password)


            if choice1 == 2:
                print("Welcome to user login!")
                username = input("Enter username: ")
                username = username.lower()
                password = input("Enter password: ")
                password = password.lower()
                print("*" * 100)
                user_login(username, password)

        elif choice == 3:
            return "break"
    except :
        print("_" * 100)
        print(" " * 30 +"Exited successfully")
        print("_" * 100)

def sql_database():
    conn = sqlite3.connect('streamingCatalogSystem.db')
    c = conn.cursor()

    # create tables
    c.execute('''CREATE TABLE IF NOT EXISTS tb_user
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LOGIN VARCHAR NOT NULL,
                PASSWORD VARCHAR NOT NULL
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS tb_admin
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LOGIN VARCHAR NOT NULL,
                PASSWORD VARCHAR NOT NULL
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS tb_movies
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR NOT NULL,
                DURATION INT NOT NULL,
                CATEGORY VARCHAR NOT NULL
                );''')
    c.execute('''CREATE TABLE IF NOT EXISTS tb_series
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    NAME VARCHAR NOT NULL,
                    NO_OF_SEASON INT NOT NULL,
                    CATEGORY VARCHAR NOT NULL
                    );''')
    c.execute('''CREATE TABLE IF NOT EXISTS tb_userdata
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    LOGIN VARCHAR NOT NULL,
                    SHOW_NAME VARCHAR NOT NULL,
                    TYPE_SHOW VARCHAR NOT NULL,
                    DURATION INT,
                    SEASON INT,
                    TIME VARCHAR NOT NULL
                    );''')

    # commit the changes to db
    conn.commit()
    # close the connection
    conn.close()


def create_admin(username, password):
    admin_data = check_admin(username)
    if len(admin_data) > 0:
        print("Cannot create new admin user because username already exists.")
        return
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    params = (username, password)
    cursor.execute("INSERT INTO tb_admin (LOGIN, PASSWORD) VALUES (?,?)", params)
    conn.commit()
    print('Admin Creation Successful')
    print("*" * 100)
    conn.close()


def check_admin(username):
    query = f"select ID from tb_admin where LOGIN = '{username}'"
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    res = cursor.execute(query)
    result = res.fetchall()
    return result


def create_user(username, password):
    users_data = check_user(username)
    if len(users_data) > 0:
        print("Cannot create new user because username already exists.")
        return
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    params = (username, password)
    cursor.execute("INSERT INTO tb_user (LOGIN, PASSWORD) VALUES (?,?)", params)
    conn.commit()
    print('User Creation Successful')
    print("*" * 100)
    conn.close()


def check_user(username):
    query = f"select ID from tb_user where LOGIN = '{username}'"
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    res = cursor.execute(query)
    result = res.fetchall()
    return result


def user_login(username, password):
    users_data = check_user(username)
    if len(users_data) == 0:
        print("Login unsuccessful because user doesn't exist.")
        print("*" * 100)
        return
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM tb_user WHERE LOGIN ='{username}'")
    data = cur.fetchone()
    if data[2] == password:
        print('******************************')
        print(f"{username} LogIn Successful")
        print('******************************')
        while True:
            data = user_data(username)
            if data == "break":
                break
    else:
        print("Login unsuccessful password incorrect.")
        print("*" * 100)



def user_data(username):
    print("Select what you want to do")
    print("1. Watch Movies")
    print("2. Watch Series")
    print("3. View the shows I have already selected.")
    print("-------------Enter any other character to exit---------------")
    user_choice = int(input("Enter your Choice: "))

    if user_choice == 1:
        print("What movie you would like to watch? ")
        print("*************************************")
        print("NO:  Movie   Length Genre")
        conn = sqlite3.connect('streamingCatalogSystem.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * from tb_movies''')
        movie_row = cursor.fetchall()
        for movie_row in movie_row:
            print(movie_row)

        print("*" * 100)

        movie_choice = int(input("Enter the number for which you want to watch movie: "))
        time = input("At what time will you watch/book the movie? ")
        query = f"select TIME from tb_userdata where LOGIN = '{username}'"
        time_check = cursor.execute(query)
        time_list = time_check.fetchall()
        time_list = [x[0] for x in time_list]
        if time in time_list:
            print("You have already booked at this time select another time")
            return
        movie = "movie"
        conn.close()
        add_moviechoice(username, movie_choice, movie, time)


    elif user_choice == 2:
        print("What series you would like to watch? ")
        print("*************************************")
        print("NO:  Series Seasons Genre")
        conn = sqlite3.connect('streamingCatalogSystem.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * from tb_series''')
        movie_row = cursor.fetchall()
        for movie_row in movie_row:
            print(movie_row)
        # conn.close()
        print("*" * 100)
        series_choice = int(input("Enter the number for which you want to watch series: "))
        # username = input("Enter your username: ")
        time = input("At what time will you watch/book the series? Please enter in hh:mm am/pm. ")

        query = f"select TIME from tb_userdata where LOGIN = '{username}'"
        time_check = cursor.execute(query)
        time_list = time_check.fetchall()
        time_list = [x[0] for x in time_list]
        if time in time_list:
            print("You have already booked at this time select another time")
            return

        series = "series"
        conn.close()
        add_serieschoice(username, series_choice, series, time)


    elif user_choice == 3:
        print("These are the details of the movies/series you have selected: ")
        conn = sqlite3.connect('streamingCatalogSystem.db')
        cursor = conn.cursor()
        # username = input("Enter your username: ")
        query = f"select * from tb_userdata where LOGIN = '{username}'"
        cursor.execute(query)
        show_row = cursor.fetchall()
        for show_row in show_row:
            print("Id: ", show_row[0])
            print("Your username: ", show_row[1])
            print("Show Name: ", show_row[2])
            print("Show Type: ", show_row[3])
            print("Duration: ",show_row[4])
            print("Season: ", show_row[5])
            print("Time: ", show_row[6])
            print("*" * 100)
#            print(show_row)

        conn.close()
        print("*" * 100)

    elif user_choice == 4:
        return "break"



def add_moviechoice(username, movie_choice, movie, time):
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT NAME, DURATION FROM tb_movies WHERE ID ='{movie_choice}'")
    movie_row = cursor.fetchall()

    for movie_row in movie_row:
        movie_name = movie_row[0]
        dur = movie_row[1]

    params = (username, movie_name, movie, dur, time)
    cursor.execute("INSERT INTO tb_userdata (LOGIN, SHOW_NAME, TYPE_SHOW, DURATION, TIME) VALUES (?,?,?,?,?)", params)
    conn.commit()
    print('Movie time booked')
    conn.close()



def add_serieschoice(username, series_choice, series, time):
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT NAME, NO_OF_SEASON FROM tb_series WHERE ID ='{series_choice}'")
    series_row = cursor.fetchall()
    for series_row in series_row:
        series_name = series_row[0]
        season = series_row[1]
    params = (username, series_name, series, season, time)
    cursor.execute("INSERT INTO tb_userdata (LOGIN, SHOW_NAME, TYPE_SHOW, SEASON, TIME) VALUES (?,?,?,?,?)", params)
    conn.commit()
    print('Series time booked')
    conn.close()


def admin_login(username, password):
    admin_data = check_admin(username)
    if len(admin_data) == 0:
        print("Login unsuccessful because user doesn't exist.")
        print("*" * 100)
        return

    conn = sqlite3.connect('streamingCatalogSystem.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM tb_admin WHERE LOGIN ='{username}'")
    data = cur.fetchone()
    if data[2] == password:
        print('******************************')
        print(f"{username} LogIn Successful")
        # print(f"Number of previous logins:{num_logins}")
        print('******************************')
        # update_access_count(user_data[0][0])
        while True:
            movies_data = movie_data()
            if movies_data == "break":
                break
    else:
        print("Login unsuccessful password incorrect.")
        print("*" * 100)




def movie_data():
    print("What data you would like to do?")
    print("1. Add Movies")
    print("2. Add Series")
    print("3. View movies catalog")
    print("4. View series catalog")
    print("5. View user bookings")
    print("6. View Reports")
    print("_" * 100)
    print("Enter any other character to exit")
    print("*" * 100)
    admin_choice = int(input("Enter your choice"))

    try:
        if admin_choice == 1:
            movie_name = input("Enter movie name: ")
            movie_dur = input("Enter movie duration: ")
            movie_cat = input("Enter movie category: ")
            add_movie(movie_name, movie_dur, movie_cat)

        if admin_choice == 2:
            series_name = input("Enter series name: ")
            series_season = input("Enter number of season in this series: ")
            series_cat = input("Enter series category: ")
            add_series(series_name, series_season, series_cat)

        if admin_choice == 3:
            print("NO:  Movie   Length Genre")
            conn = sqlite3.connect('streamingCatalogSystem.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * from tb_movies''')
            movie_row = cursor.fetchall()
            for movie_row in movie_row:
                print(movie_row)

            print("*" * 100)
            while True:
                movies_data = movie_data()
                if movies_data == "break":
                    break

        if admin_choice == 4:
            print("NO:  Series Seasons Genre")
            conn = sqlite3.connect('streamingCatalogSystem.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT * from tb_series''')
            movie_row = cursor.fetchall()
            for movie_row in movie_row:
                print(movie_row)

            print("*" * 100)
            while True:
                movies_data = movie_data()
                if movies_data == "break":
                    break

        if admin_choice == 5:
            conn = sqlite3.connect('streamingCatalogSystem.db')
            cursor = conn.cursor()
            # username = input("Enter your username: ")
            query = f"select * from tb_userdata "
            cursor.execute(query)
            show_row = cursor.fetchall()
            for show_row in show_row:
                print("_" * 100)
                print("Id: ", show_row[0])
                print("Username: ", show_row[1])
                print("Show Name: ", show_row[2])
                print("Show Type: ", show_row[3])
                print("Time: ", show_row[6])
                print("_" * 100)
                while True:
                    movies_data = movie_data()
                    if movies_data == "break":
                        break


        if admin_choice == 6:
            print("1: View all the available movie categories")
            print("2: View all the available series categories")
            print("3: View all the movies that are booked by the users")
            print("4: View all the series that are booked by the users")
            print("5: View the non admin user list")
            print("6: View all the available series with more than 4 seasons")
            print("7: View all the available movie longer than 120 mins")
            print("_" * 100)
            print("Enter any other character to exit")
            print("_" * 100)
            rchoice = int(input("Enter your choice: "))
            print("*" * 100)
            if rchoice == 1:
                movie_cat_list()
                print("*" * 100)

            if rchoice == 2:
                series_cat_list()
                print("*" * 100)

            if rchoice == 3:
                movies_booked()
                print("*" * 100)

            if rchoice == 4:
                SERIES_booked()
                print("*" * 100)

            if rchoice == 5:
                user_list()
                print("*" * 100)

            if rchoice == 6:
                long_series()
                print("*" * 100)

            if rchoice == 7:
                long_movie()
                print("*" * 100)

        else:
            print("_" * 100)
            print(" " * 30 + "Exited successfully")
            print("_" * 100)
            return "break"
    except:
        print("_" * 100)
        print(" " * 30 + "Exited successfully")
        print("_" * 100)

def add_movie(movie_name, movie_dur, movie_cat):
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    params = (movie_name, movie_dur, movie_cat)
    cursor.execute("INSERT INTO tb_movies (NAME, DURATION, CATEGORY) VALUES (?,?,?)", params)
    conn.commit()
    print('MOVIE ADDED!')
    print("*" * 100)
    conn.close()


def add_series(series_name, series_season, series_cat):
    conn = sqlite3.connect('streamingCatalogSystem.db')
    cursor = conn.cursor()
    params = (series_name, series_season, series_cat)
    cursor.execute("INSERT INTO tb_series (NAME, NO_OF_SEASON, CATEGORY) VALUES (?,?,?)", params)
    conn.commit()
    print('SERIES ADDED!')
    print("*" * 100)
    conn.close()


def movie_cat_list():
    conn = sqlite3.connect('streamingCatalogSystem.db')
    movie = pd.read_sql("select * from tb_movies", con=conn)
    movie_category = movie.CATEGORY
    movie_category.drop_duplicates(inplace =True)
    report1 = pd.DataFrame(movie_category)
    position_r1 = []
    for i in range(report1.size):
        position_r1.append(i + 1)
    report1['Item'] = position_r1
    print(report1)
    conn.close()

def series_cat_list():
    conn = sqlite3.connect('streamingCatalogSystem.db')
    series = pd.read_sql("select * from tb_series", con=conn)
    series_category = series.CATEGORY
    series_category.drop_duplicates(inplace=True)
    report2 = pd.DataFrame(series_category)
    position_r2 = []
    for i in range(report2.size):
        position_r2.append(i + 1)
    report2['Item'] = position_r2
    print(report2)
    conn.close()

def movies_booked():
    conn = sqlite3.connect('streamingCatalogSystem.db')
    mov = pd.read_sql("select * from tb_userdata WHERE TYPE_SHOW = 'movie'", con=conn)
    booked_movies = mov.SHOW_NAME
    booked_movies.drop_duplicates(inplace=True)
    report3 = pd.DataFrame(booked_movies)
    position_r3 = []
    for i in range(report3.size):
        position_r3.append(i + 1)
    report3['Item'] = position_r3
    print(report3)

    conn.close()

def SERIES_booked():
    conn = sqlite3.connect('streamingCatalogSystem.db')
    SER = pd.read_sql("select * from tb_userdata WHERE TYPE_SHOW = 'series'", con=conn)
    booked_series = SER.SHOW_NAME
    booked_series.drop_duplicates(inplace=True)
    report4 = pd.DataFrame(booked_series)
    position_r4 = []
    for i in range(report4.size):
        position_r4.append(i + 1)
    report4['Item'] = position_r4
    print(report4)
    conn.close()

def user_list():
    conn = sqlite3.connect('streamingCatalogSystem.db')
    user_li = pd.read_sql("select * from tb_user", con=conn)
    list_user = user_li.LOGIN
    report5 = pd.DataFrame(list_user)
    position_r5 = []
    for i in range(report5.size):
        position_r5.append(i + 1)
    report5['Item'] = position_r5
    print(report5)
    conn.close()

def long_series():
    conn = sqlite3.connect('streamingCatalogSystem.db')
    longser = pd.read_sql("select * from tb_series where NO_OF_SEASON > 3", con=conn)
    long_ser = longser.NAME
    report6 = pd.DataFrame(long_ser)
    position_r6 = []
    for i in range(report6.size):
        position_r6.append(i + 1)
    report6['Item'] = position_r6
    print(report6)
    conn.close()

def long_movie():
    conn = sqlite3.connect('streamingCatalogSystem.db')
    longmov = pd.read_sql("select * from tb_movies where DURATION > 120", con=conn)
    long_mov = longmov.NAME
    report7 = pd.DataFrame(long_mov)
    position_r7 = []
    for i in range(report7.size):
        position_r7.append(i + 1)
    report7['Item'] = position_r7
    print(report7)
    conn.close()


if __name__ == "__main__":
    sql_database()
    try:
        while True:
            code = app()
            if code == "break":
                break
    except:
        print("_" * 100)
        print(" " * 30 + "Exited successfully")
        print("_" * 100)
        while True:
            code = app()
            if code == "break":
                break