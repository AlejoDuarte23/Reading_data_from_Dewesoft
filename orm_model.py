from sqlalchemy import create_engine, Column, Integer, Float, DateTime,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Measurement(Base):
    __tablename__ = '16.07.2024_measurements'
    timestamp = Column(DateTime, primary_key=True)
    ai_1 = Column(Float, name='AI 1')
    ai_2 = Column(Float, name='AI 2')
    ai_3 = Column(Float, name='AI 3')
    ai_4 = Column(Float, name='AI 4')
    ai_5 = Column(Float, name='AI 5')
    ai_6 = Column(Float, name='AI 6')
    ai_7 = Column(Float, name='AI 7')
    ai_8 = Column(Float, name='AI 8')
    ai_9 = Column(Float, name='AI 9')
    ai_10 = Column(Float, name='AI 10')
    ai_11 = Column(Float, name='AI 11')
    ai_12 = Column(Float, name='AI 12')
    ai_13 = Column(Float, name='AI 13')
    ai_14 = Column(Float, name='AI 14')
    ai_15 = Column(Float, name='AI 15')
    ai_16 = Column(Float, name='AI 16')



def get_measurements_between_dates(start_date: str, end_date: str):
    start_dt = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    measurements = session.query(Measurement).filter(Measurement.timestamp.between(start_dt, end_dt)).all()
    return measurements

def get_latest_measurements(limit: int = 100):
    measurements = session.query(Measurement).order_by(Measurement.timestamp.desc()).limit(limit).all()
    return measurements

def get_min_max_timestamps():
    min_timestamp = session.query(func.min(Measurement.timestamp)).scalar()
    max_timestamp = session.query(func.max(Measurement.timestamp)).scalar()
    return min_timestamp, max_timestamp


# Initialize the database connection
database_uri = 'sqlite:///E:/Hailcreeck_pre_run/hailcreeck.db'
engine = create_engine(database_uri)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Example usage
start_date = '2024-07-15 15:00:00'
end_date = '2024-07-15 16:00:00'

min_timestamp, max_timestamp = get_min_max_timestamps()

#measurements = get_measurements_between_dates(start_date, end_date)

