class DevelopmentConfig(object):
    SECRET_KEY = 'secret12345'
    DEBUG = True
    # Config MySQL
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'flask_demo'
    MYSQL_CURSORCLASS = 'DictCursor' 
    
