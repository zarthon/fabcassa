import pycassa
pool = pycassa.connect('User',['cass01:9160'])
col_fam = pycassa.ColumnFamily(pool,'temp')
col_fam.insert('row_key',{'col_name':'col_val1'})
a = col_fam.get('row_key')
print a
