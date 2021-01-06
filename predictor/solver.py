import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

maxRange = 2
maxSteps = 30


def getmax(data):
    ret = 0
    for i in data:
        if(i>ret):
            ret=i
    return ret


def solve(data):
    p = d = q = range(0, maxRange)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 14) for x in list(itertools.product(p, d, q))]

    warnings.filterwarnings("ignore")  # specify to ignore warning messages
    maxaic = 1000

    nsparam = None
    sparam = None

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(data,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()
                # print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                if (maxaic > results.aic):
                    maxaic = results.aic
                    nsparam = param
                    sparam = param_seasonal
            except Exception as fault:
                # print(fault)
                continue

    print('final params are param {} X {} with AIC = {}'.format(sparam, nsparam, maxaic))

    mod = sm.tsa.statespace.SARIMAX(data,
                                    order=nsparam,
                                    seasonal_order=sparam,
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

    results = mod.fit()

    print(results.summary().tables[1])

    # results.plot_diagnostics(figsize=(15, 12))
    # plt.show()

    # Get forecast 500 steps ahead in future
    pred_uc = results.get_forecast(steps=maxSteps)

    # Get confidence intervals of forecasts
    pred_ci = pred_uc.conf_int()

    print(pred_uc.predicted_mean)

    retval = 0

    dumdict = {}

    for i in range(0,len(data)):
        dumdict[i] = data[i]

    ax = dumdict.plot(label='observed', figsize=(20, 15))

    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('storage')

    plt.legend()
    plt.show()

    return getmax(pred_uc.predicted_mean)