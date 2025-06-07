import matplotlib.pyplot as plt
import seaborn as sns

def analyze_three_columns(dataset0, dataset1, categorical, categorical2, continuous):
    print("Without difficulties:")
    print(dataset0.groupby(by=[categorical, categorical2])[continuous].describe().head())
    print("\n\n\n")
    print("With difficulties:")
    print(dataset1.groupby(by=[categorical, categorical2])[continuous].describe().head())
    print("\n\n\n")

    lower_bound0, upper_bound0 = get_outlier_bounds(dataset0, continuous)
    lower_bound1, upper_bound1 = get_outlier_bounds(dataset1, continuous)

    custom_bi_boxplot(dataset0, dataset1, categorical, continuous, upper_bound0, upper_bound1, categorical2)

def custom_draw_boxplot(df, categorical, continuous, max_continuous, title, hue_column, subplot_position):
    """
    Малює блок-діаграму для заданого DataFrame, категоріальної та неперервної змінної.
    """
    plt.subplot(1, 2, subplot_position)
    plt.title(title)
    red_diamond = dict(markerfacecolor='r', marker='D')
    sns.boxplot(x=categorical,
                y=df[df[continuous] < max_continuous][continuous],
                data=df,
                flierprops=red_diamond,
                order=sorted(df[categorical].unique(), reverse=True),
                hue=hue_column, hue_order=sorted(df[hue_column].unique(), reverse=True))
    plt.ticklabel_format(style='plain', axis='y')
    plt.xticks(rotation=90)

def custom_bi_boxplot(df0, df1, categorical, continuous, max_continuous1, max_continuous0, hue_column):
    """
    Створює паралельні блок-діаграми для двох груп, визначених у наборі даних, на основі
    категоріальної та неперервної змінної, виділяючи відмінності за допомогою відтінків.
    """
    plt.figure(figsize=(16, 10))

    # Графік для першо групи "Труднощі з платежами" (Payment Difficulties)
    custom_draw_boxplot(df1, categorical, continuous, max_continuous1, 'Payment Difficulties', hue_column, 1)

    # Графік для другої групи "Вчасні оплати" (On-Time Payments)
    custom_draw_boxplot(df0, categorical, continuous, max_continuous0, 'On-Time Payments', hue_column, 2)

    plt.tight_layout(pad=4)
    plt.show()

def analyze_column(dataset, column):
    print(f"{dataset[column].describe()}\n")
    print(f"meadian: {dataset[column].median()}\n")
    print(f"mode: {dataset[column].mode()}")

    lower_bound_col, upper_bound_col = get_outlier_bounds(dataset, column)
    outliers = dataset[(dataset[column] < lower_bound_col) | (
            dataset[column] > upper_bound_col)][column].values


    print(f"Outliers amount: {len(outliers)}")
    print("Outliers:", outliers)

    plt.figure(figsize=(8, 6))
    sns.boxplot(x=dataset[column])
    plt.title('Boxplot for column')
    plt.xlabel('column')
    plt.show()

def analyze_correlation(dataset, column1, column2, title):
    lower_bound_col1, upper_bound_col1 = get_outlier_bounds(dataset, column1)
    lower_bound_col2, upper_bound_col2 = get_outlier_bounds(dataset, column2)

    total_rows = len(dataset)

    outliers_col1 = dataset[(dataset[column1] < lower_bound_col1) | (dataset[column1] > upper_bound_col1)]
    percentage_outliers_col1 = (len(outliers_col1) / total_rows) * 100

    outliers_col2 = dataset[(dataset[column2] < lower_bound_col2) | (dataset[column2] > upper_bound_col2)]
    percentage_outliers_col2 = (len(outliers_col2) / total_rows) * 100

    print(f"{title}")
    print(f"{'-' * 50}")

    print(f"Outlier bounds for '{column1}':")
    print(f"  Lower Bound: {lower_bound_col1}")
    print(f"  Upper Bound: {upper_bound_col1}")
    print(f"  Outliers:")
    print(f"  Percentage of outliers: {percentage_outliers_col1:.2f}%\n")

    print(f"Outlier bounds for '{column2}':")
    print(f"  Lower Bound: {lower_bound_col2}")
    print(f"  Upper Bound: {upper_bound_col2}")
    print(f"  Outliers:")
    print(f"  Percentage of outliers: {percentage_outliers_col2:.2f}%\n")

    analyze_pearson_correlation(dataset, column1, column2)

    plot_scatter_comparison(dataset, column1, column2, upper_bound_col1, upper_bound_col2, title)

def get_outlier_bounds(dataset, column):
    q1 = dataset[column].quantile(0.25)
    q3 = dataset[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return lower_bound, upper_bound

def kde_with_no_outliers(df0, df1, column, title_for_0_dataset, title_for_1_dataset):
    lower_bound_col_0, upper_bound_col_0 = get_outlier_bounds(df0, column)
    lower_bound_col_1, upper_bound_col_1 = get_outlier_bounds(df1, column)

    plt.figure(figsize=(14, 6))

    # Filter df1 (Payment difficulties)
    filtered_df1 = df1[(df1[column] >= lower_bound_col_1) & (df1[column] <= upper_bound_col_1)]
    sns.kdeplot(filtered_df1[column], label=title_for_1_dataset)

    # Filter df0 (On-Time Payments)
    filtered_df0 = df0[(df0[column] >= lower_bound_col_0) & (df0[column] <= upper_bound_col_0)]
    sns.kdeplot(filtered_df0[column], label=title_for_0_dataset)

    plt.ticklabel_format(style='plain', axis='x')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

def analyze_pearson_correlation(dataset, column1, column2):
        correlation = dataset[column1].corr(dataset[column2], method='pearson')

        if correlation == 1:
            conclusion = "Perfect positive correlation (+1)"
        elif correlation == -1:
            conclusion = "Perfect negative correlation (-1)"
        elif correlation > 0.7:
            conclusion = "Strong positive correlation"
        elif correlation > 0.3:
            conclusion = "Moderate positive correlation"
        elif correlation > 0:
            conclusion = "Weak positive correlation"
        elif correlation < -0.7:
            conclusion = "Strong negative correlation"
        elif correlation < -0.3:
            conclusion = "Moderate negative correlation"
        elif correlation < 0:
            conclusion = "Weak negative correlation"
        else:
            conclusion = "No correlation"

        print(f"Pearson Correlation between '{column1}' and '{column2}': {correlation:.4f}")
        print(f"Conclusion: {conclusion}")

def plot_scatter_comparison(dataset,
                            x_column, y_column,
                            outlier_upper_bound_x, outlier_upper_bound_y,
                            title1):

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.title(title1)
    sns.scatterplot(
        x=dataset[dataset[x_column] < outlier_upper_bound_x][x_column],
        y=dataset[dataset[y_column] < outlier_upper_bound_y][y_column],
        data=dataset
    )
    plt.ticklabel_format(style='plain', axis='x')
    plt.ticklabel_format(style='plain', axis='y')

    plt.tight_layout(pad=4)
    plt.show()

