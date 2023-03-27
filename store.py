import face_recognition
# import mysql.connector
import io
from PIL import Image
import os
import pyodbc

connection_string = 'Driver={SQL Server};Server=DESKTOP-CIRT352;Database=Face_recogntion;Trusted_Connection=yes;'

mydb = pyodbc.connect(connection_string)

mycursor = mydb.cursor()

path = r"C:\Users\iCore\PycharmProjects\Face_recognition\demo_images"

#  Loop through each file in the folder
for filename in os.listdir(path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Load the image file and get its encoding
        image_file = Image.open(os.path.join(path, filename))
        image_encoding = face_recognition.face_encodings(face_recognition.load_image_file(os.path.join(path, filename)))[0]

        # Convert image encoding to binary data
        image_binary = io.BytesIO()
        image_file.save(image_binary, format='JPEG')
        image_binary = image_binary.getvalue()

        encoding_binary = image_encoding.tobytes()

        # Insert the image and its encoding into the MySQL database
        sql = "INSERT INTO images (name, encoding, image) VALUES (?, ?, ?)"
        val = (filename, encoding_binary, image_binary)
        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted for", filename)
    else:
        print("Skipping file", filename, "as it is not a JPG or PNG")
