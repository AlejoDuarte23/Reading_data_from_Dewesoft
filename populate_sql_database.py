from get_data_from_dwd import ( open_json,load_dewesoft_dxd, 
                            datasections_engine,
                            get_measurements,
                            save_json,
                            os_walk_folder)

import pandas as pd
from sqlalchemy import create_engine



def save_df_to_sql(df: pd.DataFrame, table_name: str, database_uri: str):
    engine = create_engine(database_uri)    
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

def dxd2df(dxd_file):
    channels_list = open_json()
    dw = load_dewesoft_dxd(dxd_file=dxd_file)
    data_section = datasections_engine(dw)
    df = get_measurements(channel_list=channels_list,data_section=data_section,engine=dw)

    return  df

if __name__ == "__main__":

    dxd_list = os_walk_folder(root_folder=r"E:\Hailcreeck_pre_run")
    database_uri = 'sqlite:///E:/Hailcreeck_pre_run/hailcreeck.db'
    table_name = '16.07.2024_measurements'

    for dxd_file in dxd_list:
        df = dxd2df(dxd_file)
        save_df_to_sql(df, table_name, database_uri)
