import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
import json
import configparser
from models import create_tables, Publisher, Book, Shop, Stock, Sale

config = configparser.ConfigParser()
config.read("info.ini")
driver = config["sql"]["sql_driver"]
login = config["login"]["sql_login"]
password = config["password"]["sql_password"]
host = config["host"]["sql_host"]
port = config["port"]["sql_port"]
db_name = config["db_name"]["name"]

DSN = f"{driver}://{login}:{password}@{host}:{port}/{db_name}"
engine = db.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)


with open("tests_data.json", "r") as fd:
    data = json.load(fd)

for record in data:
    model = {
        "publisher": Publisher,
        "shop": Shop,
        "book": Book,
        "stock": Stock,
        "sale": Sale,
    }[record.get("model")]
    session.add(model(id=record.get("pk"), **record.get("fields")))
session.commit()


name = input("Enter the writer's last name or ID: ")

result = session.query(
    Book.title,
    Shop.name,
    Sale.price,
    Sale.date_sale
).join(Publisher).join(Stock).join(Shop).join(Sale)

if name.isdigit():
    result = result.filter(Publisher.id == name).all()
else:
    result = result.filter(Publisher.name == name).all()
for i in result:
    print(f"{i[0]} | {i[1]} | {i[2]} | {i[3]}")

session.close()



