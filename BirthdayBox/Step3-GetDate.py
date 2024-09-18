import datetime
import dotenv

from dotenv import set_key
from dotenv import dotenv_values

envFile = "mount/.env"
config = dotenv_values(envFile)

# The string to be parsed
previous_run = config["Step3.LastExecutionDate"]
if previous_run == "":
    previous_run = str(datetime.datetime.now())
    set_key(envFile, key_to_set="Step3.LastExecutionDate", value_to_set=previous_run)

previous_run_datetime = datetime.datetime.strptime(previous_run, "%Y-%m-%d %H:%M:%S.%f")
starttime_formatted = previous_run_datetime.strftime('%Y-%m-%dT%H:%M:%S.000-04:00')

now_datetime = datetime.datetime.now()
endtime_formatted = now_datetime.strftime('%Y-%m-%dT%H:%M:%S.000-04:00')

output={'startTime':starttime_formatted, 'endTime':endtime_formatted }

#Temporary Override!!!
if config["Step3.Testing.OverrideDate"] == "True":
    output={'startTime':"2024-08-11T00:00:00.000-04:00",'endTime':"2024-10-10T23:59:59.999-04:00"}

print(str(datetime.datetime.now()) + " "+ __file__ + " StartTime: "+output["startTime"])
print(str(datetime.datetime.now()) + " "+ __file__ + " EndTime: "+output["endTime"])
set_key(envFile, key_to_set="startTime", value_to_set=output["startTime"])
set_key(envFile, key_to_set="endTime", value_to_set=output["endTime"])
set_key(envFile, key_to_set="Step3.LastExecutionDate", value_to_set=str(now_datetime))
print(str(datetime.datetime.now()) + " "+ __file__ + " completed")