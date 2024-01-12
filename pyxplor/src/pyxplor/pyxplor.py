import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math

def numeric_explorer(data, fig_width=15, fig_height=10, output_path="numeric_explorer.png"):
    """
    Analyze and plot key statistical insights for numeric data.

    Parameters
    ----------
    data : pandas.DataFrame
        The input dataframe containing numeric data.

    fig_width : int, optional
        Width of the entire figure in inches. Default is 15.

    fig_height : int, optional
        Height of the entire figure in inches. Default is 10.

    output_path : str, optional
        Filepath to save the generated visualization. Default is "numeric_explorer.png".

    Returns
    -------
    None
        The function saves the visualization to the specified output_path.

    Examples
    --------
    >>> numeric_explorer(df, fig_width=15, fig_height=10, output_path="numeric_explorer.png")
    """

    # Get numerical columns from the dataframe
    numerical_columns = data.select_dtypes(include=['number']).columns.tolist()

    # Calculate the number of rows and columns for subplots
    total_plots = len(numerical_columns)
    rows = math.ceil(math.sqrt(total_plots))
    cols = math.ceil(total_plots / rows)

    # Create subplots in a grid
    fig, ax = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
    ax = ax.flatten()

    # Loop through numerical columns and plot
    for i, variable in enumerate(numerical_columns):
        # Plot histogram for each variable with density curve
        sns.histplot(x=variable, data=data, ax=ax[i], kde=True, bins=20)
        ax[i].set_title(variable)  # Set subplot title

        # Add central tendency labels
        mean = data[variable].mean()
        median = data[variable].median()
        ax[i].axvline(mean, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean:.2f}')
        ax[i].axvline(median, color='green', linestyle='dashed', linewidth=2, label=f'Median: {median:.2f}')

        # Identify and mark outliers (values outside 1.5 * IQR)
        q1 = data[variable].quantile(0.25)
        q3 = data[variable].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = data[(data[variable] < lower_bound) | (data[variable] > upper_bound)]
        ax[i].scatter(outliers[variable], [0] * len(outliers), color='orange', marker='x', label='Outliers')

        # Add legend
        ax[i].legend()

    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig(output_path)
    plt.show()

# Example usage:
numeric_explorer(df, fig_width=15, fig_height=10, output_path="numeric_explorer.png")