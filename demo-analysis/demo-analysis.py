import matplotlib.pylab as plt
import matplotlib.patches as mpatch
import numpy as np
import pandas as pd

# Get alcohol consumption level and GSP
YEAR = 2009
df = pd.read_csv("cache/niaaa-report.csv")
df = df[df.Year == YEAR]
df2 = pd.read_csv("cache/usgs_state_2009.csv", dtype={"Gross State Product": np.float64},
                  skiprows=5, nrows=52, thousands=",")
df3 = df.merge(df2, on='State', how='left')

# Compute measures per capita
df3["GSP per capita"] = df3["Gross State Product"].div(df3["Population (million)"])
df3["Alcohol"] = df3["Beer"] + df3["Wine"] + df3["Spirits"]

# Construct cross-table
gsp = df3["GSP per capita"] > df3["GSP per capita"].mean()
alcohol = df3["Alcohol"] > df3["Alcohol"].mean()
table = pd.crosstab(gsp, alcohol)
print(table)

# Compute correlation between ALCOHOL CONSUMPTION/capita and GSP/capita
df4 = pd.DataFrame({"GSP": df3["GSP per capita"], "Alcohol": df3["Alcohol"]})
print("\ncorr: ", df4.corr().GSP[0])

# Generate scatter plot, each alcohol is plotted separately
plt.scatter(df3["Beer"], df3["GSP per capita"], color="Blue")
plt.scatter(df3["Spirits"], df3["GSP per capita"], color="Green")
plt.scatter(df3["Wine"], df3["GSP per capita"], color="Red")

red = mpatch.Patch(color='red', label='Wine')
blue = mpatch.Patch(color='blue', label='Beer')
green = mpatch.Patch(color='green', label='Spirits')

plt.legend(handles=[red, green, blue], loc="upper left")

plt.title("GSP/Capita vs Alcohol Consumption/Capita")
plt.xlabel("Alcohol Consumption/Capita")
plt.ylabel("GSP/Capita")
plt.grid()
plt.savefig("results/gsp-alcohol.png")
