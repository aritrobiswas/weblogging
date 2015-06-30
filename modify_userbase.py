import cPickle
import os

"""
A dummy method to initialize the userbase. Do NOT use unless you want to remove the existing userbase.
"""
def init_userbase():
	f = open("user_base.txt",'wb')
	cPickle.dump(["aritro","pele","maradona"], f)
	f.close()

"""
returns the line to insert into a new user's catalog html page after s/he has just been added.
The line helps identify which user's catalog page this is.
"""
def catalog_line_to_insert(user):
	return '<form action=\\\"{{ url_for(\'catalog\',username=\''+user+'\') }}\\\" method=\'post\'>'

"""
Adds the specified user to the userbase and sets up the appropriate directories and files (including their catalog page)
so that the user can begin logging.
"""
def add_user(user):
	userbase_file = open("user_base.txt",'rb')
	USER_BASE = cPickle.load(userbase_file)
	userbase_file.close()
	if user in USER_BASE:
		raise AssertionError("This user is already in the user base!")

	USER_BASE.append(user)
	userbase_file = open("user_base.txt",'wb')
	cPickle.dump(USER_BASE, userbase_file)
	userbase_file.close()
	os.system("sudo mkdir users/%s" %user)
	os.system("sudo mkdir users/%s/logs" %user)

	os.system("sudo mkdir templates/%s" %user)
	os.system("sudo mkdir templates/%s/logs" %user)
	os.system("sudo mkdir templates/%s/log_templates" %user)
	os.system("sudo touch templates/%s/catalog.html" %user)
	os.system('sudo cp templates/catalog_template_end.txt templates/%s' %user)
	os.system("sudo touch templates/%s/catalog_content.txt" %user)

	catalog_template_start = "templates/%s/catalog_template_start.txt" %user
	os.system('sudo cp templates/catalog_template_start.txt templates/%s' %user)

	os.system("echo \""+ catalog_line_to_insert(user) +"\" | sudo tee -a " + catalog_template_start + " > /dev/null")
	os.system("sudo cat templates/catalog_form_content.txt   >> "+catalog_template_start)

"""
Removes the specified user from the userbase and deletes all their files/directories.
"""
def remove_user(user):
	userbase_file = open("user_base.txt",'rb')
	USER_BASE = cPickle.load(userbase_file)
	userbase_file.close()
	if not (user in USER_BASE):
		raise AssertionError("This user is not in the user base!")

	USER_BASE.remove(user)
	userbase_file = open("user_base.txt",'wb')
	cPickle.dump(USER_BASE, userbase_file)
	userbase_file.close()
	os.system("sudo rm -rf templates/%s" %user)
	os.system("sudo rm -rf users/%s" %user)

"""
Returns the list of all users currently in the userbase.
"""
def display_all_users():
	userbase_file = open("user_base.txt",'rb')
	USER_BASE = cPickle.load(userbase_file)
	userbase_file.close()
	print USER_BASE

if __name__ == "__main__":
	pass