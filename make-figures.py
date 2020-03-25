#!/usr/bin/env python

"""
Adapted from @boogheta

by @dbrisaro
"""

import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
from pandas.plotting import table

warnings.filterwarnings('ignore')
typ = 'Confirmed'

file = os.path.join("data", "time_series_19-covid-%s.csv" % typ)

df = pd.read_csv(file)

df = df.drop(['Province/State','Lat','Long'], axis=1)
df = df.T

new_header = df.iloc[0]
df = df[1:]
df.columns = new_header
df.index = pd.to_datetime(df.index)
df.index.names = ['Date']

# I select the countries that I want to look at
new_df = df[['Italy', 'Argentina', 'Spain', 'Brazil']]
new_df['China'] = df['China'].sum(axis=1)
new_df['USA'] = df['US'].sum(axis=1)
new_df['Australia'] = df['Australia'].sum(axis=1)

# For the normalization of the cases, I use the amount of cases every 100.000 inhabitants
# TODO download a .csv with the data of the population of every contunry, must be something like that isnt it?

pob = np.array([[60.48, 44.27, 46.66, 209.3, 1386, 327.2, 24.6]])*1e6
poblacion = pd.DataFrame(pob, index=['Population'], columns=new_df.columns)
new_df_normalized = 1e5*new_df/poblacion.values


# plotting, the size is A4 page, I believe!
# labels and titles in spanish

plt.close('all')

figure = plt.figure(figsize=(8,11))

ax = plt.axes([0.075, 0.35, 0.4, 0.2])
new_df.plot(ax=ax, fontsize=6, lw=0.5, marker='.', markersize=1, alpha=.5)
ax.set_xlabel('Fecha', fontsize=6)
ax.set_ylabel('Casos Confirmados', fontsize=6)
ax.set_ylim([0,90000])
ax.legend(fontsize=6, loc='upper left')

bx = plt.axes([0.58, 0.35, 0.4, 0.2])
new_df.plot(ax=bx, logy=True, fontsize=6, lw=0.5, marker='.', markersize=1, alpha=.5)
bx.set_xlabel('Fecha', fontsize=6)
bx.set_ylabel('Casos Confirmados', fontsize=6)
bx.legend(fontsize=6, loc='upper left')

cx = plt.axes([0.075, 0.05, 0.4, 0.2])
new_df_normalized.plot(ax=cx, fontsize=6, lw=0.5, marker='.', markersize=1, alpha=.5)
cx.set_xlabel('Fecha', fontsize=6)
cx.set_ylabel('Casos Confirmados / 100.000 habitantes', fontsize=6)
cx.set_ylim([0,150])
cx.legend(fontsize=6, loc='upper left')

new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2',]

dx = plt.axes([0.58, 0.05, 0.4, 0.2])
new_df.iloc[-1,:].plot.barh(ax=dx, alpha=0.5, fontsize=6, lw=0.5, color=new_colors)
dx.set_xlim([0,90000])
dx.set_xlabel('Casos Confirmados totales', fontsize=6)
dx.set_ylabel('Paises', fontsize=6)

ex = plt.axes([0.175, 0.7, 0.8, 0.2])
ex.axis('off')
ex.axis('tight')
table = table(ax=ex, data=new_df.iloc[-10::,:].astype('int'), fontsize=6, loc="upper center")
table.set_fontsize(7)
table.scale(1, 1.5)

# fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
fecha = datetime.datetime.now().strftime('%Y-%m-%d')

path = '/home/nico/Documents/covid-update/figures/'
figure.savefig(path + 'figura_' + fecha, dpi=400, bbox_inches='tight')
figure.savefig(path + 'figura_' + fecha + '.pdf', bbox_inches='tight')
