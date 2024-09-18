import datetime
import dotenv
from dotenv import set_key
from dotenv import dotenv_values

envFile = "mount/.env"
config = dotenv_values(envFile)

#calculate the datetime as a one-off
now = datetime.datetime.now()
startDate_minutes_ago = now - datetime.timedelta(minutes=int(config["Step3.QueryMinutes"]))
startDateFormatted_datetime = startDate_minutes_ago.strftime('%Y-%m-%dT%H:%M:%S.000-04:00')
endDateFormatted_datetime = now.strftime('%Y-%m-%dT%H:%M:%S.000-04:00')

output={'startTime':startDateFormatted_datetime, 'endTime':endDateFormatted_datetime }

#Temporary Override!!!
if config["Step3.Testing.OverrideDate"] == "True":
    output={'startTime':"2024-09-11T00:00:00.000-04:00", 'endTime':"2024-10-10T23:59:59.999-04:00"}

print(str(datetime.datetime.now()) + " "+ __file__ + "StartTime: "+output["startTime"])
print(str(datetime.datetime.now()) + " "+ __file__ + "EndTime: "+output["endTime"])
set_key(envFile, key_to_set="startTime", value_to_set=output["startTime"])
set_key(envFile, key_to_set="endTime", value_to_set=output["endTime"])
print(str(datetime.datetime.now()) + " "+ __file__ + " completed")