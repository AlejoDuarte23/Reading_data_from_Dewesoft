from sqlalchemy import create_engine, Column, Integer, Float, DateTime,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import numpy as np
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



def get_measurements_between_dates(start_date, end_date, session):
    measurements = session.query(Measurement).filter(Measurement.timestamp.between(start_date, end_date)).all()
    return measurements

def get_latest_measurements(session,limit=100):
    measurements = session.query(Measurement).order_by(Measurement.timestamp.desc()).limit(limit).all()
    return measurements

def get_min_max_timestamps(session):
    min_timestamp = session.query(func.min(Measurement.timestamp)).scalar()
    max_timestamp = session.query(func.max(Measurement.timestamp)).scalar()
    return min_timestamp, max_timestamp


def measurements_to_numpy(measurements):
    data_list = []
    for measurement in measurements:
        row = [
            measurement.ai_1,
            measurement.ai_2,
            measurement.ai_3,
            measurement.ai_4,
            measurement.ai_5,
            measurement.ai_6,
            measurement.ai_7,
            measurement.ai_8,
            measurement.ai_9,
            measurement.ai_10,
            measurement.ai_11,
            measurement.ai_12,
            measurement.ai_13,
            measurement.ai_14,
            measurement.ai_15,
            measurement.ai_16
        ]
        data_list.append(row)
    data_array = np.array(data_list)
    return data_array
