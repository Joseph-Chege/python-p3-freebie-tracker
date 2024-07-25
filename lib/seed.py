#!/usr/bin/env python3

# Script goes here!

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie
from faker import Faker
import random

fake = Faker()

if __name__ == "__main__":
    engine = create_engine('sqlite:///freebies.db')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.commit()

    #Create fake companies, devs and freebies
    companies = [
        Company(
            name=fake.unique.company(),
            founding_year=fake.unique.year()
        )
    for _ in range(10)]

    session.bulk_save_objects(companies)
    session.commit()

    devs = [
        Dev(
            name=fake.unique.name()
        )
    for _ in range(10)]

    session.bulk_save_objects(devs)
    session.commit()

    freebies = [
        Freebie(
            item_name=fake.unique.word(),
            value=random.randint(1, 100),
            company_id = random.randint(1, 10),
            dev_id = random.randint(1, 10)  
        )
    for _ in range(10)]  
        
    session.bulk_save_objects(freebies)
    session.commit()
      

    



    









