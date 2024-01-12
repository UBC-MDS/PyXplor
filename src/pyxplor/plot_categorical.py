import pandas as pd

def plot_categorical(
        input_df: pd.DataFrame,
        list_of_variables: list,
        figsize: tuple = (10, 6),
        label_y_offset: int=0,
        label_fontsize: int=10,
        output_path: str = None,
        super_title: str = "Distribution of Categorical Variables",
        super_title_font: int = 14) -> None:
    """Plot the distribution of the categorical variables in a DataFrame, save the plot, and display it.

    This function will construct a set of subplots (all bar plots)
    for each of the categorical variables specified in `list_of_variables`. The function will
    save as well as display the entire figure. 

    Parameters
    ----------
    input_df : pd.DataFrame
        The DataFrame that contains the categorical variables.

    list_of_variables : list
        List of categorical variables (column names) to be plotted.

    orientation : {'v', 'h'}
        Orientation of the plots, either vertical or horizontal. Default is is horizontal.

    fig_width : int
        Width of the figure. Default is 10.

    fig_height : int
        Height of the figure. Default is 6.

    label_y_offset : int
        Y-axis offset for label positioning. Default is 0.

    label_fontsize : int
        Font size for axis labels. Default is 10.

    output_path : str, optional
        Path to save the plot. Path to save the plot. Defaults to None, which means the plot will not be saved.
        
    super_title : str, optional
        Super title for the entire plot. Default is "Distribution of Categorical Variables".

    super_title_font : int, optional
        Font size for the super title. Default is 14.

    Returns
    -------
    None
        

    Examples
    --------
    categorical = ["cat_var1", "cat_var2", "cat_var3]
    plot_categorical(df, categorical, "h", 30, 10, 10, 10, "sample.png")
    """

    pass # Implementation to be added