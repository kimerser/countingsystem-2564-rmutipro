from typing import Type
from flask import Flask, render_template, redirect, request, url_for, Response, jsonify
import logging
# import sys
import cv2
app = Flask(__name__)


# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="counting_ststem"
# )
# mycursor = mydb.cursor()


@app.route("/")
def index():
    #     # con=mydb.connection.cursor()
    #     sql = "SELECT * FROM faculty"
    #     mycursor.execute(sql)
    #     res = mycursor.fetchall()
    #     # print(res)
    #     sql = "SELECT sum(num_of_graduates) FROM `faculty`"
    #     mycursor.execute(sql)
    #     facsum = mycursor.fetchall()

    #     sql = "select p.timeDelay,p.left,p.right  from `parameter` p"
    #     mycursor.execute(sql)
    #     side = mycursor.fetchall()
    #     # print(rows)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
