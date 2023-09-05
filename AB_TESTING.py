#####################################################
# Bidding-Methods-with-AB-Test-Comparison-of-Conversion
#####################################################


#####################################################
# TASKS
#####################################################


#####################################################
# Task 1: Preparing and Analyzing Data
#####################################################

import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

dataframe_control = pd.read_excel("ab_testing.xlsx" , sheet_name="Control Group")
dataframe_test = pd.read_excel("ab_testing.xlsx" , sheet_name="Test Group")

df_control = dataframe_control.copy()
df_test = dataframe_test.copy()

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df_control)
check_df(df_test)

df_control["group"] = "control"
df_test["group"] = "test"

df = pd.concat([df_control,df_test], axis=0,ignore_index=False)
df.head()


#####################################################
# Task 2: Defining the Hypothesis of A/B Testing
#####################################################

# H0 : M1 = M2 (There is no difference between the purchasing averages of the control group and the test group.)
# H1 : M1!= M2 (There is a difference between the purchasing averages of the control group and the test group.)

df.groupby("group").agg({"Purchase": "mean"})


#####################################################
# TASK 3: Performing Hypothesis Testing
#####################################################

# Normality Assumption :
# H0: Normal distribution assumption is provided.
# H1: Normal distribution assumption not provided.
# p < 0.05 H0 RED
# p > 0.05 H0 CANNOT BE REJECTED

test_stat, pvalue = shapiro(df.loc[df["group"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.5891
# HO cannot be rejected. The values ​​of the control group provide the assumption of normal distribution.


# Variance Homogeneity :
# H0: Variances are homogeneous.
# H1: Variances are not homogeneous.
# p < 0.05 H0 RED
# p > 0.05 H0 CANNOT BE REJECTED

test_stat, pvalue = levene(df.loc[df["group"] == "control", "Purchase"],
                           df.loc[df["group"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value=0.1083
# HO cannot be rejected. The values ​​of the Control and Test groups provide the assumption of variance homogeneity.
# Variances are Homogeneous.


# Since the assumptions are provided, an independent two-sample t-test (parametric test) is performed.
# H0: M1 = M2 (There is no statistically significant difference between the purchasing averages of the control group and test group.)
# H1: M1 != M2 (There is a statistically significant difference between the purchasing averages of the control group and the test group.)
# p<0.05 HO RED , p>0.05 HO CANNOT BE REJECTED

test_stat, pvalue = ttest_ind(df.loc[df["group"] == "control", "Purchase"],
                              df.loc[df["group"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value=0.3493
# HO cannot be rejected. There is no statistically significant difference between the purchasing averages of the control and test groups.


