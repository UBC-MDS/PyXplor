import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import re

import pytest

# Import the plot_categorical function from the src/pyxplor folder
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/pyxplor'))
from plot_categorical import plot_categorical

# Set up test data
@pytest.fixture
def test_data():
    data = {
        'Categorical_Variable_1': np.random.choice(['A', 'B', 'C'], size=100),
        'Categorical_Variable_2': np.random.choice(['X', 'Y', 'Z'], size=100),
        'Categorical_Variable_3': np.random.choice(['Apple', 'Banana', 'Orange'], size=100),
        'Binary_Variable_4': np.random.choice([0, 1], size=100)
    }
    return pd.DataFrame(data)

# Test non-dataframe input
def test_non_df_input():
    with pytest.raises(ValueError, match=re.escape("input_df must be a pandas DataFrame.")):
        plot_categorical(None, ['Categorical_Variable_1', 'Categorical_Variable_2'])

# Test empty list of variables
def test_empty_list_of_variables(test_data):
    with pytest.raises(ValueError, match=re.escape("list_of_variables cannot be an empty list.")):
        plot_categorical(test_data, [])

# Test variable not in the dataframe
def test_var_not_in_input_df(test_data):
    with pytest.raises(ValueError, match=re.escape("The following variables are not present in the DataFrame:")):
        plot_categorical(test_data, ['Categorical_Variable_1', 'Random_Variable'])

# Test valid label fontsize
def test_non_numeric_label_fontsize(test_data):
    with pytest.raises(ValueError, match=re.escape("label_fontsize must be a number (integers or floats).")):
        plot_categorical(test_data, ['Categorical_Variable_1', 'Categorical_Variable_2'], label_fontsize="abc")

# Test valid figsize
def test_non_tuple_figsize(test_data):
    with pytest.raises(ValueError, match=re.escape("figsize must be a tuple of exactly two numbers (integers or floats).")):
        plot_categorical(test_data, ['Categorical_Variable_1', 'Categorical_Variable_2'], figsize=[10, 6])

# Test non-boolean output parameter
def test_non_boolean_output_flag(test_data):
    with pytest.raises(ValueError, match=re.escape("Output must be a boolean value.")):
        plot_categorical(test_data, ['Categorical_Variable_1', 'Categorical_Variable_2'], output="True")

# Test valid super title
def test_non_string_super_title(test_data):
    with pytest.raises(ValueError, match=re.escape("super_title must be a string.")):
        plot_categorical(test_data, ['Categorical_Variable_1', 'Categorical_Variable_2'], super_title=123)

# Test valid super title font size
def test_non_numeric_super_title_fontsize(test_data):
    with pytest.raises(ValueError, match=re.escape("super_title_fontsize must be a number (integer or float).")):
        plot_categorical(test_data, ['Categorical_Variable_1', 'Categorical_Variable_2'], super_title_fontsize="abc")

# Test correct return
def test_plot_categorical_return(test_data):
    fig, ax = plot_categorical(test_data, test_data.columns.to_list())
    assert isinstance(fig, plt.Figure)
    assert isinstance(ax, np.ndarray)
    assert fig._suptitle.get_text() == "Distribution of Categorical Variables"
    rows = math.ceil(math.sqrt(len(test_data.columns.to_list())))
    cols = math.ceil(len(test_data.columns.to_list()) / rows) 
    assert len(ax) == rows * cols

# Test subplot titles
def test_subplot_title(test_data):
    _, ax = plot_categorical(test_data, test_data.columns.to_list())
    subplot_titles = [ax[i].title.get_text() for i in range(len(test_data.columns.to_list()))]
    correct_titles = ['{}'.format(variable) for variable in test_data.columns.to_list()]
    assert subplot_titles == correct_titles
