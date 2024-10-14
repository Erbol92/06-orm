import sqlalchemy as sq
from models import *
from views import *
from sqlalchemy.orm import sessionmaker
from random import randint
import json


DSN = "postgresql://postgres:postgres@localhost:5432/orm_db_hw"
engine = sq.create_engine(DSN)
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

# создание объектов
querys = []

# магазины
shops = ['Буквоед', 'Лабиринт', 'Книжный дом']
for shop in shops:
    obj = Shop(name=shop)
    querys.append(obj)

# авторы
publisher_names = ['Пушкин', 'Толстой', 'Гоголь']
for name in publisher_names:
    publisher = Publisher(name=name)
    querys.append(publisher)

# книги
books = ['Капитанская дочка', 'Руслан и Людмила',
         'Евгений Онегин', 'Русалочка']
# querys.clear()
for book in books:
    obj = Book(title=book, id_publisher=randint(1, len(publisher_names)))
    querys.append(obj)

# склады
for el in range(len(books)*len(shops)):
    stock = Stock(id_book=randint(1, len(books)), id_shop=randint(
        1, len(shops)), count=randint(1, 100))
    querys.append(stock)

# продажи
for _n in range(20):
    date = generate_random_date()
    obj = Sale(price=randint(500, 6000), date_sale=date, id_stock=randint(
        1, len(books)*len(shops)), count=randint(1, 100))
    querys.append(obj)
session.add_all(querys)
session.commit()

val = input('введите имя издателя ')
if val:
    subq = session.query(Book).join(Publisher).filter(
        Publisher.name == val).subquery()

    print('название книги | название магазина | стоимость покупки | дата покупки')
    for sale, stock in session.query(Sale, Stock).join(Stock, Sale.id_stock == Stock.id).join(subq, Stock.id_book == subq.c.id).all():
        print(f'{stock.book.title}|{stock.shop} |{
            sale.price}|{sale.date_sale.date()}')

val = input('переходим в 4му заданию? Y/N:').upper()
if val == 'Y':
    session.close()
    drop_tables(engine)
    create_tables(engine)
    with open(file='tests_data.json', mode='r') as f:
        data = json.load(f)
        tb_name = {'publisher': Publisher,
                   'book': Book,
                   'shop': Shop,
                   'stock': Stock,
                   'sale': Sale,
                   }
        for val in data:
            model = tb_name.get(val.get('model'))
            session.add(model(**val['fields']))
        session.commit()

session.close()
