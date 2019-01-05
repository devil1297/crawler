import mysql.connector
host = 'localhost'
user = 'root'
password = '@q18I0V6zDyaxFLJ'
db = 'CHIENSI3'
connection = mysql.connector.connect(host=host, database=db, user=user, password=password)
cursor = connection.cursor(buffered=True)
def insertStore(nameStore):
	cursor.execute("""INSERT INTO `stores_ebay_source` (`source_store`, `count_products`)
                                                       SELECT * FROM (
                                                       SELECT '""" + nameStore + """', 0) AS tmp
                                                       WHERE NOT EXISTS (
                                                            SELECT source_store FROM stores_ebay_source WHERE source_store = '""" + nameStore + """'
                                                       ) LIMIT 1;
                                           """)

	connection.commit()

def getAllStore():
	cursor.execute("""SELECT * FROM `stores_ebay_source`;""")
	return cursor.fetchall()

def getAllStoreNotEmpty():
	cursor.execute("""SELECT * FROM `stores_ebay_source` WHERE `count_products` != -1;""")
	return cursor.fetchall()

def getStore():
	cursor.execute("""SELECT * FROM `stores_ebay_source` ORDER BY RAND();""")
	return cursor.fetchone()

def getStoreByCountProduct():
	print()
	
def getStoreBySourceStore():
	print('Done getStoreBySourceStore')

def updateStore(name_shop,count_products):
	print(name_shop)
	# print(
	# 	"""UPDATE `stores_ebay_source` SET `count_products` = """ +str(count_products)+ """ WHERE `stores_ebay_source`.`source_store` = '""" + name_shop + """';""")
	cursor.execute("""UPDATE `stores_ebay_source` SET `count_products` = """ +str(count_products)+ """ WHERE `stores_ebay_source`.`source_store` = '""" + str(name_shop) + """';""")

	connection.commit()
	print('Done updateStore')

def updateEmptyStore(name_shop):
	print(name_shop)
	# print("""UPDATE `stores_ebay_source` SET `count_products` = -1 WHERE `stores_ebay_source`.`source_store` = '""" + name_shop + """';""")
	cursor.execute("""UPDATE `stores_ebay_source` SET `count_products` = -1 WHERE `stores_ebay_source`.`source_store` = '""" + str(name_shop) + """';""")

	connection.commit()
	print('Done updateEmptyStore')

def deleteStore():
	print('Done deleteStore')
