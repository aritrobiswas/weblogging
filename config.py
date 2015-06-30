import cPickle
password = 'default'
CONFIG_VARS = dict(
    DEBUG=True,
    SECRET_KEY='development key',
    PASSWORD=password
)
userbase_file = open("user_base.txt",'rb')
USER_BASE = cPickle.load(userbase_file)
userbase_file.close()

HOST = '0.0.0.0' #using this value allows all computers on the network to connect
PORT = '5000'
HOST_URL = "http://" + HOST + ":" + PORT + "/" #could change later