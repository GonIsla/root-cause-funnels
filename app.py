import pandas as pd
import numpy as np
import comparison_functions as cf


# 2)APP PER SE
#   2.1)Load data
input_file = 'C:\\Users\\OLX - Gonzalo\\Desktop\\Python & posgress\\AutoLookforInsight\\dummy_dataset.txt'
df = pd.read_csv(input_file, sep='\t')

# 2.2)Loop through all
funnel = ['step1', 'step2', 'step3', 'step4']
funnel_unq = [True, False, False, False]
uniq_id = ['id']
col_variant = ['Variant']
base_variant = 1
categories = ['cat1', 'cat2', 'cat3']
# 2.2.1)overall variable & funnel
overall_change = [cf.step_aggregation(df, col_variants=col_variant[0], unique_identifiers=uniq_id[0]
                                      , step=funnel[ind], step_unique=funnel_unq[ind]) for ind in [0, -1]]

overall_change = overall_change[1]/overall_change[0]
overall_change = overall_change/overall_change[base_variant]

step_by_step_chg = pd.DataFrame()
for i in range(len(funnel)-1):

    step_values = [cf.step_aggregation(df, col_variants=col_variant[0], unique_identifiers=uniq_id[0]
                                       , step=funnel[ind], step_unique=funnel_unq[ind]) for ind in [i, i+1]]

    step_values = step_values[1] / step_values[0]
    step_values = step_values / step_values[base_variant]
    if i == 0:
        step_by_step_chg = pd.DataFrame({funnel[i + 1]: step_values})
    else:
        step_by_step_chg = step_by_step_chg.join(pd.DataFrame({funnel[i+1]: step_values}))

#       Cause criteria is: if we eliminate the effect of the drop off in...
#       ...that step would the overall effect change direction?
excluding_step_chg = step_by_step_chg.divide(overall_change, axis=0).pow(-1)
step_is_cause = (np.sign(excluding_step_chg - 1)).subtract(np.sign(overall_change - 1), axis=0)

# 2.2.2)Main variable & categorical
print([cf.step_without_cat(df, col_variants=col_variant[0], unique_identifiers=uniq_id[0], category=categories[0]
                                       , step=funnel[ind], step_unique=funnel_unq[ind]) for ind in [0, -1]])
# 2.2.3)Top funnel & categorical

# 2.3)Consolidate results

# 2.4)Build explanation







