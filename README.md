# ImageExposureTime_to_NovatelSTA
Extracts the timestamps from image metadata and creates a .sta file

The scipt itself contains most of what you'll need to know. 

Usually, a camera is not syncronised with GPS time. In cases where there is no other choicebut to make a plan, this is that plan. 

You can determine the precise difference between the camera's time and the GPS time a number of ways. 
The most practical would be to extract the Camera time from a frame on an existing project and compare that to
timestamp of that EO event. This does not account for time drift on the Camera's RTC so additional work might be needed.

This is not as accurate as a GPS timestamp but it will be a life saver when you need it. 
