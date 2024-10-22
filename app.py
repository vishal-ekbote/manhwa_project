import os

import pymysql
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Get database credentials from environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Database configuration
db_config = {
    'host': db_host,
    'user': db_user,
    'password': db_password,
    'database': db_name
}


@app.route('/', methods=['GET', 'POST'])
def index():
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        search_query = request.form.get('search', '')
        if search_query:
            sql = "SELECT * FROM manhwa WHERE title LIKE %s OR genre LIKE %s"
            cursor.execute(sql, ('%' + search_query + '%', '%' + search_query + '%'))
        else:
            cursor.execute("SELECT * FROM manhwa")
    else:
        cursor.execute("SELECT * FROM manhwa")

    manhwa_list = cursor.fetchall()
    connection.close()
    return render_template('index.html', manhwa_list=manhwa_list)


if __name__ == '__main__':
    app.run(debug=True)
