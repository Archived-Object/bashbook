class User():
	def __init__(self, uid, name, age, location, websites, interests, friends):
		(	self.uid, self.name, self.age, self.location,
			self.websites, self.interests, self.friends) = (
				uid, name, age, location, websites, interests, friends
			)

class Post():
	def __init__(self, post_id, creator_uid, text_content, meta_content, comment_ids):
		(	self.post_id, self.creator_uid, self.text_content,
			self.meta_content, self.comment_ids) = (
				post_id, creator_uid, text_content,
				meta_content, comment_ids)

class Comment():
	def __init__(self, comment_id, creator_uid, text_content):
		(self.comment_id, self.creator_uid, self.text_content) = (
			comment_id, creator_uid, text_content)