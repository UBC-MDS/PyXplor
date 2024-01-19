import pytest
import pandas as pd
import numpy as np
from plot_time_series import plot_time_series

def create_test_data():
    dates = pd.date_range('2020-01-01', periods=10, freq='D')
    return pd.DataFrame({
        'date': dates,
        'sales': range(10),
        'expenses': range(10, 20)
    })

def test_valid_input():
    data = create_test_data()
    try:
        plot_time_series(data, 'date', ['sales', 'expenses'])
    except Exception as e:
        pytest.fail(f"Valid input raised an exception: {e}")

def test_invalid_date_column():
    data = create_test_data()
    with pytest.raises(ValueError):
        plot_time_series(data, 'invalid_date', ['sales', 'expenses'])

def test_non_numeric_values():
    data = create_test_data()
    data['non_numeric'] = ['a'] * 10
    with pytest.raises(ValueError):
        plot_time_series(data, 'date', ['non_numeric'])
