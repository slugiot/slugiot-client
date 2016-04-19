import datetime


############### Procedure Harness Table ###############

db.define_table('procedures',
                Field('procedure_id', 'bigint', required=True),  # key
                Field('user_id', 'string', required=True),
                Field('last_sync', 'datetime', default=datetime.datetime.utcnow(), required=True),
                Field('name', 'string'),  # Name of procedure
                Field('procedure_data', 'text', required=True),  # Actual code for procedure - is check IS_LENGTH(65536) ok?
                # Otherwise use string and specifiy larger length
                Field('valid', 'boolean', required=True)
                # If scheduler should/should not access entry for this procedure
                )
