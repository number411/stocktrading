'''
Created on Jan 7, 2017

@author: I043544
'''
from pandas.tests.test_algos import TestGroupVarFloat64
from numpy.ma.core import count
from scipy.stats.morestats import Variance
from talib.func import STDDEV

if __name__ == '__main__':
    #!/usr/bin/env python
    import matplotlib.pyplot as plt
    from datetime import datetime as dt
    import numpy as np
    from matplotlib.dates import DateFormatter, WeekdayLocator,\
        DayLocator, MONDAY, num2date, date2num
    from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
    import talib
    import matplotlib.mlab as mlab
       
    
    # (Year, month, day) tuples suffice as args for quotes_historical_yahoo
    date1 = (2007, 1, 1)
#     date1 = (2015,12,1)
    date2 = (2009, 12, 31)
    
    
    mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
    alldays = DayLocator()              # minor ticks on the days
    weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
    dayFormatter = DateFormatter('%d')      # e.g., 12
#    AAMC AAN AAP AAT AAU AAV AB ABB

    quotes = quotes_historical_yahoo_ohlc('APD', date1, date2)
    if len(quotes) == 0:
        raise SystemExit
    
#     fig, ax = plt.subplots(2,1)
#     fig.subplots_adjust(bottom=0.2)
#     plt.subplot(111)
    fig = plt.figure()
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
 


    d = []
    #candlestick_ohlc(ax1, quotes, width=0.6)
    xdate   = np.array([ d[0] for d in quotes ])
    yhigh   = np.array([ d[2] for d in quotes  ])
    ylow    = np.array([ d[3] for d in quotes  ])
    yclose  = np.array([ d[4] for d in quotes  ])

    yhighc = yhigh[1:]/yhigh[0:-1]
    
    #From Backtest_01 program
    ylowc = ylow[1:]/ylow[0:-1]
    
    #Calculating everyday returns
    yclosec = yclose[1:]/yclose[0:-1]
    #ax1.set_autoscaley_on(False)
    #ax1.set_ylim(0.6,1.4)
    adxdata = np.array(talib.ADX(yhigh,ylow,yclose,14))

#     pvar = (yclose-sma13)*4/abs(sma13-sma50)  
#     varst = STDDEV(yclosec,5)
#     print "Number of times crosses two is %d" % (pvar==2).sum()
    left, width = 0.1, 0.8
    rect1 = [left, 0.25, width, 0.65]    
    axescolor = '#f6f6f6'
    ax1 = fig.add_axes(rect1, axisbg=axescolor)  # left, bottom, width, height    
    n, bins, patches = ax1.hist(yclosec,20,color='y')
    i = 0
    for px in patches :
        #px.set_label(n[i])
        ax1.text(bins[i],0,str(n[i]),fontsize=24)
        i = i + 1 
   
    rect2 = [left, 0.05, width, 0.2]
    ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)   
    ax1.autoscale_view()
    bincenters = 0.5*(bins[1:]+bins[:-1])
    # add a 'best fit' line for the normal PDF
    y = mlab.normpdf(bincenters, np.average(yclosec), np.std(yclosec))
    l = ax1.plot(bincenters, y, 'r--', linewidth=1)
    plt.setp(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')
    avereturns = str(round((np.average(yclosec)-1)*100,2))
    sdreturns = str (round( np.std    (yclosec)*100,2))
    ax1.set_title('Average ' + avereturns + '%  StdDev ' + sdreturns + '%')
    ax1.text(1.10,60,'Number of positive returns : ' + str((yclosec > 1).sum()) + ' out of '+ str(int (yclosec.sum())),fontsize =18)
    ax2.xaxis_date()
    ax2.autoscale_view()
    #plt.setp(ax2.get_xticklabels(), rotation=45, horizontalalignment='right')
    #ax2.plot(xdate,adxdata,'b-')
    ax2.set_autoscaley_on(False)
    ax2.set_ylim(-10,+10)    
    #ax2.plot(xdate,pvar,'bo')
    
    plt.show()    
#     ax.xaxis.set_major_locator(mondays)
#     ax.xaxis.set_minor_locator(alldays)
#     ax.xaxis.set_major_formatter(weekFormatter)
#     ax.xaxis.set_minor_formatter(dayFormatter)
    
#     plot_day_summary(ax, quotes, ticksize=3)    
#     sma50 = talib.SMA(yclose,50)
#     sma13 = talib.SMA(yclose,13)  
#     ax3 = ax1.twinx()
#     ax3.set_ylim(min(varst),max(varst))
#     ax3.plot(xdate[1:],varst,'r-')
    
#     ax1.plot(xdate,sma13)
    
#     for i in range(10,len(yhighc)-10) :
#             ylast10h = yhighc[i-10:i]
#             ylast10l = ylowc[i-10:i]
#             if adxdata[i] > 25 :
#                 if (ylast10h >= 1).sum() > 6 and (ylast10l >= 1).sum() > 4 and yclosec[i-1] > 1 and yclosec[i-2] > 1:
#                     ax1.plot(xdate[i],yclose[i],'b^',markersize=12)
#                     #plt.text(xdate[i],yclose[i],yclosec[i]) 
#                 if (ylast10h <= 1).sum() > 6 and (ylast10l <= 1).sum() > 4  and yclosec[i-1] < 1 and yclosec[i-2] < 1:
#                     #if xdate[i] >= date2num(dt.strptime("040210","%y%m%d")) :
#                     #    print 'a'
#                     ax1.plot(xdate[i],yclose[i],'co',markersize=12)  
#                     #plt.text(xdate[i],yclose[i],str(yclosec[i-1])+str('p')+str(yclosec[i-2]))          
            
    #plt.plot(xdate[:],yclose[:],'g')    
    
    #End Backtest_01 program
    #plt.plot(xdate[10],10,'ro')
#     ax1.plot(xdate,yclose,'b-')
#     ax1.xaxis_date()
#     ynoccur = np.empty(1200)
#     ynoccur = np.bincount((yclosec[:]*100))