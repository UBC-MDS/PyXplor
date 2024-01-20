import numpy as np
import pandas as pd
import pytest
import math
import sys
import os
import re

from pyxplor.plot_binary import plot_binary

# Test Data
@pytest.fixture
def test_data():
    num_samples = 100
    np.random.seed(0)
    data = {
        'Binary_Variable_1': np.random.choice([0, 1], size=num_samples),
        'Binary_Variable_2': np.random.choice([0, 1], size=num_samples),
        'Binary_Variable_3': np.random.choice([0, 1], size=num_samples),
        'Binary_Variable_4': np.random.choice([0, 1], size=num_samples),
        'Categorical_Variable_5': np.random.choice([0, 4], size=num_samples),
    }
    return pd.DataFrame(data)

binary_columns = ["Binary_Variable_1", "Binary_Variable_2", "Binary_Variable_3",]
no_binary_variables = len(binary_columns)

# test error raised by invalid input
def test_non_df_input():
    with pytest.raises(ValueError, match=re.escape("input_df must be a pandas DataFrame.")):
        plot_binary("not_df", binary_columns, "count", 10, 10)

# test variable not in the dataframe
def test_var_not_in_df(test_data):
    with pytest.raises(ValueError, match=re.escape("The following variables are not present in the DataFrame: random_var.")):
        plot_binary(test_data, ["random_var"], "count", 10, 10)

# test not all variables are binary
def test_binary_variables(test_data):
    with pytest.raises(ValueError, match=re.escape("Variable 'Categorical_Variable_5' is not binary.")):
        plot_binary(test_data, ["Categorical_Variable_5"], "count", 10, 10)

# test valid input plot kind
def test_valid_plot_kind(test_data):
    with pytest.raises(ValueError, match=re.escape("Invalid value for 'plot_kind'. It should be either 'count' or 'pie'.")):
        plot_binary(test_data, binary_columns, "line", 10, 10)

# test valid input label_offset
def test_valid_label_offset(test_data):
    with pytest.raises(ValueError, match=re.escape("label_offset must be a number (integers or floats).")):
        plot_binary(test_data, binary_columns, "count", "string", 10)

# test valid input label_fontsize
def test_valid_label_fontsize(test_data):
    with pytest.raises(ValueError, match=re.escape("label_fontsize must be a number (integers or floats).")):
        plot_binary(test_data, binary_columns, "count", 10, "string")

# test valid input plot_orientation
def test_valid_plot_orientation(test_data):
    with pytest.raises(ValueError, match=re.escape("Invalid value for 'plot_orientation'. It should be either 'h' or 'v'.")):
        plot_binary(test_data, binary_columns, "count", 10, 10, "a")

# test valid input figsize
def test_valid_figsize(test_data):
    with pytest.raises(ValueError, match=re.escape("figsize must be a tuple of exactly two numbers (integers or floats).")):
        plot_binary(test_data, binary_columns, "count", 10, 10, "v", (1, "str"))

# test valid input output
def test_valid_output(test_data):
    with pytest.raises(ValueError, match=re.escape("Output must be a boolean value.")):
        plot_binary(test_data, binary_columns, "count", 10, 10, "v", (15, 15), "True")

# test valid input supertitle
def test_valid_suptitle(test_data):
    with pytest.raises(ValueError, match=re.escape("super_title must be a string.")):
        plot_binary(test_data, binary_columns, "count", 10, 10, "v", (15, 15), False, 123)

# test valid input supertitle fontsize
def test_valid_suptitle_fontsize(test_data):
    with pytest.raises(ValueError, match=re.escape("super_title_font must be a number (integer or float).")):
        plot_binary(test_data, binary_columns, "count", 10, 10, "v", (15, 15), False, "Title", "1")

def test_output_save_binary(test_data):
    _, _ = plot_binary(test_data, binary_columns, "count", 10, 10, "h", (6, 6), True)
    assert os.path.exists("binary_variables.png")
    os.remove("binary_variables.png")  # Clean up

# test figure
def test_figure(test_data):
    fig, _ = plot_binary(test_data, binary_columns, "count", 10, 10, "h", (6, 6), False)
    # test supertitle
    assert fig._suptitle.get_text() == "Distribution of Binary Variables"
    # test number of axes
    rows = math.ceil(math.sqrt(no_binary_variables))
    cols = math.ceil(no_binary_variables / rows) 
    assert len(fig.get_axes()) == rows * cols

# test subplot titles
def test_subplot_title(test_data):
    _, ax = plot_binary(test_data, binary_columns, "count", 10, 10, "h", (6, 6), False)
    subplot_titles = [ax[i].title.get_text() for i in range(no_binary_variables)]
    correct_titles = [variable for variable in binary_columns]
    assert subplot_titles == correct_titles

# for count plots
def test_number_of_bars(test_data):
    # check number of bars for horizontal orientation
    _, ax_h = plot_binary(test_data, binary_columns, "count", 10, 10, "h", (6, 6), False)
    assert [len(ax_h[i].get_yticks()) for i in range(no_binary_variables)] == [2 for _ in range(no_binary_variables)]
    # check number of bars for vertical orientation
    _, ax_v = plot_binary(test_data, binary_columns, "count", 10, 10, "v", (6, 6), False)
    assert [len(ax_v[i].get_xticks()) for i in range(no_binary_variables)] == [2 for _ in range(no_binary_variables)]

# test count annotations
def test_count_annotations(test_data):
    _, ax = plot_binary(test_data, binary_columns, "count", 10, 10, "h", (6, 6), False)
    for i, variable in enumerate(binary_columns):
        assert sorted(list(test_data[variable].value_counts())) == sorted([int(text.get_text()) for text in ax[i].texts])

# for pie charts
def test_number_of_wedges(test_data):
    # check the number of wedges for pie charts
    _, ax = plot_binary(test_data, binary_columns, "pie", 10, 10, "h", (6, 6), False)
    assert [len(ax[i].patches) for i in range(no_binary_variables)] == [2 for _ in range(no_binary_variables)]

# test pie annotations
def test_pie_annotations(test_data):
    _, ax = plot_binary(test_data, binary_columns, "pie", 10, 10, "h", (6, 6), False)

    # go through each variable
    for i, variable in enumerate(binary_columns):
        pie_annotations = []

        for text in ax[i].texts:
            if text.get_text() == "":
                continue
            # extract the count from the label
            input_string = text.get_text()
            start_index = input_string.find('(')
            end_index = input_string.find(')', start_index)
            # append the count to list
            pie_annotations.append(int(input_string[start_index+1:end_index]))

        assert sorted(list(test_data[variable].value_counts())) == sorted(pie_annotations)