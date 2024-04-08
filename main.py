import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Sale, Stock, Shop

DSN = 'postgresql://postgres:postgres@localhost:5432/base_book'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher_name_or_id = input("Введите имя или идентификатор издателя: ")

try:
    publisher_id = int(publisher_name_or_id)
except ValueError:
    publisher_id = None

publisher = session.query(Publisher).filter(
    (
        Publisher.name == publisher_name_or_id and
        publisher_id is None
    ) | (
        Publisher.id == publisher_id
    )
).first()

if not publisher:
    print("Издатель не найден.")
else:
    sales = session.query(Sale).join(Stock).join(Book).filter(Book.id_publisher == publisher.id)

    for sale in sales:
        print(f"{sale.stock.book.title} | {sale.stock.shop.name} | {sale.price} | {sale.date_sale}")

session.close()
