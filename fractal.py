import numpy as np


def var_index_and_fractal_dim(low, high):
    """Calculates the variation index and fractal dimension of a financial time series.

    Arguments:
    low -- 1-D array like of lowest prices in the bars
    high -- 1-D array like of highest prices in the bars

    Returns:
    dict of
        v_indx -- variation index of the data
        fractal_dim -- fractal dimension of the data
        V_sigma -- variation with interval size sigma
        sigma -- actual interval size, units of sigma is index

    A minimum of 128 datapoints are recommended for best results.
    Implements method outlined in this paper: http://spkurdyumov.narod.ru/Dubovikov1.pdf
    """
    sigma = 2 ** np.arange(3,6)

    left_over = len(low) % (2 ** 5)
    low = low[left_over:]
    high = high[left_over:]

    lows = []
    highs = []

    for i in range(0, 3):
        rows = 2**(i+3)
        cols = len(low)/(2**(i+3))
        lows.append(np.reshape(low, (rows, cols), order='F'))
        highs.append(np.reshape(high, (rows, cols), order='F'))

    V_sigma = np.zeros(3)
    for i in range(0, 3):
        ampMin = np.min(lows[i], axis=0)
        print(ampMin.shape)
        ampMax = np.max(highs[i], axis=0)
        print(ampMax.shape)
        V_sigma[i] = np.sum(ampMax-ampMin)

    p = np.polyfit(np.log((2 ** np.arange(3,6))), np.log(V_sigma), 1)

    v_indx = -p[0]

    fractal_dim = v_indx + 1

    return {'v_indx': v_indx, 'fractal_dim': fractal_dim, 'V_sigma': V_sigma, 'sigma': sigma}
