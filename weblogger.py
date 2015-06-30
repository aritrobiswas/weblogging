import weblog
import os
import logging
import config
import tempfile
import requests

HOST = config.HOST
HOST_URL = config.HOST_URL
PASSWORD = config.password

"""
Use this class to send log reports to a log.
Example usage:
online_logger = weblogger("example_log","example_user")
online_logger.critical("critical message - should be printed")
online_logger.debug("debug message")
"""
class weblogger:
	log = None
	log_link = None
	user = None
	format = None
	level = None
	datefmt = None
	"""
	log = the name of the log you want to log to
	user = the user who the log belongs to
	level = logging level 
	format = logging format
	date_fmt = date format
	"""
	def __init__(self,log,user,
		level=logging.INFO,
		format='%(asctime)s %(levelname)s: %(message)s',
		datefmt='%m/%d/%Y %I:%M:%S %p'
		):
			self.level = level
			self.format = format
			self.log = log
			self.log_link = HOST_URL + "logs/" + log
			self.user = user
			self.datefmt =  datefmt


	"""
	This is called each time a logging statement is issued.
	We set up a logger for each statement we want to log.
	log_file is the path of a currently existing file whose contents we will ultimately post to the http
	link of the log file we wish to update.
	"""
	def setup_logger(self,logger_name, log_file,level=logging.INFO):
	    """
	    logger_name = name of the logger
	    log_file = the path of a currently existing file whose contents we will ultimately post to the
	    site of the log file we wish to update. In the current implementation, this file is a temp file we will
	    ultimately delete after posting its contents to the logging site.
	    level = logging level
	    """
	    l = logging.getLogger(logger_name)
	    formatter = logging.Formatter(self.format,self.datefmt)
	    fileHandler = logging.FileHandler(log_file, mode='w')
	    fileHandler.setFormatter(formatter)

	    l.setLevel(self.level)
	    l.addHandler(fileHandler)

	"""
	Sets the logging level.
	"""
	def setLevel(self,lvl):
	 	self.level = lvl

	"""
	Checks if the logger is enabled for the specified level, i.e. whether
	a logging call of that level will go through given the logger's current level.
	"""
	def isEnabledFor(self,lvl):
		return self.level >= lvl

	"""
	Returns the current logging level
	"""
	def getEffectiveLevel(self):
	 	return self.level
		
	def debug(self,message):
		filename,logger = self.generate_file_and_logger()
		self.log_statement(filename,logger,message,logger.debug)

	def warning(self,message):
		filename,logger = self.generate_file_and_logger()
		self.log_statement(filename,logger,message,logger.warning)

	def info(self,message):
		filename,logger = self.generate_file_and_logger()
		self.log_statement(filename,logger,message,logger.info)

	def error(self,message):
		filename,logger = self.generate_file_and_logger()
		self.log_statement(filename,logger,message,logger.error)

	def critical(self,message):
		filename,logger = self.generate_file_and_logger()
		self.log_statement(filename,logger,message,logger.critical)

	"""
	This is called once per each logging command. A file is created that will be logged to
	according to whether the specified logging level goes through and a corresponding logger
	to log to this file will be created.

	Implementation:
	First use the NamedTemporaryFile function to generate a file whose name hasn't yet been 
	taken yet. Retain the name and remove the file. After the file has been removed, actually
	create the file with that specified name and path. Generate the appropriate logger and return both
	the file path and logger.
	The reason that the temp file created by the python method is deleted at first is because logging
	statements weren't working on the file created via the python method. Hence it was necessary to 
	delete it and remake it from terminal.
	"""
	def generate_file_and_logger(self):
		f = tempfile.NamedTemporaryFile(mode='w+b', prefix='tmp', dir=None, delete=True)
		filename = f.name
		f.close()
		os.system('sudo touch %s' %filename)
		self.setup_logger(filename,filename)
		logger = logging.getLogger(filename)
		return filename,logger

	"""
	Logs the specified message at the appropriate logging level to the filename, and then posts the
	contents to the logging site.
	"""
	def log_statement(self,filename,logger,message,fn):
		fn(message)
		f = open(filename,'r')
		text = f.read()
		f.close()
		os.system("sudo rm %s" %filename) # remove the file
		if len(text) != 0:
			self.post(text) # post this message to the logging site.

	"""
	posts the specified message to the log site.
	"""
	def post(self,html_log_entry):
		"""
		html_log_entry = the message to post to the appropriate logging site
		"""
		login_url = config.HOST_URL
		login_values = {'username': self.user, 'password': PASSWORD}
		login_request = requests.post(login_url, data=login_values)
		log_post = {'data': html_log_entry}
		log_url = "%s%s/log/%s" %(HOST_URL,self.user,self.log)
		log_request = requests.post(log_url,data=log_post)


if __name__ == "__main__":
	online_logger = weblogger("log","aritro")
	online_logger.critical("critical message - should be printed")
	online_logger.debug("debug message")