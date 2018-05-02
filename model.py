import pandas
import matplotlib.pyplot as plt
import statsmodels.api as sm


def analyze(data, time, predict_start, predict_end, disp=False):
    d = pandas.Series(data)
    d.index = pandas.Index(sm.tsa.datetools.dates_from_str(time))
    d = d.asfreq('H', method='pad')
    mod = sm.tsa.statespace.SARIMAX(d, trend='n', order=(0, 1, 0), seasonal_order=(1, 1, 1, 24),
                                    enforce_stationarity=False).fit(disp=disp)
    predict = mod.predict(predict_start, predict_end, dynamic=True)
    if disp:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax = d.plot(ax=ax)
        predict.plot(ax=ax)
        fig.show()
    return predict
