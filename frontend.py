import curses, curses.textpad
import time, math
import serverio
import textwrap

#window object, global because curses
window = None
logged_in_user = None

#these are dictionaries of data that would normally be populated by server
#because this is GUI, putting it here.
users = {}
posts = {}
comments = {}

class User():
	def __init__(self, uid, name, age, location, websites, interests, friends):
		(	self.uid, self.name, self.age, self.location,
			self.websites, self.interests, self.friends) = (
				uid, name, age, location, websites, interests, friends
			)

	def add_friend(self):
		curses.addstr(window.getmaxyx[0]-25, getmaxyx[1] ,"sending friend request.. ")
		window.refresh()
		if(self != logged_in_user and serverio.add_friend(self, logged_in_user) ):
			curses.addstr(window.getmaxyx[0]-25, getmaxyx[1] ,"friend request sent     ")
		else:
			curses.addstr(window.getmaxyx[0]-25, getmaxyx[1] ,"friend request failed to send")
		window.refresh()

class Post():
	def __init__(self, post_id, creator_uid, text_content, meta_content, comment_ids):
		(	self.post_id, self.creator_uid, self.text_content,
			self.meta_content, self.comment_ids) = (
				post_id, creator_uid, text_content,
				meta_content, comment_ids)

	def post_comment(self, comment_text):
		curses.addstr(window.getmaxyx[0]-25, getmaxyx[1] ,"posting comment...")
		window.refresh()
		if serverio.post_comment(self, logged_in_user, comment_text):
			curses.addstr(window.getmaxyx()[0]-25, getmaxyx[1] ,"Post successful     ")
		else:
			curses.addstr(window.getmaxyx()[0]-25, getmaxyx[1] ,"Post failed       ")
		window.refresh()

	def get_username(self):
		return users[self.creator_uid].name

class Comment():
	def __init__(self, comment_id, creator_uid, text_content):
		(self.comment_id, self.creator_uid, self.text_content) = (
			comment_id, creator_uid, text_content)

	def get_username(self):
		return users[self.creator_uid].name


def startup():
	curses.curs_set(0)
	window.border(0)
	window.addstr(12, 25, "Pretending to connect...")
	window.refresh()
	#time.sleep(0.5)
	window.addstr(12, 25, "        Connected         ")
	#time.sleep(0.5)
	#window.getch()

	curses.curs_set(1)

def login():
	global logged_in_user, users
	logged_in_user = User(0,"Max",18,"Toronto",["maxwell.huang-hobbs.com"],["FUCKING NOTHING"],[])
	users[0] = logged_in_user
	users[1] = User(0,"Will",19,"Boston",["williamsaulnier.com"],[],[])


def fake_load():
	global posts, users, comments
	posts[0] = Post(0,0,"Just ate a sandwich, LOL0 testing the line wrapping also so this text should be enough to cause wrap, but I don't have an elegant fallback for wrapping", "feeling full", [0])
	posts[1] = Post(1,1,"Just ate a sandwich, LOL1", "feeling full", [1,2,3])

	comments[0] = Comment(0, 1, "dumb0")
	comments[1] = Comment(1, 1, "dumb1")
	comments[2] = Comment(2, 1, "dumb2")
	comments[3] = Comment(3, 1, "dumb3")

def printblock(x, y, width, header, body):
	by = y+len(textwrap.wrap(body, width))+3;

	if( y>=0 and by< window.getmaxyx()[0]):
		curses.textpad.rectangle(window, y, x, by, x + width)
		window.addstr(y+1, x+2, header)

		#prints the body of the text post
		disp_width = width - 5
		wtext = textwrap.wrap(body, disp_width)
		for line in range(len(wtext)):
			window.addstr(y+2+line, x+5, wtext[line])
	return by

def redraw(scrolly):
	#redraw scroll
	post_x  = 3
	post_width = window.getmaxyx()[1]- 1 -post_x
	count_y=0
	for i in range(len(posts)):
		post = posts[i]

		count_y = printblock(
			post_x, count_y,post_width,
			post.get_username(),
			post.text_content) +1
		for c in range(len(post.comment_ids)):
			count_y = printblock(
					post_x+5, count_y, post_width-5,
					comments[post.comment_ids[c]].get_username(),
					comments[post.comment_ids[c]].text_content) +1

	window.refresh()

def main_interface():
	window.clear()
	window.refresh()
	scrolly = 0
	redraw(scrolly)
	while True:
		s = window.getch()
		print(s)
		if (s == curses.KEY_H):
			scrolly += 1
			redraw(scrolly)
		if (s == curses.KEY_UP):
			scrolly -= 1
			redraw(scrolly)
		if (s == curses.KEY_EXIT):
			break





if __name__ == "__main__":
	window = curses.initscr()

	startup()
	fake_load()
	login()
	main_interface()

	curses.endwin()