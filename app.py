from flask import Flask, request, jsonify
import mysql.connector


db_config = {
    'user': 'vsbec',
    'password': 'Vicky@0717',  # Replace with your MySQL password
    'host': 'vsbec.mysql.pythonanywhere-services.com',
    'database': 'vsbec$users',  # Replace with your MySQL database name
    'port': 3306,  # Default MySQL port
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

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
    cursor.execute(query, (email))
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

    query = "INSERT INTO users (email,password) VALUES (%s,%s)"
    cursor.execute(query, (email,password))
    connection.commit()

    return jsonify({"success":True})

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)