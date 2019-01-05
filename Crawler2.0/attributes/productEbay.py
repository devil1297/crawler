class productEbay:
    def __init__(self, id, title, image_link, type_product, source_store, sold_ebay, created_date, view_ebay):
        self.id = id
        self.title = title
        self.image_link = image_link
        self.type_product = type_product
        self.source_store = source_store
        self.sold_ebay = sold_ebay
        self.created_date = created_date
        self.view_ebay = view_ebay
    def setId(self, id):
        self.id = id

    def setTitle(self, title):
        self.title = title

    def setImage_link(self, image_link):
        self.image_link = image_link

    def setType_product(self, type_product):
        self.type_product = type_product

    def setSource_store(self, source_store):
        self.source_store = source_store

    def setCreated_date(self, created_date):
        self.created_date = created_date

    def setSold_ebay(self, sold_ebay):
        self.sold_ebay = sold_ebay

    def setView_ebay(self, view_ebay):
        self.view_ebay = view_ebay

    def __str__(self):
        return '['+str(self.id)+','+str(self.title)+','+str(self.image_link)+','+str(self.type_product)+','+str(self.sold_ebay)+','+str(self.created_date)+','+str(self.view_ebay)+']'