import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import sys

matplotlib.style.use('dark_background')

def get_population_data(info_df):
    filename = "../COVID-19/csse_covid_19_data/UID_ISO_FIPS_LookUp_Table.csv"
    pop_df = pd.read_csv(filename)

    #join_us_pop_df = pop_df.join(info_df, on='Population', how='left', rsuffix="repeat")
    cols_to_use = pop_df.columns.difference(info_df.columns)
    join_us_pop_df = pd.merge(info_df, pop_df[cols_to_use], left_index=True, right_index=True, how='outer')

    return join_us_pop_df.set_index('UID')

def getdata():

    filename = '../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    a = pd.read_csv(filename)
    #a.drop(columns=['iso2','iso3','code3','Admin2','Country_Region','Lat','Long_','Combined_Key'],inplace=True)

    us_df = get_population_data(a)

    # Getting the rate of positive tests per day per state
    test_df = us_df.groupby('Province_State').sum()
    test_df.drop(columns=['code3', 'FIPS', 'Lat', 'Long_', 'Population'], inplace=True)

    dt_index = pd.to_datetime(test_df.columns)
    statesdata = test_df.T
    statesdata = statesdata.reindex(dt_index)

    # Getting the population per state
    #population_series = us_df.groupby('Province_State').sum()['Population']
    statepops = pd.read_csv('nst-est2019-01.csv',index_col='State')

    return statesdata, statepops


def state_plot(state,data):

    fig = plt.figure(figsize=(6,4))

    plt.bar(data.index,data[state].diff())
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    plt.gcf().autofmt_xdate(rotation=0,ha='center')

    plt.ylabel('Daily new cases')
    plt.suptitle(state,fontsize='x-large')

    plt.savefig(f'{state}_new_cases.png',bbox_index='tight')


def grid_plot(data, pops):

    fig,axes = plt.subplots(10,5,figsize=(10,12),sharex=True)
    plt.subplots_adjust(wspace=0.3)

    stateslist = ['Alabama','Alaska','Arizona','Arkansas','California',
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

    for key in data.keys():
        try:
            data[key] = (data[key]/pops['Population'][key]) * 100
        except KeyError:
            continue

    dailydata = data.diff()

    for i,ax in enumerate(axes.flatten()):

        ax.bar(dailydata.index, dailydata[stateslist[i]])
        ax.plot(dailydata[stateslist[i]].rolling(5, center=True, min_periods=2).mean(),
                c='gold',lw=0.75)
        #ax.set_ylim(bottom=0)
        ax.set_ylim(0, 0.05)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        plt.gcf().autofmt_xdate(rotation=70)

        ax.tick_params('both',labelsize='xx-small')
        ax.text(0.025,0.8,stateslist[i],fontsize='small',transform=ax.transAxes)


    plt.suptitle(f'New daily cases\n{dailydata.index[-1]:%B %d, %Y}',fontsize='large')
    plt.savefig(f'states_new_cases.pdf',bbox_inches='tight')


if __name__ == "__main__":

    data,pops = getdata()

    grid_plot(data, pops)

    #state_plot()
