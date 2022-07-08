from scipy.optimize import minimize

def chi2(pars):
    """Cost function.
    """
    y_model = pars[0] * data['x'] + pars[1]
    chi = (data['y'] - y_model) / data['y_err']
    return np.sum(chi ** 2)

result = minimize(fun=chi2, x0=[0, 0])
popt = result.x
print('a = {0:10.3f}'.format(popt[0]))
print('b = {0:10.3f}'.format(popt[1]))
