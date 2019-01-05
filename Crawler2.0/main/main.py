import dbconnection.dbProductEbay as dbEbay
import lib.FunctionHelper as FunctionHelper
import attributes.productEbay as ProductEbay
title = 'Ernie Sesame Gay LGBT Pride Over It Jumper Puppet Masc Bottom Top'
[status, type]=FunctionHelper.get_type_product(title)
a = ProductEbay.productEbay('a','b','a','b','a','b','a')
dbEbay.insertProduct(a)
print(a)