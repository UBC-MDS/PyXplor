import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import unittest

#test data
np.random.seed(0)
dates = pd.date_range('20200101', periods=730, freq='D')  # 2 years of data
data = pd.DataFrame({
    'date': dates,
    'sales': np.random.rand(730) * 1000,
    'cost_of_goods': np.random.rand(730) * 700,
    'gross_profit': np.random.rand(730) * 300,
    'operational_expenses': np.random.rand(730) * 150,
    'operational_profit': np.random.rand(730) * 150,
    'financial_expenses': np.random.rand(730) * 100,
    'net_profit': np.random.rand(730) * 100
})

#test functions
def setUp(self):
    # Create a sample DataFrame for testing
    self.dates = pd.date_range('2020-01-01', periods=10, freq='D')
    self.data = pd.DataFrame({
        'date': self.dates,
        'sales': range(10),
        'expenses': range(10, 20)
    })

def test_valid_input(self):
    # Test with valid input
    try:
        plot_time_series(self.data, 'date', ['sales', 'expenses'])
    except Exception as e:
        self.fail(f"Valid input raised an exception: {e}")

def test_invalid_date_column(self):
    # Test with invalid date column
    with self.assertRaises(ValueError):
        plot_time_series(self.data, 'invalid_date', ['sales', 'expenses'])

def test_non_numeric_values(self):
    # Test with non-numeric value column
    self.data['non_numeric'] = ['a'] * 10
    with self.assertRaises(ValueError):
        plot_time_series(self.data, 'date', ['non_numeric'])
