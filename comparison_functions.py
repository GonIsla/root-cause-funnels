import pandas as pd

#Funnel comparison function
#category comparison
# 1)FUNCTIONS
#   1.1.1)Define the comparison functions
#       1.1.1) Non statistical (DONE)
#       1.1.2) Proportions
#       1.1.3) Ordinal
#   1.2)Define the variable change per category functions


def step_aggregation(df, col_variants, unique_identifiers, step, step_unique=True):
    if step_unique:
        col_agg = df[df[step] > 0].pivot_table(index=col_variants, values=unique_identifiers
                                               , aggfunc='nunique')[unique_identifiers]
    else:
        col_agg= df.pivot_table(index=col_variants, values=step, aggfunc='sum')[step]

    return col_agg


def step_without_cat(df, col_variants, category, unique_identifiers, step, step_unique):
    # this is a most efficient workaround to count unique of the category without the values
    # leveraging the "vector" way of pandas/numpy
    if step_unique:
        df_subset = df[df[step] > 0].loc[:, [unique_identifiers, col_variants, category]]
        uniq_x_cat = df_subset.pivot_table(index=[unique_identifiers, col_variants], columns=category
                                          , values=unique_identifiers, aggfunc='nunique').fillna(0)
        uniq_x_cat[uniq_x_cat.sum(axis=1) != 1] = 0 #identify the rows that are uniques in all categories

        uniq_x_cat = pd.DataFrame({'uniq_cat': uniq_x_cat.stack()})
        uniq_x_cat.reset_index(level=[col_variants, category], inplace=True)
        cat_agg = uniq_x_cat.pivot_table(index=[col_variants, category], values='uniq_cat', aggfunc='sum')['uniq_cat']
    else:
        cat_agg = step_aggregation(df=df, col_variants=[col_variants, category], unique_identifiers=unique_identifiers
                                   , step=step, step_unique=step_unique)

    all_values = step_aggregation(df=df, col_variants=col_variants, unique_identifiers=unique_identifiers
                                  , step=step, step_unique=step_unique)
    df_without_cat = pd.DataFrame({'overall': all_values}).join(pd.DataFrame({'cat_agg': cat_agg}))

    return df_without_cat['overall'] - df_without_cat['cat_agg']
