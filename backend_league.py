import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests

from selenium.webdriver import Chrome
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import json

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix

df = pd.read_csv("df.csv")
df_champ = pd.read_csv("df_champ.csv")

#modify time
df["time"] = df["time"].apply(lambda x: int(x[:2]))

#modify game_result
result_map = {"Victory": 1, "Defeat": 0}

df["game_result"] = df["game_result"].map(result_map)

#modify kill participation
df["kill_p."] = df["kill_p."].apply(lambda x: int(x[:2]))

# new column consist of winrates that are until corresponding index (game count)
static_var = len(df["game_result"])

def winrate(elem):
    global static_var

    average = df["game_result"].tail(static_var).mean()
    static_var -= 1
    return average


df["winrate"] = df["game_result"].apply(winrate)

df["kill"] = df["kda"].apply(lambda x: int(x.split('/')[0]))
df["death"] = df["kda"].apply(lambda x: int(x.split('/')[1]))
df["assist"] = df["kda"].apply(lambda x: int(x.split('/')[2]))
df["k-a"] = df["kill"] + df["assist"]
df["kda_ratio"] = df["k-a"] / df["death"]

conditions = [(df["kda_ratio"] >= 4), (df["kda_ratio"] < 4)]
labels = ["high", "low"]
df["kda_ratio_category"] = np.select(conditions, labels)
df["kda_ratio_category"] = df["kda_ratio_category"].apply(lambda x: 1 if x == "high" else 0)
df["vis/cs_score"] = df["vis/cs_score"].apply(lambda x: int(x.split(" ")[0]))

# first plot
played_reversed = df_champ["Played"][::-1]
champ_reversed = df_champ["Champion"][::-1]

plt.figure(figsize=(15, 6))

plt.bar(champ_reversed, played_reversed, color="purple")

plt.xlabel('Champions')
plt.ylabel('Games Played')
plt.title('Games Played Per Champion')

plt.xticks(rotation=90)
plt.ylim(0, max(df_champ['Played']))

plt.savefig('champ_plot', bbox_inches='tight')
#plt.show()

# winrate plot
winrate_reversed = df["winrate"].values[::-1]

plt.figure(figsize=(10, 6))

sns.set(style="whitegrid")

sns.scatterplot(x=df["winrate"].index, y=winrate_reversed, hue=winrate_reversed > 0.5, data=df,
                palette={True: 'green', False: 'red'}, marker='s', s=150)

plt.plot(df["winrate"].index, winrate_reversed, linestyle='-', color='gray', linewidth=2)

plt.ylim(0, 1)

plt.xlabel('Time (Game Count)')
plt.ylabel('Winrate')
plt.title('Winrate over time')

plt.legend(['> 0.5', "< 0.5"], loc='upper right')

plt.savefig("winrate_plot", bbox_inches='tight')
#plt.show()

# champion performance chart
with open("charts", "r") as json_file:
    data = json.load(json_file)

data.pop(6)
data.pop(6)

# ML PART

df.replace([np.inf, -np.inf], 0, inplace=True)

df_ml = df.drop("kda", axis=1)

X = df_ml.drop("game_result", axis=1)
y = df_ml["game_result"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_report_result = classification_report(y_test, y_pred, output_dict=True)

#print("Accuracy:", accuracy)
#print("Classification Report:\n", classification_report_result),

# Feature Importance Graph
plt.clf()

features = df_ml.columns
importances = model.feature_importances_
indices = np.argsort(importances)

plt.title("Feature Importances")
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel("Relative Importance")
#plt.show()

plt.savefig('feature_importances', bbox_inches='tight')

# confusion matrix
cm = confusion_matrix(y_test, y_pred)

plt.clf()

plt.figure(figsize=(12, 6))

sns.heatmap(cm, annot=True)

plt.xlabel("Predicted")
plt.ylabel("Truth")

plt.savefig("confusion_matrix", bbox_inches="tight")
