import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import pytest
import re

from pyxplor.plot_numeric import plot_numeric

# Set up test data
@pytest.fixture
def test_data_numeric():
    data = {
        'numeric_var1': np.random.normal(0, 1, 100),
        'numeric_var2': np.random.normal(5, 2, 100),
        'numeric_var3': np.random.uniform(1, 10, 100),
        'non_numeric_var': np.random.choice(['A', 'B', 'C'], size=100)
    }
    return pd.DataFrame(data)

# Test non-dataframe input
def test_non_df_input_numeric():
    with pytest.raises(ValueError, match=re.escape("input_df must be a pandas DataFrame.")):
        fig, ax = plot_numeric(None, ['numeric_var1', 'numeric_var2'], 'hist')
        plt.close('all')

# Test for non-numeric columns
def test_non_numeric_columns_numeric(test_data_numeric):
    with pytest.raises(ValueError, match=re.escape("No valid numeric columns found in the provided list_of_variables.")):
        fig, ax = plot_numeric(test_data_numeric, ['non_numeric_var'], 'hist')
        plt.close('all')

# Test case where there are no numeric variables
def test_no_numeric_variables_numeric(test_data_numeric):
    with pytest.raises(ValueError, match=re.escape("No valid numeric columns found in the provided list_of_variables.")):
        fig, ax = plot_numeric(test_data_numeric, ['non_numeric_var'], 'hist')
        plt.close('all')

# Test empty list of variables
def test_empty_list_of_variables_numeric(test_data_numeric):
    with pytest.raises(ValueError, match=re.escape("list_of_variables cannot be an empty list.")):
        fig, ax = plot_numeric(test_data_numeric, [], 'hist')
        plt.close('all')

# Test for larger dataset
def test_large_dataset_numeric():
    # Generate a larger dataset for testing
    data_large = {
        'numeric_var1': np.random.normal(0, 1, 1000),
        'numeric_var2': np.random.normal(5, 2, 1000),
    }
    df_large = pd.DataFrame(data_large)
    
    fig, ax = plot_numeric(df_large, ['numeric_var1', 'numeric_var2'], 'hist+kde')
    assert isinstance(fig, plt.Figure)
    assert isinstance(ax, np.ndarray)
    plt.close('all')

# Test variable not in the dataframe
def test_var_not_in_input_df_numeric(test_data_numeric):
    with pytest.raises(ValueError, match=re.escape("The following variables are not present in the DataFrame:")):
        fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'Random_Variable'], 'hist')
        plt.close('all')
        plt.close('all')

# Test invalid plot_kind
def test_invalid_plot_kind_numeric(test_data_numeric):
    with pytest.raises(ValueError, match=re.escape("Invalid value for 'plot_kind'. It should be either 'hist', 'kde', or 'hist+kde'.")):
        fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'numeric_var2'], 'invalid_plot_kind')
        plt.close('all')

# Test valid figsize
def test_non_tuple_figsize_numeric(test_data_numeric):
    with pytest.raises(ValueError, match=re.escape("figsize must be a tuple of exactly two numbers (integers or floats).")):
        fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'numeric_var2'], 'hist', figsize=[10, 6])
        plt.close('all')

# Test for 'hist' and 'kde' without 'hist+kde'
def test_plot_kind_without_kde_numeric(test_data_numeric):
    fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'numeric_var2'], 'hist')
    assert isinstance(fig, plt.Figure)
    assert isinstance(ax, np.ndarray)

    fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'numeric_var2'], 'kde')
    assert isinstance(fig, plt.Figure)
    assert isinstance(ax, np.ndarray)

# Test correctness of the plots
def test_plot_correctness_numeric(test_data_numeric):
    fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'numeric_var2'], 'hist+kde')
    plt.close('all')

# Test non-string output_path
def test_non_string_output_path_numeric(test_data_numeric):
    with pytest.raises(ValueError, match=re.escape("Output must be a boolean value.")):
        fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'numeric_var2'], 'hist', output=123)
        plt.close('all')

# Test non-numeric super_title_font
def test_non_numeric_super_title_font_numeric(test_data_numeric):
    with pytest.raises(ValueError, match=re.escape("super_title_font must be a number (integer or float).")):
        fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'numeric_var2'], 'hist', super_title_font="abc")
        plt.close('all')

# Test correct return
def test_plot_numeric_return(test_data_numeric):
    fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'numeric_var2'], 'hist')
    assert isinstance(fig, plt.Figure)
    assert isinstance(ax, np.ndarray)
    assert fig._suptitle.get_text() == "Distribution of Numeric Variables"
    rows = math.ceil(math.sqrt(len(['numeric_var1', 'numeric_var2'])))
    cols = math.ceil(len(['numeric_var1', 'numeric_var2']) / rows)
    assert len(ax) == rows * cols

# Test saved output (output_path specified)
def test_output_save_numeric(test_data_numeric, tmp_path):
    output_path = os.path.join(tmp_path, 'numeric_distribution.png')
    fig, ax = plot_numeric(test_data_numeric, ['numeric_var1', 'numeric_var2'], 'hist', (8, 6), output=True)
    assert os.path.exists("numeric_variables.png")
    os.remove("numeric_variables.png")  # Clean up
    plt.close('all')