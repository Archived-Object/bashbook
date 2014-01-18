#BashBook
Hastily constructed in-terminal social network written in python and (hopefully) node.js

Made for M-Hacks

Scrolling is mapped to j/k for scrolling up/down.
To make a post, press enter when in scroll mode (not implemented)
to enter a conversation, press enter when in chat mode (not implemented)
to go to the inner console line, type :

to exit the program, go to the inner console and type :quit


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
