"""

    Helper functions for the pretrained model to be used within our API.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.

    Importantly, you will need to modify this file by adding
    your own data preprocessing steps within the `_preprocess_data()`
    function.
    ----------------------------------------------------------------------

    Description: This file contains several functions used to abstract aspects
    of model interaction within the API. This includes loading a model from
    file, data preprocessing, and model prediction.  

"""

# Helper Dependencies
import numpy as np
import pandas as pd
import pickle
import json

def _preprocess_data(data):
    """Private helper function to preprocess data for model prediction.

    NB: If you have utilised feature engineering/selection in order to create
    your final model you will need to define the code here.


    Parameters
    ----------
    data : str
        The data payload received within POST requests sent to our API.

    Returns
    -------
    Pandas DataFrame : <class 'pandas.core.frame.DataFrame'>
        The preprocessed data, ready to be used our model for prediction.
    """
    # Convert the json string to a python dictionary object
    feature_vector_dict = json.loads(data)
    # Load the dictionary as a Pandas DataFrame.
    feature_vector_df = pd.DataFrame.from_dict([feature_vector_dict])

    # ---------------------------------------------------------------
    # NOTE: You will need to swap the lines below for your own data
    # preprocessing methods.
    #
    # The code below is for demonstration purposes only. You will not
    # receive marks for submitting this code in an unchanged state.
    # ---------------------------------------------------------------

    # ----------- Replace this code with your own preprocessing steps --------
    # 1. Replacing null values in 'valencia_pressure' with the feature median value
    feature_vector_df.columns = feature_vector_df.columns.str.lower()
    feature_vector_df =  feature_vector_df[['time', 'barcelona_pressure', 'barcelona_rain_1h', 'barcelona_rain_3h',
       'barcelona_temp', 'barcelona_temp_max', 'barcelona_temp_min',
       'barcelona_weather_id', 'barcelona_wind_deg', 'barcelona_wind_speed',
       'bilbao_clouds_all', 'bilbao_pressure', 'bilbao_rain_1h',
       'bilbao_snow_3h', 'bilbao_temp', 'bilbao_temp_max', 'bilbao_temp_min',
       'bilbao_weather_id', 'bilbao_wind_deg', 'bilbao_wind_speed',
       'madrid_clouds_all', 'madrid_humidity', 'madrid_pressure',
       'madrid_rain_1h', 'madrid_temp', 'madrid_temp_max', 'madrid_temp_min',
       'madrid_weather_id', 'madrid_wind_speed', 'seville_clouds_all',
       'seville_humidity', 'seville_pressure', 'seville_rain_1h',
       'seville_rain_3h', 'seville_temp', 'seville_temp_max',
       'seville_temp_min', 'seville_weather_id', 'seville_wind_speed',
       'valencia_humidity', 'valencia_pressure', 'valencia_snow_3h',
       'valencia_temp', 'valencia_temp_max', 'valencia_temp_min',
       'valencia_wind_deg', 'valencia_wind_speed']]

    # 2. Replacing null values in 'valencia_pressure' with the feature median value
    feature_vector_df['valencia_pressure'] = feature_vector_df['valencia_pressure'].fillna(1015.0)
    # 3. Converting categorical features to a numeric format
    feature_vector_df['valencia_wind_deg']= feature_vector_df['valencia_wind_deg'].str.extract('(\d+)')
    feature_vector_df['valencia_wind_deg'] = pd.to_numeric(feature_vector_df['valencia_wind_deg'])
    feature_vector_df['seville_pressure']= feature_vector_df['seville_pressure'].str.extract('(\d+)')
    feature_vector_df['seville_pressure'] = pd.to_numeric(feature_vector_df['seville_pressure'])
    # 4. Changing time colum from string type to datetime object and then to a delta time feature
    feature_vector_df['time'] = pd.to_datetime(feature_vector_df['time'])
    # 5. Splitting the time column
    feature_vector_df['year'] = feature_vector_df['time'].dt.year
    feature_vector_df['month'] = feature_vector_df['time'].dt.month
    feature_vector_df['day'] = feature_vector_df['time'].dt.day
    feature_vector_df['hour'] = feature_vector_df['time'].dt.hour
    feature_vector_df['minute'] = feature_vector_df['time'].dt.minute
    feature_vector_df['second'] = feature_vector_df['time'].dt.second
    # 6. Reordering the columns to place time features first
    feature_vector_df = feature_vector_df.drop(['time'], axis=1)
    # 7. Dropping the target variable to create the predict vector
    predict_vector = feature_vector_df #.to_numpy(copy=True)

    # ------------------------------------------------------------------------

    return predict_vector

def load_model(path_to_model:str):
    """Adapter function to load our pretrained model into memory.

    Parameters
    ----------
    path_to_model : str
        The relative path to the model weights/schema to load.
        Note that unless another file format is used, this needs to be a
        .pkl file.

    Returns
    -------
    <class: sklearn.estimator>
        The pretrained model loaded into memory.

    """
    return pickle.load(open(path_to_model, 'rb'))


""" You may use this section (above the make_prediction function) of the python script to implement 
    any auxiliary functions required to process your model's artifacts.
"""

def make_prediction(data, model):
    """Prepare request data for model prediction.

    Parameters
    ----------
    data : str
        The data payload received within POST requests sent to our API.
    model : <class: sklearn.estimator>
        An sklearn model object.

    Returns
    -------
    list
        A 1-D python list containing the model prediction.

    """
    # Data preprocessing.
    prep_data = _preprocess_data(data)
    # Perform prediction with model and preprocessed data.
    prediction = model.predict(prep_data)
    # Format as list for output standardisation.
    return prediction.tolist()
