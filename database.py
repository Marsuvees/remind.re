from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from dateutil.relativedelta import relativedelta

engine = create_engine('sqlite:///database.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class ReminderDetails(Base):
    __tablename__ ='reminder_details'
    id = Column(Integer, primary_key=True)
    tenant_name = Column(String)
    tenant_phone_number = Column(String)
    rent_amount = Column(Integer)
    rent_period_in_months = Column(Integer)
    date_of_initial_payment = Column(Date, default=datetime.today())
    rent_expiry_date = Column(Date, default=datetime.today()+relativedelta(months=12))

if __name__ == '__main__': 
    Base.metadata.create_all(engine)
    template = ReminderDetails(tenant_name="tenant3", tenant_phone_number="1234567890", rent_amount=1000, date_of_initial_payment=datetime(2023, 8, 23), rent_period_in_months=2)
    session.add(template)
    session.commit()