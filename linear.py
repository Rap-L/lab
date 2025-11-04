import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
dt_iris = pd.read_csv("/workspaces/lab/iris.csv") 
X = dt_iris.iloc[:,0:1]
Y = dt_iris.iloc[:,1:2]
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.33) 
lmodel=LinearRegression()
lmodel.fit(X_train,Y_train)
prediction = lmodel.predict(X_test) 
intercept=lmodel.intercept_ 
slop=lmodel.coef_
print("R square value = " + str(lmodel.score(X_test,Y_test)))


import matplotlib.pyplot as plt 
plt.scatter(X,Y,alpha=0.8) #s=50, 
plt.plot(X,intercept+slop*X,'r-') 
plt.show()

