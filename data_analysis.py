from orm_model import get_measurements_between_dates, Base, create_engine, sessionmaker , measurements_to_numpy
from datetime import datetime
from scipy.signal  import welch, detrend

import numpy as np
import matplotlib
import matplotlib.pyplot as plt  



#%matplotlib qt

def apply_detrend(data_array):
    # Apply linear detrending
    detrended_array = detrend(data_array, axis=0)
    return detrended_array

def plot_pdf(array):
    frequencies, psd = welch(array, fs=100, axis=0 ,nperseg=2**12)
    plt.figure()
    for i in range(12):
        plt.plot(frequencies, psd[:,i], label=f'Channel {i+1}')
    
    plt.show()

def create_session():
    database_uri = 'sqlite:///E:/Hailcreeck_pre_run/hailcreeck.db'
    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


if __name__ == "__main__":
    session = create_session()
    start_date = datetime(2024, 7, 15, 11,0, 0, 0)
    end_date = datetime(2024, 7, 15, 12, 0, 0, 0)
    measurements = get_measurements_between_dates(start_date, end_date, session)

    data_array = measurements_to_numpy(measurements)
    detrended_array = apply_detrend(data_array)

    frequencies, psd = welch(detrended_array[:,:12], fs=100, axis=0 ,nperseg=2**12)
    plt.figure()
    for i in range(12):
        plt.plot(frequencies, psd[:,i], label=f'Channel {i+1}')
    plt.show()