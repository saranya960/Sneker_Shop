sql = '''
  create table sneakers(
    id integer primary key,
    brand text not null,
    name text not null,
    year integer not null,
    price integer not null
  );
'''

from db_connect import db, cursor
cursor.execute(sql)
db.commit()
