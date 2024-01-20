import pytest
import pandas as pd
import numpy as np
import re
import os

from pyxplor.plot_time_series import plot_time_series

@pytest.fixture
def sample_time_series_data():
    dates = pd.date_range('20200101', periods=100, freq='D')
    data = pd.DataFrame({
        'date': dates,
        'sales': np.random.rand(100) * 1000,
        'expenses': np.random.rand(100) * 500
    })
    return data

def test_valid_input(sample_time_series_data):
    fig, ax = plot_time_series(sample_time_series_data, 'date', ['sales', 'expenses'], freq='M')
    assert fig is not None
    assert ax is not None

def test_empty_dataframe():
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError, match="Input DataFrame is empty."):
        plot_time_series(empty_df, 'date', ['sales'], freq='M')

def test_invalid_date_column(sample_time_series_data):
    with pytest.raises(ValueError, match="Date column 'invalid_date' not found in DataFrame."):
        plot_time_series(sample_time_series_data, 'invalid_date', ['sales'], freq='M')

def test_nonexistent_value_column(sample_time_series_data):
    with pytest.raises(ValueError, match="Value column 'nonexistent' not found in DataFrame."):
        plot_time_series(sample_time_series_data, 'date', ['nonexistent'], freq='M')

def test_non_numeric_value_column(sample_time_series_data):
    sample_time_series_data['non_numeric'] = ['a'] * 100
    with pytest.raises(ValueError, match="Column 'non_numeric' must contain numeric data."):
        plot_time_series(sample_time_series_data, 'date', ['non_numeric'], freq='M')

def test_invalid_frequency(sample_time_series_data):
    with pytest.raises(ValueError, match=re.escape("Invalid frequency. Valid options are 'D', 'W', 'M', 'Q', 'A'.")):
        plot_time_series(sample_time_series_data, 'date', ['sales'], freq='Y')
        
def test_non_datetime_date_column(sample_time_series_data):
    sample_time_series_data['non_datetime_date'] = '2020-01-01'
    with pytest.raises(ValueError, match="Date column 'non_datetime_date' must be of datetime type."):
        plot_time_series(sample_time_series_data, 'non_datetime_date', ['sales'], freq='M')

def test_invalid_figsize(sample_time_series_data):
    with pytest.raises(ValueError, match="figsize must be a tuple of two positive numbers."):
        plot_time_series(sample_time_series_data, 'date', ['sales'], figsize=(10, -6))

def test_output_path_generation(sample_time_series_data, tmp_path):
    fig, ax = plot_time_series(sample_time_series_data, 'date', ['sales'], output=True)
    assert fig is not None

def test_invalid_super_title(sample_time_series_data):
    with pytest.raises(ValueError, match="super_title must be a string."):
        plot_time_series(sample_time_series_data, 'date', ['sales'], super_title=123)

def test_invalid_date_column_type(sample_time_series_data):
    sample_time_series_data['string_date'] = '2020-01-01'
    with pytest.raises(ValueError, match="Date column 'string_date' must be of datetime type."):
        plot_time_series(sample_time_series_data, 'string_date', ['sales'], freq='M')

def test_invalid_freq(sample_time_series_data):
    with pytest.raises(ValueError, match="Invalid frequency. Valid options are 'D', 'W', 'M', 'Q', 'A'."):
        plot_time_series(sample_time_series_data, 'date', ['sales'], freq='Y')

def test_invalid_super_title_font(sample_time_series_data):
    with pytest.raises(ValueError, match="super_title_font must be a number."):
        plot_time_series(sample_time_series_data, 'date', ['sales'], super_title_font='large')

