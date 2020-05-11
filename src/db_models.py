from sqlalchemy import Column, Integer, String, Date, Float, Boolean, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    author = Column(String(255))
    description = Column(String(1000))
    isbn = Column(Integer)
    pages = Column(Integer)
    published = Column(String(10))
    publisher = Column(String(255))
    subtitle = Column(String(255))
    title = Column(String(255))
    website = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    user_ref = relationship('User', back_populates='book_ref')

    def __repr__(self):
        return f'Book(id={self.id}, ' \
               f'author=\'{self.author}\',' \
               f'description=\'{self.description}\',' \
               f'isbn={self.isbn},' \
               f'pages={self.pages},' \
               f'published=\'{self.published}\',' \
               f'publisher=\'{self.publisher}\',' \
               f'subtitle=\'{self.subtitle}\',' \
               f'title=\'{self.title}\',' \
               f'website=\'{self.website}\')'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(255))
    password = Column(String(255))
    permission_lvl = Column(Integer)
    book_ref = relationship('Book', back_populates='user_ref')

    def __repr__(self):
        return f'User(id={self.id}, ' \
               f'username=\'{self.username}\', ' \
               f'email=\'{self.email}\', ' \
               f'password=\'{self.password}\', ' \
               f'permission_lvl=\'{self.permission_lvl}\')'
