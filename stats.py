import pandas as pd
import json
import seaborn
import matplotlib.pyplot as plt

pd.set_option('display.expand_frame_repr', False)

data = pd.read_csv("data/product_data.csv")

data = data[data["volume"] != "{}"]


def get_json_property(series, field_name):
    return series.apply(lambda x: x.replace("\'", "\"")) \
        .apply(lambda x: x.replace("\\", "")) \
        .apply(lambda x: json.loads(x)[field_name])


alcohol = get_json_property(data["alcohol"], "value")
price = get_json_property(data["price"], "value")
volume = get_json_property(data["volume"], "value")

price_per_liter = price / volume

ml_alcohol_per_krone = (alcohol / 100) / price_per_liter * 1000

data["ml_alcohol_per_krone"] = ml_alcohol_per_krone
data["link"] = data["code"].apply(lambda code: f"https://www.vinmonopolet.no/p/{code}")
data = data[data["ml_alcohol_per_krone"] != 0]

data = data.sort_values(by="ml_alcohol_per_krone", ascending=True)
print(data[["code", "name", "ml_alcohol_per_krone", "link"]])

data["category"] = get_json_property(data["main_category"], "name")
data = data.sort_values(by="category")
seaborn.catplot(data=data, x="ml_alcohol_per_krone", y="category", kind="box")
plt.show()
