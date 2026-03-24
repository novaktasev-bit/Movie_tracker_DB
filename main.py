import sqlite3

connection = sqlite3.connect("movie_database.db")
cursor = connection.cursor()

cursor.execute ( 
    """
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT,
        release_year INTEGER,
        rating REAL
    )
    """
    )

running = True

while running:
    print ("\n === MOVIE TRACKER MENU ===")
    print("1. ADD A NEW MOVIE")
    print ("2. VIEW ALL MOVIES")
    print ("3. SEARCH")
    print ("4. DELETE MOVIE")
    print ("5. UPDATE RATING")
    print ("6. EXIT ")

    choice = input ("Select an option (1-6): ")

    if choice == "1":
        try:
            user_title = input("Please enter title: ")
            user_year = int(input("Please enter release year: "))
            user_rating = float(input("Please enter rating: "))

            query = "INSERT INTO movies (title,release_year,rating) VALUES (?,?,?)"
            data = (user_title,user_year,user_rating)

            cursor.execute(query,data)
            connection.commit()
            print("Movie saved successfully!")

        except ValueError:
            print("ERROR: Please enter numbers only for year and rating!")
            continue

    
    elif choice == "2":
        cursor.execute("SELECT * FROM movies")
        all_movies = cursor.fetchall()

        print("\n" + "="*40)
        print("YOUR MOVIE COLECTION")
        print("="*40)
        for movie in all_movies:
            print(f"ID: {movie[0]} | TITLE: {movie[1]} | YEAR: {movie[2]} | RATING: {movie[3]}")

    elif choice == "6":
        running = False
        print ("Goodbye!")

    elif choice == "4":
        try:
            delete_id=int(input("Enter movie ID to delete: "))

            cursor.execute("SELECT title FROM movies WHERE ID = ?",(delete_id,))
            result = cursor.fetchone()

            if result:
                movie_name = result[0]



                query = "DELETE FROM movies WHERE ID = ?"
                cursor.execute(query,(delete_id,))
                connection.commit() 

                print(f"Movie {movie_name} with ID number {delete_id} has been deleted.")

            else:
                print("Wrong ID, please enter a valid ID number")
        
        except ValueError:
            print("Please enter valid ID number.")

    elif choice == "5":
            try:
                rating_update = int(input("Please enter movie ID to update rating: "))
                cursor.execute("SELECT title FROM movies WHERE ID = ?",(rating_update,))
                result = cursor.fetchone()
                
                if result:
                    movie_name = result[0]
                    
                    new_rating = float(input(f"Enter new rating for movie {movie_name}: "))

                    query = "UPDATE movies SET rating = ? WHERE id = ?"
                    cursor.execute(query,(new_rating, rating_update))
                    connection.commit()

                    print(f"Rating of movie: {movie_name} is updated to {new_rating}.")

                else :
                    print("Please enter valid ID number.")

            except ValueError:          
                print("Please enter valid ID number.")

    elif choice == "3":
        search = input ("Please enter the name of movie: ")
        formatted_search = f"%{search}%"
        cursor.execute("SELECT * FROM movies WHERE title LIKE ?",(formatted_search,))
        results = cursor.fetchall()

        if results:
            print("\n =====Movies found: =====")
            for m in results:
                print(f"ID: {m[0]} | Title: {m[1]} | Release Year: {m[2]} | Rating: {m[3]}")

        else:
            print(f"No movies found with {search}.")


    else:
        print("Invalid choice, please try again.")
connection.close()
