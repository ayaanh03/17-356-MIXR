from django.shortcuts import render
import pyrebase


# Create your views here.
config = {
  "apiKey": "AIzaSyDOAMIg3T_NToCDwqhNRTXKWXCuaRn6O9Q",
  "authDomain": "mixr-17-356.firebaseapp.com",
  "databaseURL": "https://mixr-17-356-default-rtdb.firebaseio.com",
  "projectId": "mixr-17-356",
  "storageBucket": "mixr-17-356.appspot.com",
  "messagingSenderId": "1097388094664",
  "appId": "1:1097388094664:web:254cf663cf38fc773d21fd",
  "measurementId": "G-V5QVSSZ5DK"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()

def mixr(request):
    print(database.get().val())

    return render(request,"Home.html",{"testval": database.get().val()})