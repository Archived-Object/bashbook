import curses, curses.textpad
import time, math
import serverio
from definitions import *
import textwrap

#window object, global because curses
window = None
logged_in_user = None

#these are dictionaries of data that would normally be populated by server
#because this is GUI, putting it here.
online_friends = {}
users = {}
posts = {}
comments = {}

scroll_y=0
chat_y=0


def get_username(post):
	return users[post.creator_uid].name


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

def login():
	global logged_in_user, users
	logged_in_user = User(0,"Max",18,"Toronto",["maxwell.huang-hobbs.com"],["FUCKING NOTHING"],[])
	users[0] = logged_in_user
	for friend in serverio.get_friends(logged_in_user):
		users[friend.uid] = friend

	update_posts(0)

def update_posts(fish_depth):
	for post in serverio.get_recent_posts(logged_in_user, fish_depth):
		if(post.post_id not in posts.keys()):
			posts[post.post_id] = post

			for cid in post.comment_ids:
				if not cid in comments.keys():
					comments[cid] = serverio.get_comment_by_id(logged_in_user, cid)


def printblock(x, y, width, header, body):
	disp_width = width - 5
	by = y+len(textwrap.wrap(body, disp_width))+3;

	if( y>=0 and by< window.getmaxyx()[0]-1):
		curses.textpad.rectangle(window, y, x, by, x + width)
		window.addstr(y+1, x+2, header)

		#prints the body of the text post
		wtext = textwrap.wrap(body, disp_width)
		for line in range(len(wtext)):
			window.addstr(y+2+line, x+5, wtext[line])
	return by


def redraw_both( return_chat):
	window.clear()
	window.refresh()
	chat = redraw_chat(chat_y)
	scroll = redraw_scroll(scroll_y)
	return chat if return_chat else scroll

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

	window.refresh()
	return count_y

def main_interface():
	redraw_both(True)
	while(True):
		scroll_interface()
		chat_interface()
		control_interface()

def redraw_chat(chaty):
	curses.textpad.rectangle(window, 0, window.getmaxyx()[1]-28, 2, window.getmaxyx()[1]-1)
	window.addstr(1, window.getmaxyx()[1]-27, "Online Friends")

	curses.textpad.rectangle(window, 3, window.getmaxyx()[1]-28, window.getmaxyx()[0]-2, window.getmaxyx()[1]-1)

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

def chat_interface():
	global chat_y
	window.clear()
	curses.textpad.rectangle(window, y, x, by, x + width)
	window.refresh()
	maxheight = redraw_both(True)
	while True:
		s = window.getkey()
		if (s == "k" and chat_y<=maxheight-window.getmaxyx()[0]):
			chat_y += 1
			maxheight = redraw_both(True)
		if (s == "j" and chat_y>0):
			chat_y -= 1
			maxheight = redraw_both(True)


if __name__ == "__main__":
	window = curses.initscr()

	startup()
	login()

	main_interface()

	curses.endwin()