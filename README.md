// please change this if any changes
// see requirements.txt for installation purposes

database:
db = project
Idhar username and password apna daal dena
username = root
password = test

table 1 = login
user varchar(255) not null primarykey
pass varchar(255) not null

table 2 = property
plotid int pk nn
ownername varchar(255) nn
size int nn
price int nn
rating int nn
typeofhouse varchar(20) nn

// below this tumko banana hai
// while adding path to the db for images make sure to use \\ instead of \ for path
table 3 - image
user_id varchar(255) nn pk (user id argv se aajayega in photos.py tujhe bas db se display karna hai) 
image1 largeblob nn
image2 largeblob nn
image3 largeblob nn
image4 largeblob nn
image5 largeblob nn
