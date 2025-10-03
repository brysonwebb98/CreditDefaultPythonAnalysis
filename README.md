# Overview

The goal of this project is for me to strengthen my skills as a software engineer by building a real-world data analysis example. I worked with a public dataset from LendingClub to explore loan default risks and how to extract meaningful insights using code and data visualization.

The dataset that I used contains information about loan applications such as credit history, income, delinquencies, and the loan purpose. I obtained this from Kaggle. (Loan Data: https://www.kaggle.com/datasets/itssuru/loan-data/data)

My purpose in analyzing this data is to practice presenting results in a way that I could explain to investors or stakeholders. I chose this data because I work for a financial institution and see these things from the borrowers on a daily basis. This analysis shows which types of borrowers are more risky and which are less risky. 

[Software Demo Video](https://youtu.be/RwJFT3hKOz8)

# Data Analysis Results

**Questions and Findings:**

1. **How do FICO Scores impact default rates?**  
Borrowers with **Fair and Poor FICO scores** show the highest risk of default. Very Good and Excellent scores are the safest.  

2. **How does income impact default rates?**  
Borrowers earning **below $25K** default most often. Interestingly, defaults also increase for borrowers earning **above $125K**, likely due to higher revolving balances (more debt carried).  

3. **How do large outstanding credit balances impact default rates?**  
Higher revolving credit balances are strongly correlated with increased default rates.  

4. **How do past delinquencies affect default rates?**  
Default rates rise steadily with the number of delinquencies. Even one delinquency significantly increases risk.  

5. **How do delinquencies and public records together affect default rates?**  
Borrowers with **both delinquencies and public records (bankruptcy, tax liens, judgments)** are at the highest risk of default.  

6. **Which loan types are most likely to default?**  
**Small business and educational loans** show the highest default rates, while credit card and major purchase show lower default rates.  

# Development Environment

Tools Used
- Jupyter Notebook

Programming Language
- Python 3

Libraries Used
- pandas (used to create the dataframes and do groupby functions)
- numpy for numerical calculations
- matplotlib for visualizations
- Ipython.display was used for markdown formatting

# Useful Websites

* [Kaggle Dataset](https://www.kaggle.com/datasets/itssuru/loan-data/data)  
* [Pandas Documentation](https://pandas.pydata.org/docs/)
* [Matplotlib Documentation](https://matplotlib.org/stable/index.html)
* [Stack Overflow](https://stackoverflow.com/)

# Future Work

* Make sure my game plan when starting the code is more concrete, actionable, and measurable. Without this it would be hard to align what time I am working on wher. 
* Taking my time and really thinking through errors. Reading my errors on stackoverflow so I can understand what is happening and get better.
* Review the full dataset prior to starting any assignment. You should know everything that is within the data to see what will be useful to you and what you might not use. 


