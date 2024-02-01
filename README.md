# pyxplor

[![Documentation Status](https://readthedocs.org/projects/pyxplor/badge/?version=latest)](https://pyxplor.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![version](https://img.shields.io/github/v/release/UBC-MDS/pyxplor) ![release](https://img.shields.io/github/release-date/UBC-MDS/pyxplor)
[![ci-cd](https://github.com/UBC-MDS/PyXplor/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/UBC-MDS/PyXplor/actions/workflows/ci-cd.yml)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![Python 3.9.0](https://img.shields.io/badge/python-3.9.0-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![PyPI - Version](https://img.shields.io/pypi/v/PyXplor)](https://pyxplor.readthedocs.io/en/latest/?badge=latest%2F)
[![codecov](https://codecov.io/gh/UBC-MDS/PyXplor/graph/badge.svg?token=pJe5bA9V8z)](https://codecov.io/gh/UBC-MDS/PyXplor)


<img src="https://github.com/UBC-MDS/pyxplor/blob/main/img/pyxplor_logo.png?raw=true" height="300">

A package for simplifying the EDA of different data types!

## About

`pyxplor` is a comprehensive Python package designed to automate and streamline the Exploratory Data Analysis (EDA) process. Tailored for various data types including numeric, categorical, binary, and time series data, `pyxplor` aims to enhance data interpretation through a suite of specialized plotting functions. This package seeks to reduce the complexity and time invested in initial data analysis, making it an essential tool for data scientists and analysts at all levels.

## Documentation

Online documentation can be found [here](https://pyxplor.readthedocs.io/en/latest/?badge=latest/)


## Installation (developers)

Note that the package is still under development.

1. Clone the repository.

```bash
git clone https://github.com/UBC-MDS/PyXplor.git
cd pyxplor
```

2. Create an environment with conda and then activate the environment.

```bash
conda create -n pyxplor python=3.11 -y
conda activate pyxplor
```

3. Install poetry inside the environment.

```bash
conda install poetry
```

4. Run `poetry install`.

```bash
poetry install
```

## Testing

To test that the functions is working properly, run the commands below from the root directory.

```bash
pytest tests/
```

To see the coverage of the tests, run the commands below instead.

```bash
pytest tests/ --cov
```

## Usage

The functions in `pyxplor` are very simple to use. Below is a simple demonstration:

```python
from pyxplor.plot_binary import plot_binary
from pyxplor.plot_categorical import plot_categorical
from pyxplor.plot_numeric import plot_numeric
from pyxplor.plot_time_series import plot_time_series

# a dataframe that contains different types of variables
data = {
    'BinaryVariable': binary_variable,
    'CategoricalVariable': categorical_variable,
    'NumericVariable': numeric_variable,
    'DatetimeVariable': datetime_variable
}

df = pd.DataFrame(data)

binary_variables = ['BinaryVariable']
categorical_variables = ['CategoricalVariable']
numeric_variables = ['NumericVariable']

fig, ax = plot_binary(df, binary_variables, "count")
fig, ax = plot_categorical(df, categorical_variables)
fig, ax = plot_numeric(df, numeric_variables, "hist+kde")
fig, ax = plot_time_series(df, "DatetimeVariable", numeric_variables)
```

## Functions

- `plot_numeric(input_df, list_of_variables, ...)`:
  Plots the distribution of numeric variables in a DataFrame, offering options for histograms, KDE plots, or a combination of both.
- `plot_categorical(input_df, list_of_variables, ...)`:
  Visualizes categorical data by creating bar plots for each categorical variable specified, aiding in understanding frequency distributions.
- `plot_binary(input_df, list_of_variables, ...)`:
  Generates plots for binary variables, either as bar plots or pie charts, to highlight distributions and potential imbalances.
- `plot_time_series(input_df, date_column, value_columns, ...)`:
  Specialized in time-series analysis, this function creates line plots for multiple time series variables, allowing for trend analysis and comparison.


## PyXplor Use in Python Ecosystem

While there are several EDA packages in the Python ecosystem, such as `pandas-profiling` ([link](https://github.com/pandas-profiling/pandas-profiling)) and `sweetviz` ([link](https://github.com/fbdesignpro/sweetviz)), `pyxplor` differentiates itself by offering specialized functions for different data types. This targeted approach enables more nuanced and relevant insights, particularly for binary and time-series data which are often less catered for in existing tools. `pyxplor` complements these existing tools by filling these specific gaps, thus enriching the Python EDA toolkit.

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## Contributors

- Po-Hsun (Ben) Chen (@phchen5)
- Rachel Bouwer (@rbouwer)
- Arturo Boquin (@arturoboquin)
- Iris Luo (@luonianyi)

## License

`pyxplor` was created by Ben Chen, Rachel Bouwer, Arturo Boquin, and Iris Luo. It is licensed under the terms of the MIT license.

## Credits

`pyxplor` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
