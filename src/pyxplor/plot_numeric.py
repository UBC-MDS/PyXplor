import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import math

def plot_numeric(
        input_df: pd.DataFrame,
        list_of_variables: list,
        plot_kind: str,
        label_y_offset: int = 10,
        label_fontsize: int = 10,
        figsize: tuple = (8, 10),
        output: bool = False,
        super_title: str = "Distribution of Numeric Variables",
        super_title_font: int = 14) -> tuple:
    """Plot the distribution of numeric variables in a DataFrame, save the plot, and display it.

    This function will construct a set of subplots for each of the numeric variables specified
    in `list_of_variables`. The function will save as well as display the entire figure.

    Parameters
    ----------
    input_df : pd.DataFrame
        The DataFrame that contains the numeric variables.

    list_of_variables : list
        List of numeric variables (column names) to be plotted.

    plot_kind : {'hist', 'kde', 'hist+kde'}
        Type of plot to be generated:
        'hist': Histogram only.
        'kde': Kernel density estimate plot only.
        'hist+kde': Histogram with a kernel density estimate plot showing median and mean.

    label_y_offset : int, optional
        Y-axis offset for label positioning. Default is 10.

    label_fontsize : int, optional
        Font size for axis labels. Default is 10.

    figsize : tuple[int, int], optional
        The width and height of the figure size in a tuple. Default is (8, 10)

    output : bool, optional
        Whether to output the figure to the current working directory. Default is False.

    super_title : str, optional
        Super title for the entire plot. Default is "Distribution of Numeric Variables".

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
    numeric = ["numeric_var1", "numeric_var2"]
    plot_numeric(df, numeric, "hist+kde")
    """
    # Validate input_df
    if not isinstance(input_df, pd.DataFrame):
        raise ValueError("input_df must be a pandas DataFrame.")

    # Validate list_of_variables
    if not all(var in input_df.columns for var in list_of_variables):
        missing_vars = [var for var in list_of_variables if var not in input_df.columns]
        raise ValueError(f"The following variables are not present in the DataFrame: {', '.join(missing_vars)}.")
    
    if len(list_of_variables) == 0:
        raise ValueError("list_of_variables cannot be an empty list.")

    # Validate plot_kind
    valid_plot_kinds = {'hist', 'kde', 'hist+kde'}
    if plot_kind not in valid_plot_kinds:
        raise ValueError("Invalid value for 'plot_kind'. It should be either 'hist', 'kde', or 'hist+kde'.")

    # Validate label_y_offset and label_fontsize
    if not all(isinstance(val, (int, float)) for val in [label_y_offset, label_fontsize]):
        raise ValueError("label_y_offset and label_fontsize must be numbers (integers or floats).")

    # Validate figsize
    if not (isinstance(figsize, tuple) and len(figsize) == 2 and
            all(isinstance(val, (int, float)) for val in figsize)):
        raise ValueError("figsize must be a tuple of exactly two numbers (integers or floats).")

    # Validate output
    if not isinstance(output, bool):
        raise ValueError("Output must be a boolean value.")

    # Validate super_title_font
    if not isinstance(super_title_font, (int, float)):
        raise ValueError("super_title_font must be a number (integer or float).")

    # Get numeric columns from the dataframe
    numeric_columns = input_df.select_dtypes(include=['number']).columns.tolist()

    # Filter numeric columns based on the provided list_of_variables
    numeric_columns = [var for var in list_of_variables if var in numeric_columns]

    # Check if there are any numeric columns to plot
    if not numeric_columns:
        raise ValueError("No valid numeric columns found in the provided list_of_variables.")

    # Calculate the number of rows and columns dynamically
    total_plots = len(numeric_columns)
    rows = math.ceil(math.sqrt(total_plots))
    cols = math.ceil(total_plots / rows)

    # Create subplots in a grid
    fig, ax = plt.subplots(rows, cols, figsize=figsize)
    if len(list_of_variables) > 1:
        ax = ax.flatten()


    # Loop through numeric columns and plot
    for i, variable in enumerate(numeric_columns):
        # Plot histogram or kernel density estimate plot for each variable
        if plot_kind == 'hist':
            sns.histplot(x=variable, data=input_df, ax=ax[i], bins=20)
        elif plot_kind == 'kde':
            sns.kdeplot(x=variable, data=input_df, ax=ax[i])
        elif plot_kind == 'hist+kde':
            sns.histplot(x=variable, data=input_df, ax=ax[i], bins=20, kde=True)

            # Add central tendency labels with different colors
            mean = input_df[variable].mean()
            median = input_df[variable].median()
            mean_label = f'Mean: {mean:.2e} units'
            median_label = f'Median: {median:.2e} units'
            ax[i].axvline(mean, color='orange', linestyle='dashed', linewidth=2, label=mean_label)
            ax[i].axvline(median, color='red', linestyle='dashed', linewidth=2, label=median_label)

            # Add legend outside the subplots
            ax[i].legend(loc='upper right', bbox_to_anchor=(1.1, 1.05))

        ax[i].set_title(variable)  # Set subplot title

    # Add super title
    fig.suptitle(super_title, fontsize=super_title_font)

    # Adjust layout and save the figure
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust rect to make space for super title
    
    if output:
        plt.savefig("numeric_variables.png")

    return fig, ax
