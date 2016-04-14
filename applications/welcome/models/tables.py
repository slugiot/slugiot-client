#########################################################################
## Define your tables below, for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

db.define_table('procedures',
                Field('procedure_id', 'bigint', required=True), #key
                Field('device_id', required=True), # not sure what field type this should be
                Field('last_sync', 'datetime', default=datetime.datetime.utcnow(), required=True),
                Field('name', 'string'),  # Name of procedure
                Field('data', 'text', required=True),  # Actual code for procedure - is check IS_LENGTH(65536) ok?
                                        # Otherwise use string and specifiy larger length
                Field('valid', 'boolean', required=True) # If scheduler should/should not access entry for this procedure
                )