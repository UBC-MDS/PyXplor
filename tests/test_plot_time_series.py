import pytest
import pandas as pd
import numpy as np
from plot_time_series import plot_time_series

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
    with pytest.raises(ValueError, match="Invalid frequency 'Y'. Valid options are {'D', 'W', 'M', 'Q', 'A'}."):
        plot_time_series(sample_time_series_data, 'date', ['sales'], freq='Y')

