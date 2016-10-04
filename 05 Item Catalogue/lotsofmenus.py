from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, CatalogueItem, Base

engine = create_engine('sqlite:///sql-catalogue2.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


category1 = Category(name="Food")
session.add(category1)
session.commit()

catItem1_1 = CatalogueItem(name="Carrot",
                     description="Juicy orange root vegetable",
                     price=7.5,
                     category=category1)
session.add(catItem1_1)

catItem1_2 = CatalogueItem(name="Dog Hair",
                     description="Actually not very nice to eat",
                     price=99.95, category=category1)
session.add(catItem1_2)

catItem1_3 = CatalogueItem(name="Cat",
                     description="This... isn't actually a food",
                     price=380.00, category=category1)
session.add(catItem1_3)
session.commit()

# adwdf

category2 = Category(name="Paper")
session.add(category2)
session.commit()

catItem2_1 = CatalogueItem(name="Lined Paper",
                     description="You can write on this",
                     price=380.00, category=category2)
session.add(catItem2_1)
session.commit()

print "Added catalogue items."
