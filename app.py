from flask import Flask, request, jsonify
import mysql.connector
import psycopg2

# db_config = {
#     'user': 'vsbec',
#     'password': 'Vicky@0717',  # Replace with your MySQL password
#     'host': 'vsbec.mysql.pythonanywhere-services.com',
#     'database': 'vsbec$users',  # Replace with your MySQL database name
#     'port': 3306,  # Default MySQL port
# }

# connection = mysql.connector.connect(**db_config)
# cursor = connection.cursor()


db_config = {
    'dbname': 'verceldb',    # Replace with your PostgreSQL database name
    'user': 'default',      # Replace with your PostgreSQL username
    'password': 'Bk8ROoUayC2m',  # Replace with your PostgreSQL password
    'host': 'ep-spring-silence-a136eckp-pooler.ap-southeast-1.aws.neon.tech',          # Replace with your PostgreSQL host address
    'port': '5432',          # Replace with your PostgreSQL port
}

# Establish PostgreSQL connection
connection = psycopg2.connect(**db_config)
cursor = connection.cursor()

# query = "INSERT INTO users (email,password) VALUES (%s,%s) RETURNING id"
# cursor.execute(query, ("vignesh","123",))

# res = cursor.fetchone()
# print(res)

if(connection):
    print("DB Connected")
    # query = "INSERT INTO users (email,password) VALUES (%s,%s) RETURN id"
    # cursor.execute(query, ("test","test"))
    # print(cursor.fetchone())
    # connection.commit()

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    query = "SELECT password from users where email = %s"
    cursor.execute(query, (email,))
    res = cursor.fetchone()
    if(res):
        if(res[0] == password):
            return jsonify({
                "success":True,
                "message":"Hi"
            })
        else:
            return jsonify({
                "success":False,
                "message":"Password Incorrect"
            })
    else:
        return jsonify({
            "success":False,
            "message":"User Not Exist"
        })

    

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success":False,
            "Message":"No Data"
        })

    query = "INSERT INTO users (email,password) VALUES (%s,%s) RETURNING id"
    cursor.execute(query, (email,password,))

    res = cursor.fetchone()
    connection.commit()

    return jsonify({"success":True})

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)
