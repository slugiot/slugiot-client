import datetime

db.define_table('logs',
                Field('timestamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('module'),
                Field('level', 'integer'), #  int, 0 = most important.
                Field('message', 'text'),
                )

db.define_table('output',
                Field('timestamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('module'),
                Field('name'), # Name of variable
                Field('value', 'text'), # Json, short please
                )

db.define_table('values',
                Field('timestamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('module'),
                Field('name'),  # Name of variable
                Field('value', 'text'),  # Json, short please
                )

############### Procedure Harness Table ###############

db.define_table('procedures',
                Field('procedure_id', 'bigint', required=True),  # key
                Field('user_email', 'string', required=True),
                Field('last_sync', 'datetime', default=datetime.datetime.utcnow(), required=True),
                Field('name', 'string'),  # Name of procedure
                Field('data', 'text', required=True),  # Actual code for procedure - is check IS_LENGTH(65536) ok?
                # Otherwise use string and specifiy larger length
                Field('valid', 'boolean', required=True)
                # If scheduler should/should not access entry for this procedure
                )
