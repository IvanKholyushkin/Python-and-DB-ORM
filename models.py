import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=40), unique=True)

    def __str__(self):
        return f"{self.id}: {self.name}"


class Book(Base):
    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=60), unique=True)
    id_publisher = db.Column(db.Integer, db.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f"{self.title}"


class Shop(Base):
    __tablename__ = "shop"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=20), unique=True)

    def __str__(self):
        return f"{self.name}"


class Stock(Base):
    __tablename__ = "stock"

    id = db.Column(db.Integer, primary_key=True)
    id_book = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    id_shop = db.Column(db.Integer, db.ForeignKey("shop.id"), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="Stock")
    sales = relationship("Sale", backref="stock")

    def __str__(self):
        return f"{self.count}"


class Sale(Base):
    __tablename__ = "sale"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    date_sale = db.Column(db.Date, nullable=False)
    id_stock = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"{self.price}, {self.date_sale}, {self.count}"


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
