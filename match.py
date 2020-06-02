import face_recognition,os,mysql.connector,time
from datetime import datetime,date
from time import strptime
import numpy as np

# Getting save images list
user_dir = "Users"
get_path = os.listdir(user_dir)

#Getting capturing path 
today = str(date.today())
path = "Source/"+today
name_list = os.listdir(path)
full_list = [os.path.join(path,i) for i in name_list]
time_sorted_list = sorted(full_list, key=os.path.getmtime)
cap_path = [os.path.basename(i) for i in time_sorted_list]


userObj ={}
known_face_encodings=[]
known_face_names=[]


# Data base connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="face_rec"
    )

mycursor = mydb.cursor()
# getting last face match of the database
mycursor.execute("SELECT Image_id FROM `attendance` WHERE In_time="+today+" ORDER BY Image_id DESC LIMIT 1") 
myresult = mycursor.fetchall()

ending_point = 0
for row in myresult:
        ending_point=row[0]

#Getting saved face images 
for x in get_path:
    known_face_names.append(x)
    userObj[x] = face_recognition.face_encodings(face_recognition.load_image_file("Users/"+x))[0]
    known_face_encodings.append(userObj[x])
count=1;

# getting capturing source images
for cap_img in cap_path:
    
    if(ending_point<count):
        unknown_image = face_recognition.load_image_file("Source/"+today+"/"+cap_img)

        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            # Finding best matches
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                
            # removing file extantion
            user_name=os.path.splitext(name)[0]
            # array form
            ImageData=cap_img.split(',')
            
            # Getting time and date
            created=time.ctime(os.path.getctime("Source/"+today+"/"+cap_img))
            get_time=created.split(" ")
            
            # time converting - this :
            current_time=get_time[3]
            month=str(strptime(get_time[1],'%b').tm_mon)
            # print(get_time)
            # removing file extantion
            dateTime=get_time[3]+'-'+month+'-'+get_time[5]+'  '+get_time[4]
            print(user_name,ImageData[0],dateTime)
            
            # Insert into database
            sql = "INSERT INTO attendance (Image_id,Emp_name, In_time) VALUES (%s, %s,%s)"
            val = (ImageData[0],user_name,dateTime)
            mycursor.execute(sql, val)
            mydb.commit()
    
    
    count+=1     


