import pandas as pd

year = 35
url = "https://www.myhora.com/lottery/stats.aspx?mx=09&vx={year}"

df = pd.read_html(url.format(year=year), flavor="bs4", header=None)
print(df[-1].head())

df_new = pd.DataFrame(df[-1][0].apply(lambda x: x.split(" ")).tolist())
df_new = df_new.drop([2, 4, 9, 14, 15, 16, 17, 18, 19], axis=1)
# df_new.columns = [
#     "day",
#     "month",
#     "year",
#     "first_prize",
#     "last_two",
#     "top_three",
#     "bottom_two",
#     "front_last_three",
# ]
print(df_new.tail())
