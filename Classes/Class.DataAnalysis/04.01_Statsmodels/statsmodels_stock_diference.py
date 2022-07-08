stock_data['Natural Log'] = stock_data['Close'].apply(lambda x: np.log(x))
stock_data['Logged First Difference'] = stock_data['Natural Log'] - \
                                        stock_data['Natural Log'].shift()
