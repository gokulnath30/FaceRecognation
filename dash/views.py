from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import mysql.connector
import numpy as np
import cv2

# Data base connection

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="face_rec"
    )
mycursor = mydb.cursor()


def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request,'index.html')

def ViewHistory(request):
    
    return render(request,'ViewHistory.html',{'name':'gokul'})

        
def user_details(request):
    if request.method == 'POST':
        user_img=request.POST["User_name"]+'.png'
        uploaded_file = request.FILES['profile_img']
        fs = FileSystemStorage()
        fs.save(user_img, uploaded_file)
        

        
        # Insert into database
        sql = "INSERT INTO user_details (name, email,DOB,department,profile_image) VALUES (%s, %s, %s, %s, %s)"
        val = (request.POST["User_name"],request.POST["User_email"],request.POST["user_dob"],request.POST["User_dep"],user_img)
        mycursor.execute(sql, val)
        mydb.commit()
        
    return render(request, "index.html")