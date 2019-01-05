import mysql.connector

import attributes.productEbay as ProductEbay
host = 'localhost'
user = 'root'
password = '@q18I0V6zDyaxFLJ'
db = 'CHIENSI3'
connection = mysql.connector.connect(host=host, database=db, user=user, password=password)
cursor = connection.cursor(buffered=True)
def insertProduct(id, title, image_link, type_product, source_store, sold_ebay, created_date, view_ebay):
	cursor.execute("""INSERT INTO `product`(`product`.`id`, `product`.`title`, `product`.`image_link`, `product`.`type_product`, `product`.`source_store`,`product`.`sold_ebay`, `product`.`created_date`, `product`.`view_ebay`)
	                                      SELECT * FROM (
	                                          SELECT '""" + str(id) + """' as cl1, " """ +
				   str(title) + """ " as cl2, '""" + str(image_link) + """' as cl3, '""" +
				   str(type_product) + """' as cl4, '""" + str(source_store) + """' as cl5, '""" +
				   str(sold_ebay) + """' as cl6, '""" + str(created_date) + """' as cl7, '""" + str(view_ebay) + """' as cl8) AS tmp
	                                      WHERE NOT EXISTS (
	                                          SELECT id FROM product WHERE id = '""" + str(id) + """') LIMIT 1;""")

	connection.commit()

	# print('Done insertProduct')

def getProductById():
	print('getProductById')

	
def getProductBySourceStore():
	print('DO getProductBySourceStore')

def getProductByType():
	print('DO getProductByType')	

def updateProduct():
	print('DO updateProduct')

def deleteProduct():
	print('DO deleteProduct')
