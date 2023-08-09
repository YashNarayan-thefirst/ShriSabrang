import requests
import re
import mysql.connector

def search_database(search_string):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="website_data_db"
        )

        cursor = db.cursor()

        search_query = "SELECT * FROM website_data WHERE title LIKE %s OR content LIKE %s"
        cursor.execute(search_query, ('%' + search_string + '%', '%' + search_string + '%'))
        search_results = cursor.fetchall()

        if search_results:
            return search_results[0]
        else:
            return ("No matching data found.")

    except Exception as e:
        print("An error occurred:", e)
    finally:
        # Close the database connection
        if db.is_connected():
            cursor.close()
            db.close()

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )

    cursor = db.cursor()

    # Create a database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS website_data_db")
    cursor.execute("USE website_data_db")

    # Create a table to store website data
    create_table_query = "CREATE TABLE IF NOT EXISTS website_data (title VARCHAR(255), content TEXT);"
    cursor.execute(create_table_query)

    # Define the URL to the website
    url = r"https://www.g20.org/en/about-g20/#overview"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Use regular expressions to extract titles and content
        pattern = r'<h2.*?>(.*?)<\/h2>.*?<p.*?>(.*?)<\/p>'
        matches = re.findall(pattern, response.text, re.DOTALL)

        for match in matches:
            title = match[0]
            content = match[1]

            # Insert data into the database
            insert_query = "INSERT INTO website_data (title, content) VALUES (%s, %s)"
            data = (title, content.strip())
            cursor.execute(insert_query, data)
            db.commit()

            print(f"Inserted data: Title='{title}', Content='{content[:50]}...'")

    else:
        print("Request failed with status code:", response.status_code)

    # Perform a search
    search_string = input("Enter a search string: ")
    search_database(search_string)

except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the database connection
    if db.is_connected():
        cursor.close()
        db.close()
