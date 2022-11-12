import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
import datetime as dt
import math
import seaborn as sns
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


data = pd.read_excel("Kaggle_dosyalar/all-weeks-countries.xlsx")
df=data.copy()

def Analysis(df):
    print(5*"*"+"DF1 Verisinin Analizi"+"*"*5)
    print("\nGENEL BİLGİ")
    print(f"\n{df.info()}")
    print(f"\n\nDESCRİBE \n{df.describe().T}")
    print(f"\n\nSÜTUNLAR \n{[col for col in df.columns]}")
    print(f"\n\nSHAPE\n{df.shape}")
    print(f"\n\nBOŞ DEĞER\n{df.isnull().sum()}\n\n")

Analysis(df)

def Arrange_Date(df):
    df["weeks"]=pd.to_datetime(df["week"])
    current_date=dt.datetime(2022,12,1)
    df["analyze_week"]=(((current_date-df["weeks"]).dt.days/7)).apply(lambda x : math.ceil(x))
    df["analyze_month"]=(((current_date-df["weeks"]).dt.days/30)).apply(lambda x : math.ceil(x))
    df["cumulative_months_in_top_10"]=(((df["cumulative_weeks_in_top_10"]/4))).apply(lambda x : "%.2f" % x).astype("float")
    del df["weeks"]
    print(df.head())

Arrange_Date(df)

def Arrange_Sort_df(df):
    sort_df=df.groupby(["country_name","category","show_title","analyze_week","analyze_month"]).agg({"cumulative_weeks_in_top_10":"mean",                                                                                                     "cumulative_months_in_top_10":"mean"})
    sort_df.reset_index(inplace=True)
    sort_df.columns=["country_name","category","show_title","analyze_week","analyze_month","cumulative_weeks_in_top_10_mean","cumulative_months_in_top_10_mean"]
    print(sort_df.head(3))
    return sort_df

sort_df=Arrange_Sort_df(df)

"""
q1, q2, q3 = sort_df["analyze_week"].quantile([0.25, 0.5, 0.75])

sort_df["week_rank"] = sort_df["analyze_week"]

Q1 = sort_df[sort_df["analyze_week"] < q1]["cumulative_weeks_in_top_10_mean"].mean() * 20 / 100
Q2 = sort_df[(sort_df["analyze_week"] > q1) & (sort_df["analyze_week"] <= q2)]["cumulative_weeks_in_top_10_mean"].mean() * 24 / 100
Q3 = sort_df[(sort_df["analyze_week"] > q2) & (sort_df["analyze_week"] <= q3)]["cumulative_weeks_in_top_10_mean"].mean() * 26 / 100
Q4 = sort_df[sort_df["analyze_week"] > q3]["cumulative_weeks_in_top_10_mean"].mean() * 30 / 100

sort_df["week_rank"]=sort_df["week_rank"].apply(lambda x: Q1 if (x <= q1) else Q2 if (q2 >= x > q1) else Q3 if (q2 >= x > q1) else Q4)

result_sorts = {"Q1": sort_df[sort_df["week"] < q1]["cumulative_weeks_in_top_10_mean"].mean() * 20 / 100,
          "Q2": sort_df[(sort_df["week"] > q1) & (sort_df["week"] <= q2)][
                    "cumulative_weeks_in_top_10_mean"].mean() * 24 / 100,
          "Q3": sort_df[(sort_df["week"] > q2) & (sort_df["week"] <= q3)][
                    "cumulative_weeks_in_top_10_mean"].mean() * 26 / 100,
          "Q4": sort_df[sort_df["week"] > q3]["cumulative_weeks_in_top_10_mean"].mean() * 30 / 100
          }
sort_df=sort_df[["country_name","week_rank", "show_title"]]
sort_df=sort_df.groupby(["country_name","show_title"]).agg({"week_rank":"mean"})
sort_df.head()
sort_df.reset_index(inplace=True)

sort_df[sort_df["country_name"]=="Argentina"].sort_values(by="week_rank",ascending=False,ignore_index=True)

"""

###Sorting by Average, Weekly

def Weekly_Sort(df,category,country,thres=[0.2,0.24,0.26,0.3]):
    q1, q2, q3 = df["analyze_week"].quantile([0.25, 0.5, 0.75])

    df["week_rank"] = df["analyze_week"]

    Q1 = df[df["analyze_week"] < q1]["cumulative_weeks_in_top_10_mean"].mean() * 20 / 100
    Q2 = df[(df["analyze_week"] > q1) & (df["analyze_week"] <= q2)]["cumulative_weeks_in_top_10_mean"].mean() * 24 / 100
    Q3 = df[(df["analyze_week"] > q2) & (df["analyze_week"] <= q3)]["cumulative_weeks_in_top_10_mean"].mean() * 26 / 100
    Q4 = df[df["analyze_week"] > q3]["cumulative_weeks_in_top_10_mean"].mean() * 30 / 100

    df["week_rank"] = df["week_rank"].apply(lambda x: Q1 if (x <= q1) else Q2 if (q2 >= x > q1) else Q3 if (q2 >= x > q1) else Q4)

    df = df[["country_name","category","week_rank", "show_title"]]
    df = df.groupby(["country_name","category", "show_title"]).agg({"week_rank": "mean"})
    df.head()
    df.reset_index(inplace=True)

    print(df[(df["country_name"] == country) & (df["category"]==category)].sort_values(by="week_rank", ascending=False, ignore_index=True))
    return df[(df["country_name"] == country) & (df["category"]==category)].sort_values(by="week_rank", ascending=False, ignore_index=True)



week=Weekly_Sort(sort_df,"TV","Argentina")


def Montly_Sort(df,category,country,thres=[0.2,0.24,0.26,0.3]):
    q1, q2, q3 = df["analyze_month"].quantile([0.25, 0.5, 0.75])

    df["month_rank"] = df["analyze_month"]

    Q1 = df[df["analyze_month"] < q1]["cumulative_months_in_top_10_mean"].mean() * 20 / 100
    Q2 = df[(df["analyze_month"] > q1) & (df["analyze_month"] <= q2)]["cumulative_months_in_top_10_mean"].mean() * 24 / 100
    Q3 = df[(df["analyze_month"] > q2) & (df["analyze_month"] <= q3)]["cumulative_months_in_top_10_mean"].mean() * 26 / 100
    Q4 = df[df["analyze_month"] > q3]["cumulative_weeks_in_top_10_mean"].mean() * 30 / 100

    df["month_rank"] = df["month_rank"].apply(lambda x: Q1 if (x <= q1) else Q2 if (q2 >= x > q1) else Q3 if (q2 >= x > q1) else Q4)


    df = df[["country_name","category","month_rank", "show_title"]]
    df = df.groupby(["country_name","category", "show_title"]).agg({"month_rank": "mean"})
    df.reset_index(inplace=True)
    print(df[(df["country_name"] == country) & (df["category"]==category)].sort_values(by="month_rank", ascending=False, ignore_index=True))
    return df[(df["country_name"] == country) & (df["category"]==category)].sort_values(by="month_rank", ascending=False, ignore_index=True)

month=Montly_Sort(sort_df,"TV","Argentina")

def Compare(df,category,country,thres=[0.2,0.24,0.26,0.3]):
    week=Weekly_Sort(df,category,country)
    month=Montly_Sort(df,category,country)
    ifade=""
    if category == "TV":
        ifade += "dizisi"
    else:
        ifade += "filmi"
    for x, col in enumerate(week["show_title"]):
        print(f"\nHaftalık ortalamada {x}. olan {col} {ifade}=> "
              f"Aylık ortalamada {(month[month['show_title'] == col]).index[0]}. olmuştur")

Compare(sort_df,"Films","Vietnam")

#########################

def Sort_Analysis_Average_Method(df,category,country,thres=[0.2,0.24,0.26,0.3]):
    Analysis(df)
    Arrange_Date(df)
    sort_df=Arrange_Sort_df(df)
    Compare(sort_df,category,country)

Sort_Analysis_Average_Method(df,"TV","Argentina")