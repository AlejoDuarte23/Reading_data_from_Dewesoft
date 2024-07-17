from orm_model import get_measurements_between_dates, Base, create_engine, sessionmaker , measurements_to_numpy
from datetime import datetime
from scipy.signal  import welch, detrend

import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt  

def apply_detrend(data_array):
    # Apply linear detrending
    detrended_array = detrend(data_array, axis=0)
    return detrended_array

def plot_pdf(array):
    frequencies, psd = welch(array, fs=100, axis=0 ,nperseg=2**12)
    plt.figure()
    for i in range(np.shape(array)[1]):
        plt.plot(frequencies, psd[:,i], label=f'Channel {i+1}')
    plt.xlim([0.5, 50])
    plt.show()

def create_session():
    database_uri = 'sqlite:///E:/Hailcreeck_pre_run/hailcreeck.db'
    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def ploting_data(array1, array2):
    fig, ax1 = plt.subplots()

    # Plot the first dataset on the primary y-axis
    ax1.plot(array1, 'b-')  # 'b-' is the color blue with a solid line
    ax1.set_xlabel('Data points')  # replace with your actual x-axis label
    ax1.set_ylabel('Accelerations [g]', color='b')  # replace with your actual y-axis label
    ax1.tick_params(axis='y', labelcolor='b')

    # Create a second y-axis sharing the same x-axis
    ax2 = ax1.twinx()
    ax2.plot(array2[:, 12], 'r-')  # 'r-' is the color red with a solid line
    ax2.set_ylabel('Micro Strains', color='r')  # replace with your actual y-axis label
    ax2.tick_params(axis='y', labelcolor='r')

    # Show the plot
    plt.show()


if __name__ == "__main__":
    session = create_session()
    start_date = datetime(2024, 7, 17, 9, 30, 0, 0)
    end_date = datetime(2024, 7, 17, 11, 0, 0, 0)
    measurements = get_measurements_between_dates(start_date, end_date, session)
    
    data_array = measurements_to_numpy(measurements)
    detrended_array = apply_detrend(data_array)


    '''
    X_fiter =  detrended_array[:,[0, 2, 4, 6, 8, 10]]
    plot_pdf(X_fiter)
    Y_fiter =  detrended_array[:,[1, 3, 5, 7, 9, 11]]
    plot_pdf(Y_fiter)
    '''
