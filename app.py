from typing import Type
import mysql.connector
from flask import Flask, render_template, redirect, request, url_for, Response, jsonify
import logging
import sys
import cv2
app = Flask(__name__)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="counting_ststem"
)
mycursor = mydb.cursor()


@app.route("/")
def index():
    # con=mydb.connection.cursor()
    sql = "SELECT * FROM faculty"
    mycursor.execute(sql)
    res = mycursor.fetchall()
    # print(res)
    sql = "SELECT sum(num_of_graduates) FROM `faculty`"
    mycursor.execute(sql)
    facsum = mycursor.fetchall()

    sql = "select p.timeDelay,p.left,p.right  from `parameter` p"
    mycursor.execute(sql)
    side = mycursor.fetchall()
    # print(rows)
    return render_template("index.html", datas=res, facsum=facsum, side=side)


@ app.route('/update', methods=['POST'])
def update():
    facId = request.form["facId"]
    Id = request.form["Id"]
    fac = request.form["fac"]
    department = request.form["department"]
    num = request.form["num"]
    sql = "UPDATE `faculty` SET `fac_id`=%s,`fac_name`=%s,`department`=%s,`num_of_graduates`=%s WHERE fac_id = %s"
    val = [facId, fac, department, num, Id]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("index"))


@ app.route("/update_left", methods=['GET', 'POST'])
def left():
    left = request.form["left"]
    sql = "UPDATE `parameter` SET `left`= %s"
    val = [left]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("index"))


@ app.route("/update_right", methods=['GET', 'POST'])
def right():
    right = request.form["right"]
    sql = "UPDATE `parameter` SET `right`= %s"
    val = [right]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("index"))


@ app.route("/delaytime", methods=['GET', 'POST'])
def delaytime():
    delaytime = request.form["delaytime"]
    sql = "UPDATE `parameter` SET `timeDelay`= %s"
    val = [delaytime]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("index"))


@ app.route("/insert_fac", methods=['GET', 'POST'])
def insert_fac():
    try:
        if request.method == "POST":
            facId = request.form["facId"]
            fac = request.form["fac"]
            department = request.form["department"]
            num = request.form["num"]
            sql = "INSERT INTO `faculty`(`fac_id`, `fac_name`, `department`, `num_of_graduates`) VALUES (%s,%s,%s,%s)"
            val = [facId, fac, department, num]
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        else:
            print("NOT SUCCESS")
    except Exception as e:
        return jsonify({'error': 'Missing data!'})
    return redirect(url_for("index"))


# @ app.route('/process', methods=['POST'])
# def process():

#     email = request.form['email']
#     name = request.form['name']

#     if name and email:
#         newName = name[::-1]

#         return jsonify({'name': newName})

#     return jsonify({'error': 'Missing data!'})
# @app.route("/insert", methods=['GET', 'POST'])
# def insert():
#     if request.method == "POST":
#         Time = request.form["Time"]
#         if Time == '':
#             print("hi")
#         else:
#             left = request.form["left"]
#             right = request.form["right"]
#             sql = "UPDATE `timedelay` SET `TimeDelay`=(%s),`left`=(%s),`right`=(%s) WHERE 1"
#             val = [Time, left, right]
#             mycursor.execute(sql, val)
#             mydb.commit()
#             print(mycursor.rowcount, "record inserted.")
#     else:
#         print("NOT SUCCESS")

#     return redirect(url_for("index"))


@ app.route('/delete/<string:id_data>', methods=['GET'])
def delelte(id_data):
    mycursor.execute("DELETE FROM `faculty` WHERE  fac_id = " + (id_data))
    mydb.commit()
    return redirect(url_for("index"))


@ app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


    # Video streaming route. Put this in the src attribute of an img tag
camera = cv2.VideoCapture(0)
switch = 1
selectcamera = 1


def gen_frames():
    sql = "select p.left,p.right from `parameter` p"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    left = 0
    right = 0
    for parameter in myresult:
        left = parameter[0]
        right = parameter[1]
        print(left, right)
    while True:
        success, frame = camera.read()  # read the camera frame
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        cv2.line(frame, (frameWidth//2 - left, 0),
                 (frameWidth//2 - left, frameHeight), (0, 255, 255), 2)
        cv2.line(frame, (frameWidth//2 + right, 0),
                 (frameWidth//2 + right, frameHeight), (0, 255, 255), 2)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@ app.route('/requests', methods=['POST', 'GET'])
def tasks():
    global switch, camera, selectcamera
    print(left, " ", right)
    if request.method == 'POST':
        if request.form.get('stop') == 'Start/Stop':
            if(switch == 1):
                switch = 0
                camera.release()
                cv2.destroyAllWindows()
            else:
                camera = cv2.VideoCapture(0)
                switch = 1
            return redirect(url_for("index"))
        elif request.form.get('camera') == 'camera':
            if(selectcamera == 1):
                camera = cv2.VideoCapture(selectcamera)
                selectcamera = 0
            else:
                camera = cv2.VideoCapture(selectcamera)
                selectcamera = 1
            return redirect(url_for("index"))
        return redirect(url_for("index"))


@ app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text


if __name__ == "__main__":
    app.run(debug=True)
