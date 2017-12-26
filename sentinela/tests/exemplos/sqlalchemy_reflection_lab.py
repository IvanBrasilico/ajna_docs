from sqlalchemy import inspect

from sentinela.models.carga import Base, Escala, MySession

mapper = inspect(Escala)

print(mapper)

print(mapper.attrs)

print('Columns')
for column in mapper.column_attrs:
    print(column)

print('Relationships')
for column in mapper.relationships:
    print(column)

dbsession = MySession(Base).session
q = dbsession.query(Escala)
row = q.first()
print(row)
print(row.to_dict)
print(row.to_list)
mapper = inspect(type(row))
print(mapper)
print('Columns row')
for column in mapper.column_attrs:
    print(column)
