import mysql.connector
import matplotlib.pyplot as plt
import numpy as np


movies = []
START = "\nEnter 'a' to add a movie, \n 'l' to see your movies, \n 'f' to find a movie by title, \n 'c' to see the chart, \n or 'q' to quit: "
USER = "\nEnter user id : "
PASSWORD = "\nEnter password : "



def db():

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      port='10005',
      database='movies',
      password="root"
    )
    return mydb

def add_movie():
    title = input("Enter title of the film: ")
    director = input("Enter director of the film: ")
    year = input("Enter year of the film: ")
    genre = input("Enter genre of the film: ")
    mydb = db()
    mycursor = mydb.cursor()
    
    sql = "INSERT INTO movies (movietitle, genre, director) VALUES (%s, %s, %s)"
    value = (title, genre, director)
    mycursor.execute(sql,value)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    movies.append({
        'title': title,
        'year': year,
        'director': director,
        'genre': genre
    })


def chart():
    mydb = db()
    mycursor = mydb.cursor()
    mycursor.execute("select genre, count(genre) as count from movies group by genre;")
    myresult = mycursor.fetchall()
    value = []
    label = []
    for x in myresult:
        value.append(x[1])
        label.append(x[0])
    
    y = np.array(value)
    
    plt.pie(y, labels=label)
    plt.show()

def list_movies():
    quantity = len(movies)
    titles = [movie['title'] for movie in movies]
    titles = ', '.join(titles)

    if quantity:
        print(f'You have following movies in collection: {titles}. In total you have {quantity} {"movie" if quantity == 1 else "movies"}.')
    else:
        print('There are no movies in you collection.')


def print_movie_info(movie):
    print('Here is information about requested title')
    print(f'Title: {movie["title"]},')
    print(f'Director: {movie["director"]},')
    print(f'Year: {movie["year"]},')
    print(f'Genre: {movie["genre"]}.')


def find_title():
    search_title = input('Enter title you are looking for: ')
    for movie in movies:
        if movie['title'] == search_title:
            print_movie_info(movie)
        else:
            print('Requested title was not found in the collection.')


user_selection = {
    'a': add_movie,
    'l': list_movies,
    'f': find_title,
    'c': chart
}


def menu():
    userid = input(USER)
    print("You have entered "+userid)
    password = input(PASSWORD)
    print("You have Password "+password)
    selection = input(START).lower()
    while selection != 'q':
        if selection in user_selection:
            selected_action = user_selection[selection]
            selected_action()
        else:
            print("Unknown command. Please choose within available options: 'a', 'f', 'l' or 'q' to close the app.")
        selection = input(START)
    print('Thank you for using the app. See you next time!')


if __name__ == '__main__':
    menu()
