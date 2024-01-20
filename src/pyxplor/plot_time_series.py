import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_time_series(input_df: pd.DataFrame, 
                     date_column: str, 
                     value_columns: list, 
                     freq: str = 'D', 
                     figsize: tuple = (10, 6),
                     output: bool = False, 
                     super_title: str = "Time Series Analysis",
                     super_title_font: int = 14) -> tuple:
    """Generates line plot visualizations for multiple time-series variables in a DataFrame.

    This function will construct a multiple lineplot of different numerical values over time.
    The time frequency will be adjustable and the function will return the figure and axes object.

    Parameters
    ----------
    input_df : pd.DataFrame
        DataFrame containing the time-series data with date and numeric columns.

    date_column : str
        Name of the column containing date/time information in datetime format.

    value_columns : list
        List of column names containing numeric values to plot as time series.

    freq : str, optional
        Frequency of data aggregation ('D' for daily, 'W' for weekly, etc.). Default is 'D'.

    figsize : tuple[int, int], optional
        Size of the plot as (width, height). Default is (10, 6).

    output : bool, optional
        Whether to output the figure to the current working directory. Default is False.

    super_title : str, optional
        Title for the entire plot. Default is "Time Series Analysis".

    super_title_font : int, optional
        Font size for the super title. Default is 14.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib Figure object.
        
    ax : matplotlib.axes.Axes or array of Axes
        The matplotlib Axes object(s).

    Examples
    --------
    datetime_variable = df["datetime_variable"]
    numerical_variables = ["num_var1", "num_var2", "num_var3"]
    fig, ax = plot_time_series(df, datetime_variable, numerical_variables)
    """

    # Validation checks
    if not isinstance(input_df, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame.")
    
    if input_df.empty:
        raise ValueError("Input DataFrame is empty.")
    
    if date_column not in input_df.columns:
        raise ValueError(f"Date column '{date_column}' not found in DataFrame.")
    
    if not pd.api.types.is_datetime64_any_dtype(input_df[date_column]):
        raise ValueError(f"Date column '{date_column}' must be of datetime type.")
    
    if not value_columns:
        raise ValueError("List of value columns is empty.")
    
    for column in value_columns:
        if column not in input_df.columns:
            raise ValueError(f"Value column '{column}' not found in DataFrame.")
        if not pd.api.types.is_numeric_dtype(input_df[column]):
            raise ValueError(f"Column '{column}' must contain numeric data.")
        
    valid_freqs = {'D', 'W', 'M', 'Q', 'A'}
    if freq not in valid_freqs:
        raise ValueError(f"Invalid frequency. Valid options are 'D', 'W', 'M', 'Q', 'A'.")
    
    if not (isinstance(figsize, tuple) and len(figsize) == 2 and
            all(isinstance(n, (int, float)) and n > 0 for n in figsize)):
        raise ValueError("figsize must be a tuple of two positive numbers.")
    
    if not isinstance(output, bool):
        raise ValueError("Output must be a bool.")
    
    if not isinstance(super_title, str):
        raise ValueError("super_title must be a string.")
    
    if not isinstance(super_title_font, (int, float)):
        raise ValueError("super_title_font must be a number.")

    # Plotting logic
    input_df[date_column] = pd.to_datetime(input_df[date_column])
    num_plots = len(value_columns)
    fig, axes = plt.subplots(num_plots, 1, figsize=figsize, squeeze=False)

    for i, column in enumerate(value_columns):
        ts_data = input_df.set_index(date_column).resample(freq)[column].mean()
        axes[i, 0].plot(ts_data)
        axes[i, 0].set_title(column)
        axes[i, 0].set_xlabel("Date")
        axes[i, 0].set_ylabel("Values")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(super_title, fontsize=super_title_font)

    if output:
        plt.savefig("timeseries_variables.png")

    return fig, axes
