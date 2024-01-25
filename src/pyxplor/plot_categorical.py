import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns

def plot_categorical(
        input_df: pd.DataFrame,
        list_of_variables: list,
        label_fontsize: int = 10,
        figsize: tuple = (10, 6),
        output: bool = False,
        super_title: str = "Distribution of Categorical Variables",
        super_title_fontsize: int = 14,
        padding: float=0.5) -> None:
    """Plot the distribution of the categorical variables in a DataFrame, save the plot, and display it.

    This function will construct a set of subplots (all horizontal bar plots)
    for each of the categorical variables specified in `list_of_variables` (with 20 or less unqiue values). 
    The function will display the entire figure (with option to save figure). 

    Parameters
    ----------
    input_df : pd.DataFrame
        The DataFrame that contains the categorical variables.

    list_of_variables : list
        List of categorical variables (column names) to be plotted

    label_fontsize : int, optional
        Font size for axis labels. Default is 10.

    figsize : tuple[width: int, height: int], optional
        The width and height of the figure size in a tuple. Default is (10, 6).

    output : bool, optional
        Whether to output the figure to the current working directory. Default is False.
        
    super_title : str, optional
        Super title for the entire plot. Default is "Distribution of Categorical Variables".

    super_title_fontsize : int, optional
        Font size for the super title. Default is 14.

    padding : float, optional
        The height of the padding between subplots, as a fraction of the average Axes height. Default is (0.5).

    Returns
    -------
    fig : matplotlib.figure.Figure
        The matplotlib Figure object.
        
    ax : matplotlib.axes._subplots.AxesSubplot
        The matplotlib Axes object.

    Examples
    --------
    categorical = ["cat_var1", "cat_var2", "cat_var3"]
    fig, ax = plot_categorical(df, categorical)
    """
    # Check if input is a dataframe
    if not isinstance(input_df, pd.DataFrame):
        raise ValueError("input_df must be a pandas DataFrame.")
    
    # Check if list_of_variables is empty
    if len(list_of_variables) == 0:
        raise ValueError("list_of_variables cannot be an empty list.")
    
    # Check if list_of_variables are in dataframe
    missing_variables = [var for var in list_of_variables if var not in input_df.columns]
    if missing_variables:
        raise ValueError(f"The following variables are not present in the DataFrame: {', '.join(missing_variables)}.")

    # Check if list_of_variables is categorical with 20 or less unique values
    selected_cols = [col for col in list_of_variables if input_df[col].nunique() <= 20]
    if selected_cols != list_of_variables:
        print("Only displaying plots for categorical variables with 20 or less unique values.")
        dropped_list = [col for col in list_of_variables if col not in selected_cols]
        print(f"Dropping the following variables for plotting: {', '.join(dropped_list)}")
        list_of_variables = selected_cols
    
    # Check if label_fontsize is a number
    if not (isinstance(label_fontsize, (int, float))):
        raise ValueError("label_fontsize must be a number (integers or floats).")
    
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
    if not isinstance(super_title_fontsize, (int, float)):
        raise ValueError("super_title_fontsize must be a number (integer or float).")

    # Calculate dimensions of figure (number of rows and columns of sublots)
    total_plots = len(list_of_variables)
    rows = math.ceil(math.sqrt(total_plots))
    cols = math.ceil(total_plots / rows)

    # Create Figure object and Axes array
    fig, ax = plt.subplots(rows, cols, figsize=figsize)

    # Case when multiple subplots to be created
    if len(list_of_variables) > 1:
        # Flatten Axes array if more than one variable provided for plotting
        ax = ax.flatten()

        # Iterate through plotting categorical variables
        for i, var in enumerate(list_of_variables):  

            # Create Bar Plot sublpot for each element in list_of_variables
            sns.countplot(ax=ax[i], y=var, hue=var, legend=False, data=input_df)

            # Add subplot title
            ax[i].set_title(var)

    else: # Just one variable provided in list_of_variables

        #Create Bar Plot for single subplot
        sns.countplot(ax=ax, y=list_of_variables[0], hue=list_of_variables[0], legend=False, data=input_df)

        # Add subplot title for single subplot
        ax.set_title(list_of_variables[0])

    # Add overall Figure title 
    fig.suptitle(super_title, fontweight="bold", fontsize=super_title_fontsize)

    # Configure subplot spacing
    plt.subplots_adjust(hspace=padding)

    # Save figure into current working directory if output is True
    if output:
        plt.savefig("categorical_variables.png")

    return fig, ax