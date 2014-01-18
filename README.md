#BashBook
Hastily constructed in-terminal social network written in python and (hopefully) node.js

Made for M-Hacks


##Users:
 - Avatar 
 - ID
 - Name

 - Age
 - Location
 - Website
 - Other social networks (twitter, facebook, github)

 - Interests
 - Friends (1 way links)

##Text Posts:
 - User (by ID)
 - Text Content
 - Post Date
 - Comment on post (at location, mood, etc.)
 - Tags

 - Links?

##Chat:
 - This is totally optional if we have time (which we won't)

 ##list of server interactions:
 - login (user ID, pw)
 	- respond with yes/no

 - request list of posts (boolean filter by user)
 	-defaults to filter by people on the user's friend list
 	-responds with a list of posts or a request deinied

 - request user
 	-respond with user

 - comment on post
 	-respond with pass/fail, new post object

 - request user
 	-respond with user
