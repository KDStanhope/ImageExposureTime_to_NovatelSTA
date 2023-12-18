import exifread
from datetime import datetime
from datetime import timedelta  
import pytz
import gnsscal
import os, sys

local = pytz.timezone("Africa/Johannesburg")
image_list = []
event_dict = {}
# initial run population mode:
#time_offset_to_epoch = 169.823531
# second run 1500 population mode:
# Note possible ~1s time offset observed with lidar data too.
# time_offset_to_epoch = 159.902895
# second run 280 population mode:
# time_offset_to_epoch = 158.71
time_offset_to_epoch = 160

def utctoweekseconds(utc,leapseconds):
    """ Returns the GPS week, the GPS day, and the seconds 
        and microseconds since the beginning of the GPS week """
    import datetime, calendar
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
    tdiff = utc -epoch  + datetime.timedelta(seconds=leapseconds)
    gpsweek = tdiff.days // 7 
    gpsdays = tdiff.days - 7*gpsweek         
    gpsseconds = tdiff.seconds + 86400* (tdiff.days -7*gpsweek) 
    return gpsweek,gpsdays,gpsseconds,tdiff.microseconds

def get_moment_of_exposure(path):
    f = open(path,'rb')
    tags = exifread.process_file(f)
    local_time = tags['EXIF DateTimeOriginal'].values
    try:
        ms_component = int(tags['EXIF SubSecTimeOriginal'].values)
    except:
        ms_component = 0
    
    naive_dt = datetime.strptime(local_time, "%Y:%m:%d %H:%M:%S")
    
    local_dt = local.localize(naive_dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    utc_dt = utc_dt.replace(tzinfo=None)
    utc_dt = utc_dt + timedelta(milliseconds=ms_component)
    
    return utc_dt

def event_generator(event_dict):
    stations = open("stations.sta","w")
    stations.write('$STAINFO Ver 8.90.2428 OEM42GPB NovAtelOem4\n')

    for i in event_dict:
        stations.write("Mrk { \n")
        stations.write('\tEvent: "'+i+'"\n')
        stations.write('\tDesc: "CAMERA PULSE"\n')
        stations.write('\tGTim: '+str(event_dict[i][2])+' '+str(event_dict[i][0]))
        stations.write('\n}\n')
        
    stations.close()
        
def csv_for_epoch_establishment(event_dict):
    stations = open("stations.csv","w")

    for i in event_dict:
        stations.write(i+',')
        stations.write(str(event_dict[i][2]))
        stations.write('\n')
        
    stations.close()

        
# get a list of files
for i in os.listdir():
    if i.endswith(".NEF"):
        image_list.append(i)

#make a dict of the data and keep track
count = 0
for image in image_list:
    timing = get_moment_of_exposure(image)
    gpsweek,gpsdays,gpsseconds,gps_ms = utctoweekseconds(timing,18)
    event_dict[image]=[gpsweek,gpsdays,gpsseconds+time_offset_to_epoch+(gps_ms/100000)]
    count += 1
    print("File "+str(count)+" of "+str(len(image_list)))
          
csv_for_epoch_establishment(event_dict)
    
    
