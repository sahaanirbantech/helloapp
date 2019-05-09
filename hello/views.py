from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date, datetime
from .models import Hello
from .serializers import HelloSerializer
import json
from django.db import connection
from django.http import HttpResponse

def health_check(request):
    with connection.cursor() as cursor:
        cursor.execute("select 1")
        one = cursor.fetchone()[0]
        if one != 1:
            raise Exception('The site did not pass the health check')
    return HttpResponse("ok")

@api_view(['GET', 'PUT'])
def get_put_username(request, uname):
    date_format = "%Y-%m-%d"
    date_today = date.today()

    if uname.isalpha():
        if request.method == 'GET':
            try:
                userdata = Hello.objects.get(username=uname)
                serializer = HelloSerializer(userdata)
    
                date_of_birth = datetime.strptime(serializer.data["date_of_birth"], date_format)
                td_bday_this_yr = datetime(date_today.year, date_of_birth.month, date_of_birth.day)
                td_bday_next_yr = datetime(date_today.year+1, date_of_birth.month, date_of_birth.day)
                td_today = datetime(date_today.year, date_today.month, date_today.day)
                bday_this_year = datetime.strptime(serializer.data["date_of_birth"], date_format).date().replace(year=date_today.year) 
    
                if date_today > bday_this_year:
                    days_to_birthday = (max(td_bday_this_yr, td_bday_next_yr) - td_today).days
                else:
                    days_to_birthday = (bday_this_year - date_today).days
                
                if date_today == bday_this_year: 
                    custom_response = {"message": "Hello " + uname + " ! Happy birthday !"}
                else:
                    custom_response = {"message": "Hello " + uname + " ! Your birthday is in " + str(days_to_birthday) + " day(s)"}
    
                return Response(json.loads(json.dumps(custom_response)), status=status.HTTP_200_OK)
            except Hello.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    
        if request.method == 'PUT':
            dob_entered = datetime.strptime(request.data.get('dateOfBirth'), date_format).date()
    
            if dob_entered < date_today:
                data = {
                    'username': uname,
                    'date_of_birth': request.data.get('dateOfBirth'),
                }
                serializer = HelloSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                custom_response = {"message":"The date of birth entered is in the future"}
                return Response(json.loads(json.dumps(custom_response)), status=status.HTTP_400_BAD_REQUEST)
    else:
        error_message = {"message":"The provided username is invalid, only letters are accepted!"}
        return Response(json.loads(json.dumps(error_message)), status=status.HTTP_400_BAD_REQUEST)
