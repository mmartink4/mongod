import pymongo as mongo
import json
import mongo_utils as utils

ip = "192.168.78.135"

print("Connecting to MongoDB...")

def connectMongoDB(localhost):
	try:
		client = mongo.MongoClient("mongodb://"+localhost+":27017/")
		print("Connected to MongoDB!")
		return client
	except mongo.errors.ConnectionFailure as e:
		print(f"Could not connect to MongoDB: {e}")
		return None

def importJSON(data, dest):
	with open(data, "r") as file:
		print("Importing JSON...")
		i = 1
		errors = 0
		for line in file:
			try:
				data = json.loads(line)
				dest.insert_one(data)
				print(f"line {i} imported!")
				i += 1
			except json.JSONDecodeError as e:
				print(f"Error cargando JSON: {e}")
				errors += 1
		print(f"JSON imported! (errors while importing: {errors})")

conexion = connectMongoDB(ip)

if conexion is None:
	print("Error de conexion")
else:
	#db = conexion["tweets"] #collection = db["tweets"] #importJSON("tweets.json", collection) # importar archivo JSON a la DB
	tweets = conexion.get_database("tweets").get_collection("tweets")

	trending_accounts = utils.popularAccounts(tweets)[:10]
	trending_topics = utils.popularHashtags(tweets)[:10]

	

conexion.close()
