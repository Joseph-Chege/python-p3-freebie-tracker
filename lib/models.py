from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

#Create a Table object
company_dev = Table(
    'company_dev', 
    Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id'), primary_key=True),
    Column('dev_id', Integer, ForeignKey('devs.id'), primary_key=True),
    extend_existing=True,
)

#Company Class Definition
class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship("Freebie", backref=backref("company"))
    devs = relationship("Dev", secondary=company_dev, back_populates="companies")

    def __repr__(self):
        return f'<Company: {self.name}, id: {self.id}, founding-year: {self.founding_year}>'
    
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(new_freebie)
        session.commit()

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship("Freebie", backref=backref("dev"))
    companies = relationship("Company", secondary=company_dev, back_populates="devs")

    def __repr__(self):
        return f'<Dev: {self.name}, id: {self.id}>'
    
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            session.commit()


#Freebie Class Definition
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    dev = relationship("Dev", back_populates="freebies")
    company = relationship("Company", back_populates="freebies")

    def __repr__(self):
        return f'<Freebie: {self.item_name}, value: {self.value}, company-id: {self.company_id}, dev-id: {self.dev_id}>'
    
    def print_details(self):
        print(f'{self.dev.name} owns a {self.item_name} from {self.company.name}')   

    
    