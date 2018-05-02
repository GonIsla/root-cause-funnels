import pandas as pd

#Funnel comparison function
#category comparison
# 1)FUNCTIONS
#   1.1.1)Define the comparison functions
#       1.1.1) Non statistical (DONE)
#       1.1.2) Proportions
#       1.1.3) Ordinal
#   1.2)Define the variable change per category functions


def direct_comparison(df, col_variants, unique_identifiers, end_step, start_step=None
                      , start_step_unique=True, end_step_unique=False):
    if start_step:
        if start_step_unique:
            col_start = df[df[start_step]>0].pivot_table(index=col_variants, values=unique_identifiers
                                                         , aggfunc='nunique')[unique_identifiers]
        else:
            col_start = df.pivot_table(index=col_variants, values=start_step, aggfunc='sum')[start_step]
    else:
        col_start = df.pivot_table(index=col_variants, values=unique_identifiers, aggfunc='nunique')[unique_identifiers]
    if end_step_unique:
        col_end = df[df[end_step] > 0].pivot_table(index=col_variants, values=unique_identifiers
                                                     , aggfunc='nunique')[unique_identifiers]
    else:
        col_end = df.pivot_table(index=col_variants, values=end_step, aggfunc='sum')[end_step]

    return [col_start, col_end]


def category_comparison(df, col_variants, unique_identifiers, end_step, category, base_variant
                        , start_step=None, start_step_unique=True, end_step_unique=False):
    """
    cat_values = direct_comparison(df=df, col_variants=[col_variants, category], unique_identifiers=unique_identifiers
                                   , end_step=end_step, start_step=start_step, start_step_unique=start_step_unique
                                   , end_step_unique=end_step_unique)

    all_values = direct_comparison(df=df, col_variants=col_variants, unique_identifiers=unique_identifiers
                                   , end_step=end_step, start_step=start_step, start_step_unique=start_step_unique
                                   , end_step_unique=end_step_unique)
    weight = cat_values[0]/all_values[0]
    all_change = all_values[1]/all_values[0]
    all_change = all_change/all_change[base_variant]
    cat_change = cat_values[1]/cat_values[0]
    cat_change = cat_change/cat_change[base_variant]
    cat_exclusion = pd.DataFrame({'overall':all_change}).join(pd.DataFrame({'per_impact': cat_change * weight}))
    cat_exclusion = (cat_exclusion.overall - cat_exclusion.per_impact) * ((weight * (-1) + 1).pow(-1))

    return cat_exclusion
    """

    all_values = direct_comparison(df=df, col_variants=col_variants, unique_identifiers=unique_identifiers
                                   , end_step=end_step, start_step=start_step, start_step_unique=start_step_unique
                                   , end_step_unique=end_step_unique)

    all_change = all_values[1]/all_values[0]
    all_change = all_change/all_change[base_variant]

    if start_step_unique or end_step_unique:
        cat_values = direct_comparison(df=df, col_variants=[col_variants, category], unique_identifiers=unique_identifiers
                                       , end_step=end_step, start_step=start_step, start_step_unique=start_step_unique
                                       , end_step_unique=end_step_unique)
        cat_start = pd.DataFrame({'overall': all_values[0]}).join(pd.DataFrame({'cat_val': cat_values[0]}))
        cat_start = cat_start['overall'] - cat_start['cat_val']

        cat_end = pd.DataFrame({'overall': all_values[1]}).join(pd.DataFrame({'cat_val': cat_values[1]}))
        cat_end = cat_end['overall'] - cat_end['cat_val']

        cat_change = cat_end/cat_start

        return [cat_change/cat_change[base_variant], cat_values[0], all_change, all_values[0]]
    else:
        pass