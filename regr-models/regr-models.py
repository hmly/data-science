import pandas as pd
import sklearn.linear_model as lm
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pylab as plt
import numpy as np
import numpy.random as rnd

# Read data file, eliminate missing values
df = pd.read_csv("cache/data-subset.tsv", sep="\t", na_values="-")
df = df.dropna()

# Create histograms of age of M and F
male = df[df["Gender"] == "M"]
female = df[df["Gender"] == "F"]
age_m = np.array(male["Age"])
age_f = np.array(female["Age"])

plt.figure()
plt.hist(age_m, facecolor="blue")
plt.hist(age_f, facecolor="red", alpha=0.75)

plt.grid()
plt.title("Male-Female Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.savefig("results/mf-age.png")

# Create scatter plot of generosity v. age
generosity_m = np.array(male["OGrade"] - male["IGrade"])
generosity_f = np.array(female["OGrade"] - female["IGrade"])
# disp_m = rnd.random(len(generosity_m))
# disp_f = rnd.random(len(generosity_f))
disp_m = generosity_m + np.random.normal(0, 0.1, len(generosity_m))
disp_f = generosity_f + np.random.normal(0, 0.1, len(generosity_f))
plt.figure()
plt.scatter(age_m, generosity_m + disp_m, color="blue", alpha=0.5, label="male")
plt.scatter(age_f, generosity_f + disp_f, color="red", alpha=0.5, label="female")

plt.grid()
plt.title("Age v. Generosity Level")
plt.legend(loc="lower right")
plt.xlabel("Age")
plt.ylabel("Generosity Level")
plt.savefig("results/age-generosity.png")

# Produce regression models
d = {"M": 0, "F": 1}
df["Gender"] = df["Gender"].map(d)
selection = rnd.binomial(1, 0.7, size=len(df)).astype(bool)
training = df[selection]
testing = df[~selection]

# First model - training
olm = lm.LinearRegression()
X = training[["Gender", "Age", "IGrade"]]
y = training["OGrade"]
olm.fit(X, y)

# Testing
X = testing[["Gender", "Age", "IGrade"]]
y = testing["OGrade"]
model1 = np.array([np.round(x) for x in olm.predict(X)])
print(olm.score(X, y))

# Second model - training
igrade_range = 6
dum_ograde = pd.get_dummies(training["OGrade"])
dum_igrade = pd.get_dummies(training["IGrade"])
clfs = [lm.LogisticRegression(C=10.0) for _ in range(igrade_range)]
X = pd.merge(training[["Gender", "Age"]], dum_igrade, left_index=True, right_index=True)
y = dum_ograde
for i in range(igrade_range):
    clfs[i].fit(X, y[i+1])

# Testing
dum_ograde = pd.get_dummies(testing["OGrade"])
dum_igrade = pd.get_dummies(testing["IGrade"])
X = pd.merge(testing[["Gender", "Age"]], dum_igrade, left_index=True, right_index=True)
y = dum_ograde
ograde2 = []
for i in range(igrade_range):
    testing[i] = clfs[i].predict(X)

for x in np.array(testing[[0, 1, 2, 3, 4, 5]]):
    if x.sum() == 1:
        ograde2.append(list(x).index(1) + 1)
    else:
        ograde2.append(0)
print(set(ograde2))

