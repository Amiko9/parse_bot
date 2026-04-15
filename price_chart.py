import pandas as pd
import plotly.express as px

df = pd.read_csv("./example/price.csv")

fig = px.line(df, x="Date", y="Price", color="Product", title="Product Prices")
fig.show()