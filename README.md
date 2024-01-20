# pyxplor

A package for simplifying the EDA of different data types!

## About

`pyxplor` is a comprehensive Python package designed to automate and streamline the Exploratory Data Analysis (EDA) process. Tailored for various data types including numeric, categorical, binary, and time series data, `pyxplor` aims to enhance data interpretation through a suite of specialized plotting functions. This package seeks to reduce the complexity and time invested in initial data analysis, making it an essential tool for data scientists and analysts at all levels.

## Installation (developers)

Note that the package is still under development.

For testing environment: 
- create an environment with conda (then activate the environment conda activate <env-name>)
- Install poetry inside the environment (conda install poetry)
- Run poetry install
- Then you can test it with pytest tests

```bash
$ pip install pyxplor
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
