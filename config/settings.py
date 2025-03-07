class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/V21'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'another_super_secret_key'
    JWT_TOKEN_LOCATION = "cookies"
    
    JWT_ACCESS_COOKIE_NAME = "access_token"
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_COOKIE_SECURE = False  
    JWT_COOKIE_CSRF_PROTECT = False