import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    
    catalogue_items = relationship("CatalogueItem")

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class CatalogueItem(Base):
    __tablename__ = 'catalogue_item'

    id = Column(Integer, primary_key=True)
    
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    
    price = Column(Numeric(10,2))
    owner = Column(String(250))
    
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'owner': self.owner,
        }


engine = create_engine('sqlite:///sql-catalogue.db')


Base.metadata.create_all(engine)
