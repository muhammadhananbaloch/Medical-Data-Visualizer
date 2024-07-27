import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
height_in_cm = df['height']
height_in_m = height_in_cm / 100
bmi = df['weight'] / height_in_m ** 2
df['overweight'] = bmi.apply(lambda x: 1 if x > 25 else 0)

# 3 Normalize the data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

# 4
def draw_cat_plot():
    # 5 Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, and overweight in the df_cat variable.
    df_cat = pd.melt(df, id_vars = 'cardio', value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # 6 Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat[['cardio', 'variable', 'value']].value_counts().reset_index(name = 'total')
    

    # 7 Convert the data into long format and create a chart that shows the value counts of the categorical features using the following method provided by the seaborn library import : sns.catplot()
    df_cat['cardio'] = df_cat['cardio'].astype('category')  
    df_cat['variable'] = df_cat['variable'].astype('category')  
    df_cat['value'] = df_cat['value'].astype('category')


    # 8 Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar')


    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11 Clean the data in the df_heat variable by filtering out incorrect data
    df_heat = df
    df_heat = df_heat[(df_heat['ap_lo'] <= df_heat['ap_hi'])
    & (df_heat['height'] >= df_heat['height'].quantile(0.025)) 
    & (df_heat['height'] <= df_heat['height'].quantile(0.975)) 
    & (df_heat['weight'] >= df_heat['weight'].quantile(0.025)) 
    & (df_heat['weight'] <= df_heat['weight'].quantile(0.975))]

    # 12 Calculate the correlation matrix and store it in the corr variable
    corr = df_heat.corr()

    # 13 Generate a mask for the upper triangle and store it in the mask variable
    mask = np.triu(np.ones_like(corr, dtype=bool))



    # 14 Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # 15 Plot the correlation matrix using the method provided by the seaborn library import: sns.heatmap()

    ax = sns.heatmap(corr, mask=mask, center=0, vmax=.1, linewidths=0.5, cbar_kws={"shrink": .5})

    # 16
    fig.savefig('heatmap.png')
    return fig
