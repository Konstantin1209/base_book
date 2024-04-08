from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import json
from models import Publisher, Book, Shop, Stock, Sale

Base = declarative_base()


engine = create_engine('postgresql://postgres:postgres@localhost:5432/base_book')
Base.metadata.create_all(engine)  
Session = sessionmaker(bind=engine)
session = Session()


with open('fixtures.json', 'r') as fd:
    data = json.load(fd)


for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    instance = model(id=record.get('pk'), **record.get('fields'))
    session.add(instance)

session.commit()
