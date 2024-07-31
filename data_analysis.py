from orm_model import get_measurements_between_dates, Base, create_engine, sessionmaker , measurements_to_numpy ,create_measurement_class,get_latest_measurements
from datetime import datetime
from scipy.signal  import welch, detrend
from config import database_uri_local, connection_string, table_name


from Modal_Engine._engine import (SingleMeasurement,
                                  FFTDomain,
                                  DataVisualizer)

import pickle
import numpy as np
import matplotlib.pyplot as plt  

def apply_detrend(data_array):
    # Apply linear detrending
    detrended_array = detrend(data_array, axis=0)
    return detrended_array

def plot_psd(array):
    frequencies, psd = welch(array, fs=100, axis=0 ,nperseg=2**12)
    plt.figure()
    for i in range(np.shape(array)[1]):
        plt.plot(frequencies, psd[:,i], label=f'Channel {i+1}')
    plt.xlim([0.5, 50])
    plt.show()

def create_session(database_uri):
    #database_uri = database_uri_local
    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def ploting_data(array1, array2):
    fig, ax1 = plt.subplots()

    ax1.plot(array1, 'b-')  # 'b-' is the color blue with a solid line
    ax1.set_xlabel('Data points')  # replace with your actual x-axis label
    ax1.set_ylabel('Accelerations [g]', color='b')  # replace with your actual y-axis label
    ax1.tick_params(axis='y', labelcolor='b')

    ax2 = ax1.twinx()
    ax2.plot(array2[:, 12], 'r-')  # 'r-' is the color red with a solid line
    ax2.set_ylabel('Micro Strains', color='r')  # replace with your actual y-axis label
    ax2.tick_params(axis='y', labelcolor='r')

    # Show the plot
    plt.show()

def save_pickle(data:any, filename:str)-> None:
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_pickle(filename:str)-> any:
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def plt_spectrogram(measurement: SingleMeasurement):
    fdomain = FFTDomain(measurement,NFFT=2**6)
    fdomain.fft()
    data_vis1 = DataVisualizer(fdomain)
    data_vis1.plot_spectrogram(cmap='jet')

def get_data_array():
    session = create_session(connection_string)
    start_date = datetime(2024, 7, 27, 20, 25, 0, 0)
    end_date = datetime(2024, 7, 27, 22, 25, 0, 0)
    Measurement = create_measurement_class(table_name)
    measurements = get_measurements_between_dates(start_date, end_date, session, Measurement)
    
    data_array = measurements_to_numpy(measurements)
    save_pickle(data_array, "measurements_2024/7/27:20:25_2h.pkl")
    return data_array

if __name__ == "__main__":

    file_name = "data/measurements_2024_7_27:20:25_2h.pkl"
    data_set_time = "2024/7/27:20:25"
    data_array = load_pickle(file_name)
    filter = [0, 2, 4]
    measurement_1 = SingleMeasurement(name =  f"{data_set_time} - ROM1 X", fs = 100,file_path= None,
                                      description="2h test")
    measurement_1 = measurement_1.set_data(data_array[:,filter]).resample(30)
    plt_spectrogram(measurement_1)


    filter = [1, 3, 5]
    measurement_2 = SingleMeasurement(name =  f"{data_set_time}  - ROM1 Y", fs = 100,file_path= None,
                                      description="1h test")
    measurement_2 = measurement_2.set_data(data_array[:,filter]).resample(30)
    plt_spectrogram(measurement_2)



    filter = [6, 8, 10]
    measurement_3 = SingleMeasurement(name =  f"{data_set_time}  - ROM2 X", fs = 100,file_path= None,
                                      description="1h test")
    measurement_3 = measurement_3.set_data(data_array[:,filter]).resample(30)
    plt_spectrogram(measurement_3)



    filter = [7, 9, 11]
    measurement_4 = SingleMeasurement(name =  f"{data_set_time}  - ROM2 Y", fs = 100,file_path= None,
                                      description="1h test")
    measurement_4 = measurement_4.set_data(data_array[:,filter])
    plt_spectrogram(measurement_4)









