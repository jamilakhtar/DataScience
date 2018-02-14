# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 15:57:23 2018

@author: Jamil.Akhtar
"""

#Import pandas
import pandas as pd

# Import pyplot
import matplotlib.pyplot as plt

# Create file path: file_path
editions_file_path = 'datasets\Summer Olympic medalists 1896 to 2008 - EDITIONS.tsv'

# Load DataFrame from file_path: editions
editions_df = pd.read_csv(editions_file_path,sep='\t')

# Extract the relevant columns: editions
editions = editions_df[['Edition', 'Grand Total', 'City', 'Country']]

# Create the file path: file_path
ioc_codes_file_path = 'datasets\Summer Olympic medalists 1896 to 2008 - IOC COUNTRY CODES.csv'

# Load DataFrame from file_path: ioc_codes
ioc_codes_df = pd.read_csv(ioc_codes_file_path)

# Extract the relevant columns: ioc_codes
ioc_codes = ioc_codes_df[['Country', 'NOC']]

# Create empty dictionary: medals_dict
medals_file_path = 'datasets\Summer Olympic medalists 1896 to 2008 - ALL MEDALISTS.tsv'

# Load DataFrame from file_path: editions
medals_df = pd.read_csv(medals_file_path,sep='\t')

medals = medals_df[['Edition','Athlete', 'NOC', 'Medal']]

# Construct the pivot_table: medal_counts
medal_counts = medals.pivot_table(aggfunc='count', index='Edition', values='Athlete', columns='NOC')

# Set Index of editions: totals
totals = editions.set_index('Edition')

# Reassign totals['Grand Total']: totals
totals = totals['Grand Total']

# Divide medal_counts by totals: fractions
fractions = medal_counts.divide(totals, axis='rows')

# Apply the expanding mean: mean_fractions
mean_fractions = fractions.expanding().mean()

# Compute the percentage change: fractions_change
fractions_change = mean_fractions.pct_change() * 100

# Reset the index of fractions_change: fractions_change
fractions_change = fractions_change.reset_index()

hosts = pd.merge(editions, ioc_codes, how='left')

# Extract relevant columns and set index: hosts
hosts = hosts[['Edition', 'NOC']].set_index('Edition')

# Fix missing 'NOC' values of hosts
# print(hosts.loc[hosts.NOC.isnull()])
hosts.loc[1972, 'NOC'] = 'FRG'
hosts.loc[1980, 'NOC'] = 'URS'
hosts.loc[1988, 'NOC'] = 'KOR'

# Reset Index of hosts: hosts
hosts = hosts.reset_index()

# Reshape fractions_change: reshaped
reshaped = pd.melt(fractions_change, id_vars='Edition', value_name='Change')

# Extract rows from reshaped where 'NOC' == 'CHN': chn
chn = reshaped.loc[reshaped.NOC == 'CHN']

# Merge reshaped and hosts: merged
merged = pd.merge(reshaped, hosts, how='inner')

# Set Index of merged and sort it: influence
influence = merged.set_index('Edition').sort_index()

# Extract influence['Change']: change
change = influence['Change']

# Make bar plot of change: ax
ax = change.plot(kind='bar')

# Customize the plot to improve readability
ax.set_ylabel("% Change of Host Country Medal Count")
ax.set_title("Is there a Host Country Advantage?")
ax.set_xticklabels(editions['City'])

# Display the plot
plt.show()