import numpy as np
import pandas as pd
import pytest
import math
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/pyxplor'))
from plot_binary import plot_binary

# Test Data
num_samples = 100
np.random.seed(0)
data = {
    'Binary_Variable_1': np.random.choice([0, 1], size=num_samples),
    'Binary_Variable_2': np.random.choice([0, 1], size=num_samples),
    'Binary_Variable_3': np.random.choice([0, 1], size=num_samples),
    'Binary_Variable_4': np.random.choice([0, 1], size=num_samples),
    'Categorical_Variable_5': np.random.choice([0, 4], size=num_samples),
}
df = pd.DataFrame(data)
binary_columns = [
    "Binary_Variable_1",
    "Binary_Variable_2", 
    "Binary_Variable_3",
    # "Binary_Variable_4"
]
no_binary_variables = len(binary_columns)

# test error raised by invalid input
def test_non_df_input():
    with pytest.raises(ValueError):
        plot_binary("not_df", binary_columns, "count", 10, 10)

# test variable not in the dataframe
def test_var_not_in_df():
    with pytest.raises(ValueError):
        plot_binary(df, ["random_var"], "count", 10, 10)

# test not all variables are binary
def test_binary_variables():
    with pytest.raises(ValueError):
        plot_binary(df, ["Categorical_Variable_5"], "count", 10, 10)

# test valid input plot kind
def test_valid_plot_kind():
    with pytest.raises(ValueError):
        plot_binary(df, binary_columns, "line", 10, 10)

# test valid input label_offset
def test_valid_label_offset():
    with pytest.raises(ValueError):
        plot_binary(df, binary_columns, "count", "string", 10)

# test valid input label_fontsize
def test_valid_label_fontsize():
    with pytest.raises(ValueError):
        plot_binary(df, binary_columns, "count", 10, "string")

# test valid input plot_orientation
def test_valid_plot_orientation():
    with pytest.raises(ValueError):
        plot_binary(df, binary_columns, "count", 10, 10, "a")

# test valid input figsize
def test_valid_figsize():
    with pytest.raises(ValueError):
        plot_binary(df, binary_columns, "count", 10, 10, "v", (1, "str"))

# test valid input output
def test_valid_output():
    with pytest.raises(ValueError):
        plot_binary(df, binary_columns, "count", 10, 10, "v", (15, 15), "True")

# test valid input supertitle
def test_valid_suptitle():
    with pytest.raises(ValueError):
        plot_binary(df, binary_columns, "count", 10, 10, "v", (15, 15), True, 123)

# test valid input supertitle fontsize
def test_valid_suptitle_fontsize():
    with pytest.raises(ValueError):
        plot_binary(df, binary_columns, "count", 10, 10, "v", (15, 15), True, "Title", "1")

# test figure
def test_figure():
    fig, _ = plot_binary(df, binary_columns, "count", 10, 10, "h", (6, 6), True)
    # test supertitle
    assert fig._suptitle.get_text() == "Distribution of Binary Variables"
    # test number of axes
    rows = math.ceil(math.sqrt(no_binary_variables))
    cols = math.ceil(no_binary_variables / rows) 
    assert len(fig.get_axes()) == rows * cols

# test subplot titles
def test_subplot_title():
    _, ax = plot_binary(df, binary_columns, "count", 10, 10, "h", (6, 6), True)
    subplot_titles = [ax[i].title.get_text() for i in range(no_binary_variables)]
    correct_titles = ['Distribution of {}'.format(variable) for variable in binary_columns]
    assert subplot_titles == correct_titles

# for count plots
def test_number_of_bars():
    # check number of bars for horizontal orientation
    _, ax_h = plot_binary(df, binary_columns, "count", 10, 10, "h", (6, 6), True)
    assert [len(ax_h[i].get_yticks()) for i in range(no_binary_variables)] == [2 for _ in range(no_binary_variables)]
    # check number of bars for vertical orientation
    _, ax_v = plot_binary(df, binary_columns, "count", 10, 10, "v", (6, 6), True)
    assert [len(ax_v[i].get_xticks()) for i in range(no_binary_variables)] == [2 for _ in range(no_binary_variables)]

# test count annotations
def test_count_annotations():
    _, ax = plot_binary(df, binary_columns, "count", 10, 10, "h", (6, 6), True)
    for i, variable in enumerate(binary_columns):
        assert sorted(list(df[variable].value_counts())) == sorted([int(text.get_text()) for text in ax[i].texts])

# for pie charts
def test_number_of_wedges():
    # check the number of wedges for pie charts
    _, ax = plot_binary(df, binary_columns, "pie", 10, 10, "h", (6, 6), True)
    assert [len(ax[i].patches) for i in range(no_binary_variables)] == [2 for _ in range(no_binary_variables)]

# test pie annotations
def test_pie_annotations():
    _, ax = plot_binary(df, binary_columns, "pie", 10, 10, "h", (6, 6), True)

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

        assert sorted(list(df[variable].value_counts())) == sorted(pie_annotations)