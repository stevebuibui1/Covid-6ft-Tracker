So for starters, I took the approach of stretching the harscades out so that acts as bounding box. it is a little wonky considering the size of each ox detection but it gets the job done


 for tracking, I made a trail using a list of dots and aged them; that is how I tackled the tracking part. 

 for distance, I created a dot list that makes the a trail using those dots and when someone comes in contact with another person in a 50 pixel scale, they would violate SD thus outputing a red dot.

for counting I counted people by the number of bounding boxes used in method one which was pretty accurate considering that the boxes caught a person from far away.

lastly,  my Testt.mov is my input file

Ciao,
Steven Bui
