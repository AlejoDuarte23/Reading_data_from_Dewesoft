from win32com.client import Dispatch
import numpy as np
from datetime import datetime
from tqdm import tqdm
from scipy.signal import resample

import os

import matplotlib.pyplot as plt
import pandas  as pd
import json 

def stored_time_engine(engine):
    dw = engine
    stored_time = dw.Data.StartStoreTime
    dt = datetime(stored_time.year, stored_time.month,
                  stored_time.day, stored_time.hour,
                  stored_time.minute, stored_time.second,
                  stored_time.microsecond, stored_time.tzinfo)
    dt64 = np.datetime64(dt)
    time_delta_seconds = dw.Eventlist.Item(0).TimeStamp
    time_delta_ns = np.timedelta64(int(time_delta_seconds * 1e9), 'ns')
    dt64 = dt64 + time_delta_ns

    return dt64
    

def time_stamps_engine(dt64,dw):
    total_samples = dw.LoadEngine.DataSections.Item(0).DataCount
    fs = dw.Data.SampleRate
    interval_ns = int(1e9 / fs)
    timestamps = np.arange(dt64, dt64 + np.timedelta64(interval_ns * total_samples, 'ns'), np.timedelta64(interval_ns, 'ns'))
    # timestamps = timestamps.reshape(-1, 1)
    return timestamps

def datasections_engine(engine):
    dw = engine
    data_sections = dw.LoadEngine.DataSections
    data_section = data_sections.Item(0)
    return data_section

def get_channel_data(c_id,data_section,dw):
    ch = dw.Data.UsedChannels.Item(c_id)
    data , _ =data_section.ReadData(ch)
    return data

def time_stamp_engine_array(dw):

    _dt64 = stored_time_engine(dw)
    _timestamps = time_stamps_engine(_dt64,dw)
    return _timestamps

def get_channelwtime(c_id,dw):
    _timestamps = time_stamp_engine_array()
    data_section = datasections_engine()
    _data = get_channel_data(c_id,data_section,dw=dw)
    _data = np.array(_data)
    stacked_data = np.empty(len(_data), dtype=[('timestamp', 'datetime64[ns]'), ('data', 'float64')])
    stacked_data['timestamp'] = _timestamps
    stacked_data['data'] = _data
    return stacked_data


def get_alldata(selected_chanels,data_section,dw):
    num_columns = len(selected_chanels)
    _data = []
    _timestamps = time_stamp_engine_array()
    for i in range(num_columns):
        _datai = get_channel_data(selected_chanels[i-1],data_section,dw=dw)
        _data.append(_datai)
    dtype = [('timestamp', 'datetime64[ns]')] + [('data' + str(i), 'float64') for i in range(num_columns)]
    stacked_data = np.empty(len(_datai), dtype=dtype)
    stacked_data['timestamp'] = _timestamps
    for i, _datai in enumerate(_data):
        data_array = np.array(_datai)
        stacked_data['data' + str(i)] = data_array
    return stacked_data


def file_nameautomate(_dir,a,b):
    # a initial  dxd file id
    # b last dxd file id
    file_names = []
    base_file_path = _dir
    numbers = range(a,b)    
    for num in numbers:
        file_path = base_file_path.format(str(num).zfill(2))    
        file_names.append(file_path)
    return file_names

def resample_data(data, old_fs, new_fs):
    num_columns = len(data.dtype.names) - 1
    old_len = len(data)
    new_len = int(old_len * new_fs / old_fs)
    resampled_data = np.zeros((new_len, num_columns))
    
    for i in range(num_columns):
        resampled_data[:, i] = resample(data['data' + str(i)], new_len)
    
    resampled_timestamps = pd.date_range(start=data['timestamp'][0], periods=new_len, freq=f'{1 / new_fs * 1e6:.0f}U')
    dtype = [('timestamp', 'datetime64[ns]')] + [('data' + str(i), 'float64') for i in range(num_columns)]
    resampled_stacked_data = np.empty(len(resampled_data), dtype=dtype)
    resampled_stacked_data['timestamp'] = resampled_timestamps
    for i in range(num_columns):
        resampled_stacked_data['data' + str(i)] = resampled_data[:, i]
    
    return resampled_stacked_data

def get_measurements(channel_list:dict,data_section:any, engine:any):
    dw = engine
    df = pd.DataFrame()
    
    df['timestamp']= time_stamp_engine_array(dw)

    for i in range(0, dw.Data.AllChannels.Count):
        selected_channel  = dw.Data.AllChannels.Item(i).Name 
        if (selected_channel in channel_list.keys()):
            print(i)
            df[selected_channel] =  get_channel_data(i,data_section,dw=dw)
    return df


def load_dewesoft_dxd(dxd_file:str):
    dw = Dispatch("Dewesoft.App")
    dw.Init()
    dw.Enabled = 1
    dw.Visible = 1
    dw.Top = 0
    dw.Left = 0
    dw.Width = 1024 
    dw.Height = 768
    dw.LoadFile(dxd_file)
    return dw

def open_json(file = "channel_list.json"):
    with open(file,'r')  as json_file:
        channels_list = json.load(json_file)
    return channels_list

def save_json(data,file = "channel_list.json"):
    with open(file, 'w') as json_file:
        json.dump(data, json_file , indent=4)


def os_walk_folder(root_folder:str):
    file_list = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".dxd"):
                file_list.append(os.path.join(root, file))
    return file_list

