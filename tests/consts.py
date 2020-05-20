from furl import furl

LOCALHOST = API_HOST = DB_HOST = GUI_HOST = MQ_HOST = SERVER_HOST = '127.0.0.1'

API_PORT = 5000
DB_PORT = 27017
GUI_PORT = 8080
MQ_PORT = 5672
SERVER_PORT = 8000

API_URL = f'http://{API_HOST}:{API_PORT}'
DB_URL = f'mongodb://{DB_HOST}:{DB_PORT}'
GUI_URL = f'http://{GUI_HOST}:{GUI_PORT}'
MQ_URL = f'rabbitmq://{MQ_HOST}:{MQ_PORT}'

API_FURL = furl(API_URL)
DB_FURL = furl(DB_URL)
GUI_FURL = furl(GUI_URL)
MQ_FURL = furl(MQ_URL)

DB_NAME = 'brain'
COLLECTION_NAME = 'users_and_snapshots'

PARSERS = ['pose', 'color_image', 'depth_image', 'feelings']
