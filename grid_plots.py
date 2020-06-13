import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import sys
import argparse
import get_data

stylesheet = "seaborn-dark"
#stylesheet = "dark_background"
matplotlib.style.use(stylesheet)
if stylesheet == "seaborn-dark":
    contrast = "orange"
else:
    contrast = "gold"

STATES = ['Alabama','Alaska','Arizona','Arkansas','California',
          'Colorado','Connecticut','Delaware','Florida',
          'Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa',
          'Kansas','Kentucky','Louisiana','Maine','Maryland',
          'Massachusetts','Michigan','Minnesota','Mississippi',
          'Missouri','Montana','Nebraska','Nevada','New Hampshire',
          'New Jersey','New Mexico','New York','North Carolina',
          'North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania',
          'Rhode Island','South Carolina','South Dakota','Tennessee',
          'Texas','Utah','Vermont','Virginia','Washington',
          'West Virginia','Wisconsin','Wyoming']

ALL_COUNTRIES = ['Brazil','Costa Rica','El Salvador','Germany','Iran',
                 'Italy','Korea, South','Mexico','Russia','Spain','Sweden','US']

EU_COUNTRIES = ['Austria','Belgium','Bulgaria','Croatia','Cyprus','Czechia',
                'Denmark','Estonia','Finland','France','Germany','Greece',
                'Hungary','Ireland','Italy','Latvia','Lithuania','Luxembourg',
                'Malta','Netherlands','Poland','Portugal','Romania','Slovakia',
                'Slovenia','Spain','Sweden']

LATIN_COUNTRIES = ['Mexico','Guatemala','Belize','El Salvador','Honduras',
                   'Nicaragua','Costa Rica','Panama','Colombia','Venezuela',
                   'Ecuador','Peru','Brazil','Bolivia','Paraguay','Uruguay',
                   'Argentina','Chile','Cuba','Dominican Republic']

def plot_by_state(state, data):

    fig = plt.figure(figsize=(6,4))

    plt.bar(data.index, data[state].diff())
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.gcf().autofmt_xdate(rotation=0, ha='center')

    plt.ylabel('Daily new cases')
    plt.suptitle(state, fontsize='x-large')

    plt.savefig(f'{state}_new_cases.png', bbox_index='tight')

def grid_plot(data, region, outdir="plots", eu_vs_usa=True):
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    if region in ["world", "global", "latin"]:
        subplots = (3, 4)
        figsize = (12, 6)
        lw = 1.25
        labelsize = "small"
        fontsize = "medium"
        if region in ["world", "global"]:
            statenations = ALL_COUNTRIES
            filename = "global_new_cases.pdf"
        else:
            statenations = LATIN_COUNTRIES
            filename = "latin_new_cases.pdf"
    elif region == "usa":
        subplots = (10, 5)
        figsize = (10, 12)
        statenations = STATES
        lw = 0.75
        labelsize = "xx-small"
        fontsize = "small"
        filename = "states_new_cases.pdf"
    elif region == "eu_vs_usa":
        data["EU"] = data.loc[:,EU_COUNTRIES].sum(axis=1)
        subplots = (2, 1)
        figsize = (6, 6)
        lw = 1.5
        labelsize = "small"
        fontsize = "large"
        statenations = ["US", "EU"]
        filename = "EU_vs_USA.pdf"

    fig, axes = plt.subplots(subplots[0], subplots[1],
                             figsize=(figsize[0], figsize[1]),
                             sharex=True)
    plt.subplots_adjust(wspace=0.3)

    dailydata = data.diff()

    for i,ax in enumerate(axes.flatten()):

        ax.bar(dailydata.index, dailydata[statenations[i]])
        ax.plot(dailydata[statenations[i]].rolling(5,
                                              center=True,
                                              min_periods=2).mean(),
                c=contrast, lw=lw)
        ax.set_ylim(bottom=0)
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        plt.gcf().autofmt_xdate(rotation=70)

        ax.tick_params('both', labelsize=labelsize)
        ax.text(0.025, 0.8, statenations[i], fontsize=fontsize, 
                transform=ax.transAxes)

    plt.suptitle(f'New daily cases\n{dailydata.index[-1]:%B %d, %Y}',
                 fontsize='large')
    outfilename = os.path.join(outdir, filename)
    plt.savefig(outfilename, bbox_inches='tight')
    print(f"Saved {outfilename}")

if __name__ == "__main__":
    regions = ["world"]
    #regions = ["world", "usa", "latin", "eu_vs_usa"]
    for item in regions:
        data, pops = get_data.get_data(item)
        grid_plot(data, item)
