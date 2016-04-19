import datetime


############### Procedure Harness Table ###############

db.define_table('procedure',
                Field('proc_id', 'bigint', required=True),  # key
                Field('user_id', 'string', required=True),
                Field('last_update', 'datetime', required=True),
                Field('proc_name', 'string'),  # Name of procedure
                Field('proc_data', 'text', required=True),  # Actual code for procedure - is check IS_LENGTH(65536) ok?
                # Otherwise use string and specifiy larger length
                )
