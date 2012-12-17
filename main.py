#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import users
from google.appengine.ext import db
import datetime

class MainHandler(webapp2.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if not user:
			html = '<html><body>'
			html = html + '<center><h1>Voting Website</h1></center>'
			html = html + ('<a href=\"%s\">Sign in or register</a>.'% (users.create_login_url("/")))
			html = html + '</body></html>'
		else:
			userString = ('<p>Welcome, %s! You can <a href="%s">sign out</a></p>'% (user.nickname(), users.create_logout_url("/")))
			html = '<html><body>'
			html = html + '<center><h1>Voting Website</h1></center>'
			html = html + userString
			html = html + '<form action="/mainhandlerdecide" method="post">'
			html = html + 'Enter your First Name: <input type="text" name="firstName"><br>'
			html = html + 'Enter your Last Name: <input type="text" name="lastName"><br>'
			html = html + '<input type="submit" name="button" value="Submit">'
			html = html + '<input type="submit" name="button" value="List">'
			html = html + '</body></html>'
		self.response.out.write(html)
	
class MainHandlerDecision(webapp2.RequestHandler):
    def post(self):
		if self.request.get('button') == "Submit" :
			firstName = self.request.get('firstName')
			lastName = self.request.get('lastName')
			employee = Employee(first_name=firstName,last_name=lastName)
			employee.hire_date = datetime.datetime.now().date()
			employee.put()
			html = '<html><body>'
			html = html + 'You entered ' + firstName + ' ' + lastName + '<br>'
			html = html + self.addcomment()
			html = html + '<form action="/" method="get">'
			html = html + '<input type="submit" value="Back">'
			html = html + '</body></html>'
			self.response.out.write(html)
			#self.redirect("/submitclass")
		if self.request.get('button') == "List" :
			self.redirect("/listclass")
	
    def addcomment(self):
		firstName = self.request.get('firstName')
		lastName = self.request.get('lastName')
		temp = 'This is addcomment function<br>'
		html = 'You had entered ' + firstName + ' ' + lastName + '<br>'
		temp = temp + html
		return temp
		
class SubmitClass(webapp2.RequestHandler):
	def get(self):	
		self.response.out.write('This is get of SubmitClass')
	def post(self):
		self.response.out.write('This is post of SubmitClass')

class ListClass(webapp2.RequestHandler):
	def get(self):
		emps = db.GqlQuery("SELECT * FROM Employee")
		html = '<html><body>Listing all Employees<br>'
		for emp in emps:
			firstName = emp.first_name
			lastName = emp.last_name
			html = html + firstName + ' ' + lastName + '<br>'
		html = html + '<form action="/" method="get">'
		html = html + '<input type="submit" value="Back">'
		html = html + '</body></html>'
		self.response.out.write(html)
		
	def post(self):
		self.response.out.write('This is post of ListClass')
		
class Employee(db.Model):
	first_name = db.StringProperty()
	last_name = db.StringProperty()
	hire_date = db.DateProperty()
		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/mainhandlerdecide', MainHandlerDecision),
	('/submitclass', SubmitClass),
	('/listclass', ListClass)
], debug=True)
