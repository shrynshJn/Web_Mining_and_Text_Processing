import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('titanic.csv')
x = data.iloc[:, 1:2].values
y = data.iloc[:, 2].values

from sklearn.ensemble import RandomForestRegressor
regressor = RanomdForesrRegressor(n_estimators = 100, random_state = 0)

regressor.fit(x, y)
y_pred = regressor.predict(10)

X_grid = np.arange(min(x), max(x), 0.01)
X_grid = X_grid.reshape((len(X_grid), 1))
plt.scatter(x, y, color='blue')
plt.plot(X_grid, regressor.predict(X_grid), color = 'green')
plt.title('Random Forest Regression')
plt.xlabel('Position level')
plt.ylabel('Salary')
plt.show()
