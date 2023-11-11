from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB_DEV', 'user')
mongodb_pass = config.get('DB_DEV', 'PASSWORD')
db_name = config.get('DB_DEV', 'db_name')
domain = config.get('DB_DEV', 'domain')


# connect to cluster on AtlasDB with connection string

connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)
