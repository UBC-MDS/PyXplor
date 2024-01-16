import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_time_series(input_df: pd.DataFrame, 
                     date_column: str, 
                     value_columns: list, 
                     freq: str = 'D', 
                     figsize: tuple = (10, 6),
                     output_path: str = None, 
                     super_title: str = "Time Series Analysis",
                     super_title_font: int = 14) -> None:
    """
    Generates line plot visualizations for multiple time-series variables in a DataFrame.

    This function creates a figure with subplots for each specified time series variable,
    aggregated at a given frequency. It allows for comparisons of trends and seasonality.

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

    output_path : str, optional
        File path to save the plot. If None, the plot is not saved.

    super_title : str, optional
        Title for the entire plot. Default is "Time Series Analysis".

    super_title_font : int, optional
        Font size for the super title. Default is 14.

    Returns
    -------
    None
    """

    if not isinstance(input_df, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame.")

    if date_column not in input_df.columns:
        raise ValueError(f"Date column '{date_column}' not found in DataFrame.")

    input_df[date_column] = pd.to_datetime(input_df[date_column])

    num_plots = len(value_columns)
    fig, axes = plt.subplots(num_plots, 1, figsize=figsize, squeeze=False)

    for i, column in enumerate(value_columns):
        if column not in input_df.columns:
            raise ValueError(f"Value column '{column}' not found in DataFrame.")
        if not pd.api.types.is_numeric_dtype(input_df[column]):
            raise ValueError(f"Column '{column}' must contain numeric data.")

        ts_data = input_df.set_index(date_column).resample(freq)[column].mean()
        axes[i, 0].plot(ts_data)
        axes[i, 0].set_title(column)
        axes[i, 0].set_xlabel("Date")
        axes[i, 0].set_ylabel("Values")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.suptitle(super_title + ' - Frequency: ' + freq, fontsize=super_title_font)

    if output_path:
        plt.savefig(output_path)

    plt.show()

