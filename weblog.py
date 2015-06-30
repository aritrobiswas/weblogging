import os
import cPickle
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import config
import time

app = Flask(__name__)
#username = ""
user_base = config.USER_BASE
HOST = config.HOST
# Load default config and override config from an environment variable
app.config.update(config.CONFIG_VARS)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

"""
Line to insert into the html file of a log that has just been created.
Ensures that the html file has the correct identifiers for its "username" and "log" fields
"""
def log_line_to_insert(username,log):
	"""
	log = name of the log that was created
	"""
	return '<form action=\\\"{{ url_for(\'log\',username=\'' + username + '\',log=\'' +log + '\') }}\\\" method=\'post\'>'



"""
Line to insert into the html file of a user's catalog after s/he has created a log.
Provides a link to the page of the newly created log on the user's catalog page.
"""
def catalog_line_to_insert(username,log):
	"""
	log = name of the log that was created
	"""
	return '<a href=\\\"{{ url_for(\'log\',username=\'' + username + '\',log=\'' +log + '\') }}\\\" target=\'_top\'>' + log + '</a><br>'


"""
page corresponding to the specified log of the specified user.
Supports posting data..
"""
@app.route('/<username>/log/<log>', methods=['GET','POST'])
def log(username=None,log=None):
	user_page = "templates/" + username + "/logs/" + log + ".html"
	user_log = "users/" + username + "/logs/" + log + ".txt"
	template_start  = "templates/"+username+"/log_templates/" + log + "/log_template_start.txt"
	template_end = "templates/"+username+"/log_templates/" + log + "/log_template_end.txt"
	if request.method == 'POST':
		os.system("sudo echo \"" + request.form['data'] + "<br>\" >> " + user_log)
	
	os.system("sudo cat "+template_start+" "+user_log+" "+template_end+" > "+user_page)
 	return render_template(username+'/logs/'+log+'.html')

"""
the catalog page of the specified user. Supports adding new logs and posting to existing logs.
""" 
@app.route('/<username>/catalog', methods=['GET','POST'])
def catalog(username=None):
	user_page = "templates/" + username + "/catalog.html"
	user_catalog = "templates/" + username + "/catalog_content.txt"
	catalog_template_start  = "templates/%s/catalog_template_start.txt" % username
	catalog_template_end = "templates/%s/catalog_template_end.txt" % username
	if request.method == 'POST':	
		if request.form['submit'] == 'search': # user wants to add to an existing log
			return redirect(url_for('log', username = username, log=request.form['log to search']))
		elif request.form['submit'] == 'create log': # user wants to create a new log
			log_to_create = request.form['log to create']
			log_address = "users/%s/logs/%s.txt" %(username,log_to_create)
			os.system('sudo touch %s' %log_address)
			template_dir = "templates/%s/log_templates/%s/" %(username,log_to_create)
			os.system('sudo mkdir %s' %template_dir)
			os.system('sudo cp templates/log_template_end.txt %s' %template_dir)
			os.system('sudo cp templates/log_template_start.txt %s' %template_dir)
			log_template_start = template_dir+"log_template_start.txt"
			os.system("echo \""+ log_line_to_insert(username,log_to_create) +"\" | sudo tee -a " + log_template_start + " > /dev/null")
			os.system("sudo cat templates/log_template_middle.txt   >> "+log_template_start)
			html_file_loc = "templates/%s/logs/%s.html" %(username,log_to_create)
			os.system('sudo touch %s' %html_file_loc)
			
			os.system("echo \""+ catalog_line_to_insert(username,log_to_create) +"\" | sudo tee -a " + user_catalog + " > /dev/null")

			return redirect(url_for('catalog',username = username))
		else:
			pass
		
	os.system("sudo cat "+catalog_template_start+" "+user_catalog+" "+catalog_template_end+" > "+user_page)
 	return render_template(username+'/catalog.html')


#the login page is the homepage.
@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if not request.form['username'] in user_base:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			username = request.form['username']
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('catalog',username = username))
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host=HOST) # this argument allows all computers 
                            # on the network to connect