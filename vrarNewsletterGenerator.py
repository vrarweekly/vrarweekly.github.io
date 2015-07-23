#!/usr/local/bin/python

from os.path import isfile, join
import csv
import string
import json
import codecs

# config
## issue specific
reddit_url = "https://www.reddit.com/r/oculus/comments/3ebwm0/what_happened_this_week_in_vr_vrar_weekly_issue_7/"
## name
newsletter_name = "VR/AR Weekly"
url = "http://www.vrarweekly.com" # include http://
## colors
primary_color =  "#455A64" # header, labels
secondary_color = "#303F9F" # links
support_color = "#607D8B"# domains 
## categories
categories = [
["Oculus", ["Oculus", "Palmer", "Rift", "DK2", "Carmack"]],
["Valve", ["Valve", "Steam", "Vive", "HTC", "Lighthouse"]],
["Sony", ["Sony", "Morpheus"]],
["Samsung", ["Gear", "GearVR", "Samsung"]],
["StarVR", ["StarVR"]],
["Google", ["Google", "YouTube", "Cardboard", "Android", "Android"]],
["Microsoft", ["Microsoft", "Xbox", "Minecraft", "Hololens", "HoloLens"]]
] # Leave empty if you don't want categories. If you have categories, add them to the list in the following format: [name of category, [flair tag 1, flair tag 2, flair tag3, ...]]. It will search each flair tag and if there's a match, assign it to the category.
category_search_method = "title" # choose title or flair depending

def newIssue(issue,date):
	newsletter(issue,date)
	# update the html of the landing page

def newsletter(issue, date):
	
	html_content, markdown_content = generatePosts('json/'+date+'.json')
	email_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Top posts in virtual and augmented reality | {{newsletter_name}} #{{issue}}</title>
    <meta name="description" content="Top posts from every major virtual reality subreddits for the week of {{date}}. Keep up to date with virtual reality and augmented reality by subscribing to VR/AR Weekly.">
</head>
<body>
<!-- INCLOSING TABLE AND DIV -->
<div class="issue-html"><table border="0" width="100%" cellpadding="0" cellspacing="0" bgcolor="#ffffff" style="font-family: 'helvetica neue', helvetica, arial, sans-serif; font-size: 14px; line-height: 20px; color: #333"><tr><td align="center" valign="top">

<!-- EMAIL TEXT AND AND READ ON WEB LINK -->
	<table border="0" width="660" cellpadding="0" cellspacing="0" class="container noarchive" style="border-collapse: collapse;"><tr><td style="padding-top: 6px; padding-bottom: 6px; font-size: 12px; text-align: center; color: #555">
		<a target="_blank" href="{{url}}/{{issue}}.html" style="color: {{secondary_color}}">Read this e-mail on the Web</a>
	</td></tr></table>

	<!-- BODY INCLOSING TABLE -->
	<table border="0" width="660" cellpadding="0" cellspacing="0" class="container" style="border-collapse: collapse">
		<tr><td style="background-color: {{primary_color}}"><table width="100%" cellspacing="0" cellpadding="0" align="left"><tr><td align="left" class="block" style="padding: 6px 12px;">

		<!-- TOP BANNER -->
			<table align="left" width="50%" class="gowide"><tr><td><span style="line-height: 36px; font-size: 23px; color: {{secondary_color}}; font-weight: bold; color: #ffffff; -webkit-font-smoothing: antialiased;">{{newsletter_name}}</span></td></tr></table>
			<table align="left" style="text-align: right" width="50%" class="gowide lonmo"><tr><td><span style="font-size: 14px; line-height: 36px; font-weight: normal; color: #ffffff">
				Issue #{{issue}} // {{date}}
			</span></td></tr></table>
		</td></tr></table></td></tr>

		<!-- DISCUSS ON REDDIT -->
		<tr><td bgcolor="#f4f4f4" style="font-family: verdana, helvetica, arial, sans-serif; text-align: left; padding-top: 12px; padding-left: 12px; padding-right: 12px; padding-bottom: 12px;" class="noarchive">
			<p style="line-height: 15px; font-size: 14px; margin-top: 12px">Discuss this week's top posts <a target="_blank" href="{{reddit_url}}" style="color: #0088cc">on reddit</a>.
		</td></tr>

		<!-- POSTS CONTAINER -->
		<tr><td style="padding: 16px 12px 12px 12px" align="left">

		{{html_content}}

		</td></tr>

		<!-- FOOTER -->
<tr><td bgcolor="#f4f4f4" style="font-family: verdana, helvetica, arial, sans-serif; text-align: left; padding-top: 12px; padding-left: 12px; padding-right: 12px; padding-bottom: 12px" class="noarchive">
	<p style="line-height: 15px; font-size: 14px; margin-top: 12px">A side project of <a target="_blank" href="http://twitter.com/tonysheng" style="color: #0088cc">@tonysheng</a>.
	<p style="font-size: 14px; line-height: 15px">Forwarded this email? Subscribe to the newsletter <a target="_blank" href="http://www.vrarweekly.com" style="color: #0088cc">here</a>.</p>
</td></tr>
</table>
</td></tr></table></div>
</body>
</html>
"""
	email_html = email_html.replace("{{issue}}", issue)
	email_html = email_html.replace("{{date}}", date)
	email_html = email_html.replace("{{html_content}}", html_content)
	email_html = email_html.replace("{{newsletter_name}}", newsletter_name)
	email_html = email_html.replace("{{primary_color}}", primary_color)
	email_html = email_html.replace("{{secondary_color}}", secondary_color)
	email_html = email_html.replace("{{support_color}}", support_color)
	email_html = email_html.replace("{{url}}", url)
	email_html = email_html.replace("{{reddit_url}}", reddit_url)

	#markdown 
	markdown_text = """
#{{newsletter_name}}
Issue #{{issue}} // {{date}} // [Subscribe to get every issue in your inbox](http://www.vrarweekly.com)

VR/AR Weekly is a collection of the top posts from nine virtual reality subreddits.

{{markdown_content}}

&nbsp;

*Send me some feedback by responding to the thread. If you want to subscribe by email, [click here](http://www.vrarweekly.com)*

*Past issues at the bottom of [this page](http://www.vrarweekly.com)*
"""
	markdown_text = markdown_text.replace("{{issue}}", issue)
	markdown_text = markdown_text.replace("{{date}}", date)
	markdown_text = markdown_text.replace("{{markdown_content}}", markdown_content)
	markdown_text = markdown_text.replace("{{newsletter_name}}", newsletter_name)

	Html_file = open(issue+".html","w")
	print "created newsletter '"+issue+"'"
	Html_file.write(email_html.encode('utf-8'))
	Html_file.close()

	Html_file = open("md/"+issue+".md","w")
	print "created markdown '"+issue+"'"
	Html_file.write(markdown_text.encode('utf-8'))
	Html_file.close()

def generatePosts(file):
	posts_html = """
	"""
	posts_markdown = """
	"""

	json_data = open(file)
	file_data = json.load(json_data)
	post_list = [];

	for post in file_data['data']['children']:
		post_data = {}
		post_title = post['data']['title'].encode('utf-8')
		post_url = post['data']['url'].encode('utf-8')
		post_description = post['data']['selftext'].encode('utf-8')
		if len(post_description) > 300:
			post_description = post_description[0:300] + "[...]"
		post_domain = post['data']['domain'].encode('utf-8')
		post_permalink = "https://www.reddit.com" + post['data']['permalink'].encode('utf-8')
		post_flair = str(post['data']['link_flair_text'])
		post_comments = str(post['data']['num_comments'])
		post_html = """
		<table width="600" align="left" class="gowide" cellpadding="0" cellspacing="0" style="border-collapse: collapse"><tr><td>
				<div style="font-size: 18px; margin: 2px 0px"><a target="_blank" href="{{post_url}}?utm_source=vrarweekly&amp;utm_medium=email" title="{{post_url}}" style="display: block; color: #0088cc; line-height: 24px; text-decoration: underline; font-weight: 500">{{post_title}}</a></div>
				<div style="color: {{support_color}}; font-weight: normal; font-size: 12px; line-height: 24px; text-transform: lowercase; margin-top: 2px; font-family: verdana, arial, sans-serif">
					{{post_domain}}   <a target="_blank" href="{{post_permalink}}?utm_source=vrarweekly&amp;utm_medium=email" title="{{post_permalink}}" style="display: inline-block; color: #0088cc; text-decoration: none; text-transform: none">  comments ({{post_comments}}) >></a></div>
					<div style="font-size: 13px; line-height: 17px; margin-top: 4px; color: #666666">
						{{post_description}}
					</div>
					<br>
				</td></tr></table>
				<table width="140" class="nomo" align="left"><tr><td style="text-align: center"></td></tr></table>
				<br clear="all" style="clear: both">
		"""
		post_markdown = """
**[{{post_title}}]({{post_url}})**
{{post_domain}} | [comments ({{post_comments}})]({{post_permalink}})

{{post_description}}

&nbsp;

"""

		post_html = post_html.replace("{{post_url}}", post_url.decode("utf-8"))
		post_html = post_html.replace("{{post_title}}", post_title.decode("utf-8"))
		post_html = post_html.replace("{{post_domain}}", post_domain.decode("utf-8"))
		post_html = post_html.replace("{{post_flair}}", post_flair)
		post_html = post_html.replace("{{post_comments}}", post_comments)
		post_html = post_html.replace("{{post_description}}", post_description.decode("utf-8"))
		post_html = post_html.replace("{{post_permalink}}", post_permalink.decode("utf-8"))

		post_markdown = post_markdown.replace("{{post_url}}", post_url.decode("utf-8"))
		post_markdown = post_markdown.replace("{{post_title}}", post_title.decode("utf-8"))
		post_markdown = post_markdown.replace("{{post_domain}}", post_domain.decode("utf-8"))
		post_markdown = post_markdown.replace("{{post_flair}}", post_flair)
		post_markdown = post_markdown.replace("{{post_comments}}", post_comments)
		post_markdown = post_markdown.replace("{{post_description}}", post_description.decode("utf-8"))
		post_markdown = post_markdown.replace("{{post_permalink}}", post_permalink.decode("utf-8"))

		post_list.append([post_title, post_html, post_flair, post_markdown])
		
	# if there are no categories
	if len(categories) == 0:
		for posts in post_list:
			posts_html = posts_html + posts[1]
			posts_markdown = posts_markdown + posts[3]
	# if you need fuzzy search
	elif categories[0][1]:
		# add posts from each category
		for category in categories:
			category_post_list = []
			for post in post_list:
				for category_string in category[1]:
					if (post[0] in category_string or category_string in post[0]):
						category_post_list.append([post[0], post[1], post[2], post[3]])
						post[0] = category[0]
						# effectively removes post from list
			if len(category_post_list) != 0:
				posts_html = posts_html + '<p style="color:{{primary_color}}; font-size: 24px; font-weight: normal; margin-top: 8px; margin-bottom: 10px">{{category_title}}</p>'
				posts_html = posts_html.replace("{{category_title}}", category[0])

				posts_markdown = posts_markdown + """
##{{category_title}}
"""
				posts_markdown = posts_markdown.replace("{{category_title}}", category[0])
				for post in category_post_list:
					posts_html = posts_html + post[1]
					posts_markdown = posts_markdown + post[3]
		# add uncategorized posts
		for post in post_list:
			category_post_list = []
			for category in categories:
				if post[0] == category[0]:
					post_list.remove(post)
		for post in post_list:
			for category in categories:
				if post[0] == category[0]:
					post_list.remove(post)
		for post in post_list:
			for category in categories:
				if post[0] == category[0]:
					post_list.remove(post)
		for post in post_list:
			for category in categories:
				if post[0] == category[0]:
					post_list.remove(post)
		# don't know why but need to loop it to remove all dups
		category_post_list = [];
		for post in post_list:
			category_post_list.append(post)
		if len(category_post_list) > 0:
			posts_html = posts_html + '<p style="color:{{primary_color}}; font-size: 24px; font-weight: normal; margin-top: 8px; margin-bottom: 10px">Other</p>'
			posts_markdown = posts_markdown + """
##Other
"""
		for post in category_post_list:
			posts_html = posts_html + post[1]
			posts_markdown = posts_markdown + post[3]
	# else search for category using flair



	return (posts_html, posts_markdown)

newIssue('7', 'July 23, 2015')




