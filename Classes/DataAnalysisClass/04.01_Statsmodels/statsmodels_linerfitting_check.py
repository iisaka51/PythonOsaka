from scipy.optimize import curve_fit

def f(x, a, b):
    return a * x + b

xdata = data['x']
ydata = data['y']
p0 = [0, 0] # initial parameter estimate
sigma = data['y_err']
popt, pcov = curve_fit(f, xdata, ydata, p0, sigma, absolute_sigma=True)
perr = np.sqrt(np.diag(pcov))
print('a = {0:10.3f} +- {1:10.3f}'.format(popt[0], perr[0]))
print('b = {0:10.3f} +- {1:10.3f}'.format(popt[1], perr[1]))
