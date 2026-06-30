# from dotenv import load_dotenv
# import os

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# dotenv_path = os.path.join(base_dir, '.env')
# load_dotenv(dotenv_path=dotenv_path)

# class Settings:
#     DB_HOST = os.getenv("DB_HOST")
#     DB_PORT = int(os.getenv("DB_PORT", 5432))
#     DB_NAME = os.getenv("DB_NAME")
#     DB_USER = os.getenv("DB_USER")
#     DB_PASSWORD = os.getenv("DB_PASSWORD")

#     DB_MIN_CONN = int(os.getenv("DB_MIN_CONN", 1))
#     DB_MAX_CONN = int(os.getenv("DB_MAX_CONN", 10))

# settings = Settings()



TABLE_USERS = 'users'
TABLE_TRIPS = 'trips'
TABLE_TRIP_MEMBERS = 'trip_members'