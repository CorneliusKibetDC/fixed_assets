# import psycopg2
# from psycopg2 import OperationalError

# # Database connection details
# db_uri = 'postgresql+psycopg2://p-admin:inventory2030@172.236.2.18:5432/db'


# # Extracting connection details from the URI
# import urllib.parse as up

# # Parsing the database URI
# result = up.urlparse(db_uri)
# user = result.username
# password = result.password
# host = result.hostname
# port = result.port
# database = result.path[1:]

# # Try to establish a connection to the database
# try:
#     connection = psycopg2.connect(
#         user=user,
#         password=password,
#         host=host,
#         port=port,
#         database=database,
#           # Use SSL mode as mentioned in the URI
#     )
    
#     # If successful, print connection details
#     print(f"Successfully connected to the database {database} at {host}")

#     # Close the connection
#     connection.close()

# except OperationalError as e:
#     print(f"Error: Unable to connect to the database. {e}")
