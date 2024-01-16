import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns

def plot_binary(
        input_df: pd.DataFrame,
        list_of_variables: list,
        plot_kind: str,
        label_offset: int,
        label_fontsize: int,
        plot_orientation: str = "h",
        figsize: tuple = (10, 6),
        output: bool = False,
        super_title: str = "Distribution of Binary Variables",
        super_title_font: int = 14) -> None:
    """Plot the distribution of binary variables in a DataFrame, save the plot, and display it.

    This function will construct a set of subplots (either a bar plot or a pie chart)
    for each of the binary variables specified in `list_of_variables`. The function will
    save as well as display the entire figure. 

    Parameters
    ----------
    input_df : pd.DataFrame
        The DataFrame that contains the binary variables.

    list_of_variables : list
        List of binary variables (column names) to be plotted.

    plot_kind : {'count', 'pie'}
        Type of plot to be generated, a count plot or a pie chart.

    label_offset : int
        Offset for label positioning.
        X-axis offset if orientation is horizontal.
        Y-axis offset if orientation is vertical.

    label_fontsize : int
        Font size for axis labels.

    plot_orientation: {'h', 'v'}, optional
        The orientation of countplot, which can be either horizontal or vertical.

    figsize: tuple[int, int], optional
        The width and height of the figure size in a tuple.

    output : bool, optional
        Whether to output the figure to the current working directory.

    super_title : str, optional
        Super title for the entire plot. Default is "Distribution of Binary Variables".

    super_title_font : int, optional
        Font size for the super title. Default is 14.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib Figure object.
    ax : matplotlib.axes._subplots.AxesSubplot
        The matplotlib Axes object.
        
    Examples
    --------
    binary = ["binary_var1", "binary_var2"]
    fig, ax = plot_binary(df, binary, "count", 1, 1, "h", (10, 10), True)
    """

    # Check input_df is a dataframe
    if not isinstance(input_df, pd.DataFrame):
        raise ValueError("input_df must be a pandas DataFrame.")

    # Check if list_of_variables are all in the dataframe
    missing_variables = [var for var in list_of_variables if var not in input_df.columns]
    if missing_variables:
        raise ValueError(f"The following variables are not present in the DataFrame: {', '.join(missing_variables)}.")

    # Check if list_of variables are all binary
    for var in list_of_variables:
        unique_values = input_df[var].unique()
        if len(unique_values) != 2 or set(unique_values) - {0, 1}:
            raise ValueError(f"Variable '{var}' is not binary.")

    # Check plot_kind is either 'count' or 'pie'
    valid_plot_kinds = {'count', 'pie'}
    if plot_kind not in valid_plot_kinds:
        raise ValueError("Invalid value for 'plot_kind'. It should be either 'count' or 'pie'.")

    # Check if label_offset is a number
    if not (isinstance(label_offset, (int, float))):
        raise ValueError("label_offset must be a number (integers or floats).")

    # Check if label_fontsize is a number
    if not (isinstance(label_fontsize, (int, float))):
        raise ValueError("label_fontsize must be a number (integers or floats).")

    # Check if plot_orientation is either 'h' or 'v'
    valid_plot_orientations = {'h', 'v'}
    if plot_orientation not in valid_plot_orientations:
        raise ValueError("Invalid value for 'plot_orientation'. It should be either 'h' or 'v'.")   

    # Check figsize is a tuple of 2 numbers
    if not (isinstance(figsize, tuple) and len(figsize) == 2 and
            isinstance(figsize[0], (int, float)) and isinstance(figsize[1], (int, float))):
        raise ValueError("figsize must be a tuple of exactly two numbers (integers or floats).")
            
    # Check whether output is a boolean value
    if not isinstance(output, bool):
        raise ValueError("Output must be a boolean value.")

    # Check whether super_title is a string
    if not isinstance(super_title, str):
        raise ValueError("super_title must be a string.")

    # Check whether super_title_font is a number
    if not isinstance(super_title_font, (int, float)):
        raise ValueError("super_title_font must be a number (integer or float).")

            
    # Calculate dimension of subplot
    total_plots = len(list_of_variables)
    rows = math.ceil(math.sqrt(total_plots))
    cols = math.ceil(total_plots / rows)

    # Instantiate fig and ax
    fig, ax = plt.subplots(rows, cols, figsize=figsize)
    ax = ax.flatten()

    # Plot the variables
    for i, variable in enumerate(list_of_variables):

        # Countplot
        if plot_kind == "count":
            
            # Horizontal Orientation
            if plot_orientation == "h":
                sns.countplot(ax=ax[i], y=variable, data=input_df)

                # Add horizontal labels
                for p in ax[i].patches:
                    ax[i].annotate(
                        int(p.get_width()),
                        (p.get_width(), p.get_y() + p.get_height() / 2.),
                        ha = 'center',
                        va = 'center',
                        xytext = (label_offset, 0),
                        textcoords = 'offset points',
                        fontsize = label_fontsize
                    )
            
            # Vertical Orientation
            else:
                sns.countplot(ax=ax[i], x=variable, data=input_df)

                # Add vertical labels
                for p in ax[i].patches:
                    ax[i].annotate(
                        int(p.get_height()),
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha = 'center',
                        va = 'center',
                        xytext = (0, label_offset),
                        textcoords = 'offset points',
                        fontsize = label_fontsize
                    )

            # Add subplot titles
            ax[i].set_title('Distribution of {}'.format(variable))
            

        # Pie charts
        else:

            # Calculate pie labels and sizes
            binary_variable_counts = input_df[variable].value_counts()
            labels = binary_variable_counts.index
            sizes = binary_variable_counts.values

            # Calculate percentages
            percentages = sizes / sum(sizes) * 100

            # Format the label to include both percentage and count
            label_fmt = '{}\n{:.1f}%\n({:d})'
            labels_with_count = [label_fmt.format(labels, percentage, count) for labels, percentage, count in zip(labels, percentages, sizes)]

            ax[i].pie(sizes, labels=labels_with_count, autopct='', startangle=90)  # autopct='' to suppress default percentage labels
            ax[i].set_title('Distribution of {}'.format(variable))

            # remove subplot bounding box
            plt.axis('off')

    # Supertitle
    fig.suptitle(super_title, fontweight="bold", fontsize=super_title_font)

    plt.tight_layout()

    # Save figure into current working directory if output is True
    if output:
        plt.savefig("binary_variables.png")

    plt.show()

    return fig, ax