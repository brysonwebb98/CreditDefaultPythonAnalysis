# %%
from IPython.display import Markdown as md, display
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

COLS = ["Credit Policy","Purpose of Loan","Interest Rate","Installment","Annual Income (raw)",
"Debt to Income","FICO Score","Days with Credit","Revolving Balances","Revolving Limits",
"Inquiries (Last 6 Months)","Delinquent (Last 24 months)",
"Public Records (Bankruptcy, tax liens or judgements)","Not Fully Paid"]

# BINS AND LABELS FOR WHAT WE ARE LOOKING TO ANALYZE
FICO_BINS   = [300, 580, 670, 740, 800, 900]  
FICO_LABELS = ["Poor","Fair","Good","Very Good","Excellent"]

INCOME_BINS   = [0, 25000, 50000, 75000, 100000, 125000, 500000]
INCOME_LABELS = ["0-25K","25-50K","50-75K","75-100K","100-125K","125K+"]

DTI_BINS = [0, 20, 30, 40, 50, 60, float("inf")]
DTI_LABELS = ["0-20", "20-30", "30-40", "40-50", "50-60", "60+"]

BALANCE_BINS   = [0, 5_000, 10_000, 20_000, 40_000, float("inf")]
BALANCE_LABELS = ["0-5K", "5K-10K", "10K-20K", "20K-40K", "40K+"]

# ORIGINAL DATAFRAME
df = pd.read_csv("loan_data.csv")
df.columns = COLS

# ADDING ANNUAL INCOME AS DOLLAR AMOUNTS
df["Annual Income"] = np.exp(df["Annual Income (raw)"]).round(0)

# DF W/FICO BINS
df["FICO Tier"] = pd.cut(df["FICO Score"], bins=FICO_BINS, labels=FICO_LABELS, right=True, ordered=True)

# DF W/INCOME BINS
df["Income Tier"] = pd.cut(df["Annual Income"], bins=INCOME_BINS, labels=INCOME_LABELS, right=True, ordered=True)

# DF W/DTI BINS
df["DTI Tier"] = pd.cut(df["Debt to Income"], bins=DTI_BINS, labels=DTI_LABELS, right=True, ordered=True)

# DF W/CC BALANCE BINS
df["Credit Balance Tier"] = pd.cut(df["Revolving Balances"], bins=BALANCE_BINS, labels=BALANCE_LABELS, right=True, ordered=True)

display(md("""
# Loan Default Risk Analysis  

This notebook uses LendingClub loan data (2007-2010) to explore factors related to default risk.  
We group borrowers into categories (FICO score, income, delinquencies) and calculate the average default rate within each.  
Charts are used to highlight patterns that may help investors understand which types of borrowers and loans carry higher risk.  
Below is a preview of the dataset, showing the first 10 rows and the key columns used in our analysis. 
"""))
display(df.head(10))
display(md("---"))
display(md("""
# **QUESTIONS**

1. How do FICO Scores impact default rates?

2. How does income impact default rates?

3. How do large credit balances impact default rates?

4. How do past delinquencies affect default rates?

5. How do delinquencies and public records together affect default rates?

6. Which loan type has the highest delinquency?       
"""))
display(md("---"))

# 1. FICO CHART TO DEFAULT RATE
display(md(
"""## 1. How do FICO scores impact default rates?  

We grouped the applications by their **FICO Tier**. From there we were looking at the average amount that paid the loan back.

We can see from the chart that the lower the FICO score the higher the chance of default on their loans."""))

summary_fico = df.groupby("FICO Tier", observed=False)["Not Fully Paid"].mean().mul(100).round(1).reset_index(name="Default Rate %")

plt.bar(summary_fico["FICO Tier"], summary_fico["Default Rate %"])
plt.title("Default Loans Compared to Applicants FICO")
plt.xlabel("FICO Tiers")
plt.ylabel("% of Loans Not Paid")
plt.show()

# 1. SUMMARY()
display(md("""
### Summary: As we can see the people who have **Fair** credit are more likely to default on their loans. Higher the FICO means less risk.
"""))

display(md("---"))

# 2. INCOME CHART TO DEFAULT RATE
display(md("""
## 2. How does income impact default rates?
We grouped the applications by their **Income Tier** and calculated the average loan repayment rate for each group.
"""))

summary_income = df.groupby("Income Tier", observed=False)["Not Fully Paid"].mean().mul(100).round(1).reset_index(name="Default Rate %") 

plt.bar(summary_income["Income Tier"], summary_income["Default Rate %"])
plt.title("Default Loans Compared to Applicants Income")
plt.xlabel("Income Tiers")
plt.ylabel("% of Loans Not Paid")
plt.show()

# 2.2
display(md("## Number of applicants in each income tier."))
display(df["Income Tier"].value_counts())

# 2. SUMMARY()
display(md("""
### Summary Part 1: The chart shows that applicants earning below $25K are the most likely to default, followed by those with incomes above $125K. This is interesting because you would think those who earn more money would be last. 
"""))

summary_income_to_balances = df.groupby("Income Tier", observed=False)["Revolving Balances"].mean().round(0).reset_index(name="Average Revolving Balances")

plt.bar(summary_income_to_balances["Income Tier"], summary_income_to_balances["Average Revolving Balances"])
plt.title("Average Credit Card Balances to Income")
plt.xlabel("Income Tiers")
plt.ylabel("Average Credit Card Balances")
plt.show()

# 2.2 SUMMARY()
display(md("""
### Summary Part 2: While reviewing I thought it would be interesting to see why those with higher income would be defaulting on their loans. 
### The first question that came to my mind what do these people have that those with lower FICO's don't. We can see above that they have a lot more debt.
### I believe this is why they come in second place on defaulting because they are assuming too much debt. 
"""))

display(md("---"))

# 3 LARGE OUTSTANDING CREDIT BALANCES TO DEFAULT RATES
display(md("""
## 3. How do large outstanding credit balances impact default rates?  
We grouped applicants by their **Credit Balance Tier** and compared the average default rates within each category.  
"""))

summary_revolving_balances = df.groupby("Credit Balance Tier", observed=False)["Not Fully Paid"].mean().mul(100).round(1).reset_index(name="Default Rate %")

plt.bar(summary_revolving_balances["Credit Balance Tier"], summary_revolving_balances["Default Rate %"])
plt.title("Default Loans Compared to Applicants Outstanding Credit Balances")
plt.xlabel("Credit Balance Tiers")
plt.ylabel("% of Loans Not Paid")
plt.show()

# 3. Summary()
display(md("""
### Summary: The chart illustrates how higher revolving credit balances correlate with an increased likelihood of default.
"""))

display(md("---"))

display(md("""
## 4. How do past delinquencies affect default rates?  
We grouped applicants by the **number of delinquencies in the last 24 months** and calculated the average default rate for each group.  
"""))

summary_del = df.groupby("Delinquent (Last 24 months)", observed=False)["Not Fully Paid"].mean().mul(100).round(1).reset_index(name="Default Rate %")

plt.bar(summary_del["Delinquent (Last 24 months)"], summary_del["Default Rate %"])
plt.title("Default Loans Compared to Applicants Delinquencies In The Last 24 Months.")
plt.xlabel("Delinquency Count (last 24 months)")
plt.ylabel("% of Loans Not Paid")
plt.show()

display(df["Delinquent (Last 24 months)"].value_counts().sort_index().reset_index())

# 4. Summary()
display(md("""
### Summary: The chart shows that default rates increase steadily with the number of past delinquencies. This dataset didn't have enough data on those who have more than 4 delinquencies however if there was more people in these categories I believe it would continue to increase. 
"""))

display(md("---"))

display(md("""
## 5. How do delinquencies *and* public records together affect default rates?  
We grouped applicants by two factors:  
- **Delinquency count** 
- **Public records** 
"""))

summary_del_pub = df.groupby(["Delinquent (Last 24 months)", "Public Records (Bankruptcy, tax liens or judgements)"], observed=False)["Not Fully Paid"].mean().mul(100).round(1).reset_index(name="Default Rate %")

pivot = summary_del_pub.pivot(
    index="Delinquent (Last 24 months)",
    columns="Public Records (Bankruptcy, tax liens or judgements)",
    values="Default Rate %"
)

pivot.plot(kind="bar", figsize=(10,6))
plt.title("Default Rate by Delinquencies and Public Records")
plt.xlabel("Delinquency Count (last 24 months)")
plt.ylabel("% of Loans Not Paid")
plt.legend(title="Public Record")
plt.show()

# 5. Summary()
display(md("""
### Summary: By comparing default rates across these combined groups, we can see how the presence of both delinquencies and public records amplifies default risk.  
###The results are visualized with a grouped bar chart for easy comparison.  
""")) 

display(md("---"))

display(md("# 6.Which loan type has the highest delinquency?"))

summary_loan_type = df.groupby("Purpose of Loan")["Not Fully Paid"].mean().mul(100).round(1).reset_index(name="Default Rate %")
summary_loan_type = summary_loan_type.sort_values("Default Rate %", ascending=False)

plt.bar(summary_loan_type["Purpose of Loan"], summary_loan_type["Default Rate %"])
plt.title("Which Types of Loans Are More Likely To Default?")
plt.xlabel("Purpose of Loan / Loan Type")
plt.xticks(rotation=45, ha="right")
plt.ylabel("% of Loans Not Paid")
plt.show()

# 6. Summary()
display(md("""
### Summary: From this chart we can see the highest risk loan would be small businesses first and move its way from the left to the right. 
### The type of loan can play a huge role on if you are going to get paid back or not. 
"""))

display(md("---"))
display(md("""
# Conclusion: Who Carries the Highest and Lowest Risk?  

Based on the data and analysis of the LendingClub data several borrower and loan characteristics consistently stand out as predictors of default risk:

**Highest Risk Borrowers**
- People with Fair or Poor FICO scores. These groups had the highest default percentages. 
- Individuals with 1+ delinquencies in the last 24 months, the risk is especially high when combined with a public record. 
- Borrowers who earn under 25K.
- Applicants who are earning over 125K. This is surprising, however, when we review their revolving balances it explains why they might default. 

**Lowest Risk Borrowers**  
- People with Very Good or Excellent FICO scores.
- Borrowers with no public records or delinquencies.
- People who are in the middle range on income and have lower revolving balances. 
- Applicants taking out loans for major purchases or credit cards.

**Overall Insight**
Default risk isn’t explained by one factor alone. Instead, it is a mix of credit history, income, and debt load that provides the best picture of the borrowers risk.

Thank you. 
"""))
display(md("---"))
# %%