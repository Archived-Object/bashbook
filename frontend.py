import curses, curses.textpad
import time, math, sys, textwrap, threading
import serverio
from definitions import *

#window object, global because curses
window = None
logged_in_user = None

#these are dictionaries of data that would normally be populated by server
#because this is GUI, putting it here.
online_friends = []
users = {}
posts = {}
comments = {}

scroll_y=0
chat_scroll_y=0
chat_select_y =0
chat_height = 0
focus = ""

chat_focus = ">Chat Mode"
feed_focus = ">Feed Mode"

#this function does the splash scren, will be used again when we actually need to connect to a server
def startup():
	curses.noecho()
	curses.curs_set(0)
	window.border(0)
	window.addstr(12, 25, "Pretending to connect...")
	window.refresh()
	#time.sleep(0.5)
	window.addstr(12, 25, "        Connected         ")
	#time.sleep(0.5)
	#window.getch()

	#curses.curs_set(1)

#fakes a login - grabs information about buddies, currently online friends
def login():
	global logged_in_user, users, online_friends
	logged_in_user = User(
		0,"Max",18,"Toronto",
		["maxwell.huang-hobbs.com"],["FUCKING NOTHING"],[])
	users[0] = logged_in_user
	for friend in serverio.get_friends(logged_in_user):
		users[friend.uid] = friend

	online_friends = serverio.get_online_friends(logged_in_user)
	#checker=ContinuousChecker() rand into trouble with live-updating threads. Is curses not threadsafe? ;_;
	#checker.start()

	update_posts(0)

#pulls the most recent set of posts, from age fish-depth and before
def update_posts(fish_depth):
	for post in serverio.get_recent_posts(logged_in_user, fish_depth):
		if(post.post_id not in posts.keys()):
			posts[post.post_id] = post

			for cid in post.comment_ids:
				if not cid in comments.keys():
					comments[cid] = serverio.get_comment_by_id(logged_in_user, cid)

#gets the username of the person who made a post or comment
def get_username(post):
	return users[post.creator_uid].name

# prints a neat block of text with a seperate section for
#the body
def printblock(x, y, width, header, body):
	disp_width = width - 6
	by = y+len(textwrap.wrap(body, disp_width))+3;

	if( y>=0 and by< window.getmaxyx()[0]-1):
		curses.textpad.rectangle(window, y, x, by, x + width)
		window.addstr(y+1, x+2, header)

		#prints the body of the text post
		wtext = textwrap.wrap(body, disp_width)
		for line in range(len(wtext)):
			window.addstr(y+2+line, x+5, wtext[line])
	return by


#redraws the scroll (think newsfeed) and chat areas, then
#refreshes the result to console window (double-buffered)
def redraw_both(return_chat = True):
	window.clear()
	c = redraw_chat(chat_scroll_y)
	s = redraw_scroll(scroll_y)
	window.addstr(window.getmaxyx()[0]-1 ,0 , focus)
	window.clrtoeol()
	window.refresh()
	return c if return_chat else s

#redraws the scroll, offset by scrolly columns.
#Does not draw boxes that are partially off screen. (abusable?)
#does not update the console window
def redraw_scroll(scrolly):
	#redraw scroll
	post_x  = 3
	post_width = window.getmaxyx()[1]-33
	count_y=0
	for i in range(len(posts)):
		post = posts[i]

		count_y = printblock(
			post_x, count_y-scrolly ,post_width,
			get_username( post),
			post.text_content) +1 +scrolly
		for c in range(len(post.comment_ids)):
			count_y = printblock(
					post_x+5, count_y-scrolly, post_width-5,
					get_username( comments[post.comment_ids[c]] ),
					comments[post.comment_ids[c]].text_content) +1 +scrolly

	return count_y

#redraws the chat section.
#does not update the console window
def redraw_chat(chaty):

	curses.textpad.rectangle(window, 0, window.getmaxyx()[1]-28, 2, window.getmaxyx()[1]-1)
	curses.textpad.rectangle(window, 0, window.getmaxyx()[1]-28, 2, window.getmaxyx()[1]-1)
	window.addstr(1, window.getmaxyx()[1]-27, "Online Friends")

	curses.textpad.rectangle(window, 3, window.getmaxyx()[1]-28, window.getmaxyx()[0]-2, window.getmaxyx()[1]-1)

	i=0
	for friendid in online_friends[chat_scroll_y:min(len(online_friends),chat_scroll_y+chat_height)]:
		i+=1
		friend = users[friendid]
		window.addstr(
			3+i, window.getmaxyx()[1]-25,
			("(%04d)"%(friend.uid) +" "+ friend.name[0:min(len(friend.name),14)] +
				("..." if  len(friend.name)>14 else (friend.name[-3:-1] if len(friend.name)>14 else "") ))
		)

	if(focus == chat_focus):
		window.addstr(4+chat_select_y-chat_scroll_y, window.getmaxyx()[1]-27, ">")


	return chaty

#switches between scroll_interface and chat_interface methods,
#and changes the value of "focus" (the thing in the bottom left)
def main_interface():
	window.clear()
	redraw_both()
	window.refresh()
	global focus
	while(True):
		focus=feed_focus
		scroll_interface()
		focus=chat_focus
		chat_interface()

#controls the behavior of the newsfeed section
def scroll_interface():
	global scroll_y
	maxheight = redraw_both(False)
	while True:
		s = window.getkey()
		if (s == "k" and scroll_y<=maxheight-window.getmaxyx()[0]):
			scroll_y += 1
			maxheight = redraw_both(False)
		if (s == "j" and scroll_y>0):
			scroll_y -= 1
			maxheight = redraw_both(False)
		if s == "	":
			break
		if s=="\n":
			pass #TODO make post
		if s==":":
			command_interface()

#controls the behavior of the chat section
def chat_interface():
	global chat_scroll_y, chat_select_y
	redraw_both(True)
	maxheight = redraw_both(True)
	while True:
		s = window.getkey()
		if s == "j" and chat_select_y>0:
			chat_select_y-=1
		if s == "k":
			chat_select_y+=1
		elif s == "	":
			break
		elif s=="\n":
			pass #TODO chat invites
		elif s==":":
			command_interface()

		if(chat_select_y>= len( online_friends)):
			chat_select_y = len(online_friends)-1

		if ( chat_select_y>=chat_scroll_y + chat_height):
			chat_scroll_y += 1
		elif (chat_select_y<chat_scroll_y):
			chat_scroll_y -= 1

		maxheight = redraw_both(True)

#controls the behavior of the command section
#this is the section where you type things in a 
#console w/in console
def command_interface():
	window.addstr(window.getmaxyx()[0]-1 ,0 , ":")
	window.refresh()
	window.clrtoeol()
	command = ""
	while True:
		s = window.getkey()
		if s == "	":
			break
		elif s == "\n":
			handle_command(command)
			command = ""
		elif s == "\b" and len(command)>=1:
			command = command[0:-1]
		elif s==":":
			command=""
		else:
			command = command + s
		window.addstr(window.getmaxyx()[0]-1 ,1 , command)
		window.clrtoeol()
		window.refresh()
	redraw_both()
	window.refresh()

#handles the commands coming out of command_interface
def handle_command(command):
	command = command.split(" ")
	if command[0] == "quit":
		curses.endwin()
		sys.exit(0)
	elif command[0] == "chat":
		try:
		    int(command[1])
		    if(int(command[1]) in online_friends):
		    	personal_chat_interface(command[1])
		    else:
		    	window.addstr(window.getmaxyx()[0]-2 ,1 , "user with id %i not online"%(command[1]))
		except ValueError:
			for friend in [users[x] for x in online_friends]:
				if(command[1] == friend.name):
					personal_chat_interface(friend.uid)
					return
			window.addstr(window.getmaxyx()[0]-2 ,1 , "user %s not online"%(command[1]))
	elif command[0] == "post":
		make_post_interface()
	else:
		window.addstr(window.getmaxyx()[0]-2 ,1 , "Unknown command '%s'. type 'list' for a list of valid commands"%(command[0]))


if __name__ == "__main__":
	window = curses.initscr()
	chat_height = window.getmaxyx()[0]-7

	startup()
	login()

	main_interface()

	curses.endwin()