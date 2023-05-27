from sqlalchemy import Inspector, create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('sqlite:///shopkz_products.db')

Session = sessionmaker(bind=engine)

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String)
    articul = Column(String)
    price = Column(String, default="Нет в наличии")
    description = Column(Text)
    photo_urls = Column(Text)



def insert_into_table(data_json, table_name):
    class ProductTable(BaseModel):
        __tablename__ = table_name

    session = Session()
    inspector = Inspector.from_engine(engine)

    if table_name not in inspector.get_table_names():
        Base.metadata.create_all(engine)

    for v1 in data_json.values():
        new_record = ProductTable(
            name=v1['name'], 
            articul=v1['articul'], 
            price=v1['price'],
            description=v1['description'], 
            photo_urls=v1['photo_urls']
        )
        session.add(new_record)

    session.commit()
