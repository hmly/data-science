import community
import networkx as nx
import numpy as np
import pandas as pd

# Read the csv files
df = pd.read_csv("cache/sr28asc/NUT_DATA.txt", delimiter="^", index_col=["NDB_No", "Nutr_No"],
                 names=["NDB_No", "Nutr_No", "Nutr_Val"],
                 usecols=["NDB_No", "Nutr_No", "Nutr_Val"], quotechar="~")

df2 = pd.read_csv("cache/sr28asc/NUTR_DEF.txt", delimiter="^", index_col="Nutr_No",
                  names=["Nutr_No", "Units", "Tagname", "NutrDesc", "Num_Dec", "SR_Order"],
                  usecols=["Nutr_No", "NutrDesc"], quotechar="~")

# Simplify nutrient level and find corr
df[df > 0] = 1
corr = df.unstack().corr()
corr -= np.eye(len(corr))
edges = [(col[0][1], pair[0][1]) for col in corr.items()
         for pair in col[1].items() if np.abs(pair[1]) > 0.5]
edges = pd.DataFrame(edges, columns=["from", "to"])
edges.to_csv("results/edges.csv")

# Construct network
labels = df2.to_dict()["NutrDesc"]
G = nx.from_pandas_dataframe(edges, "from", "to")
G = nx.relabel_nodes(G, labels)
nx.write_graphml(G, "results/nutr-corr.graphml")

# Compute modularity
partition = community.best_partition(G)
print("Modularity: ", community.modularity(partition, G))

# Display communities
word_clusters = pd.DataFrame({"part_id": pd.Series(partition)})
for x in word_clusters.groupby("part_id"):
    print("--", " | ".join(x[1].index))
