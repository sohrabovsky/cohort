#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 09:43:52 2023

@author: sohrab-salehin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from operator import attrgetter
import matplotlib.colors as mcolors
import plotly.express as px
import os

path = r"/home/sohrab-salehin/Documents/python_scripts/GitHub/cohort/mobile_date_id"
list_of_files = os.listdir(path)
list_of_files = [i for i in list_of_files if i[-3:] == "csv"]
df = pd.DataFrame()
for file in list_of_files:
    temp_df = pd.read_csv(path + "//" + file, parse_dates=["Registered Date"])
    df = pd.concat([df, temp_df], ignore_index=True)
df = df.drop_duplicates(subset="ID").reset_index(drop=True)

df = df.rename(
    columns={
        "User Unique Identifier": "mobile",
        "ID": "invoice_id",
        "Registered Date": "date",
    }
)
df.dropna(subset=["mobile"], inplace=True)

n_orders = df.groupby(by="mobile")["invoice_id"].nunique()
mult_orders_perc = np.sum(n_orders > 1) / df.mobile.nunique()
print(f"{100 * mult_orders_perc:.2f}% of customers ordered more than once.")

fig = px.histogram(n_orders)
fig.show()

df = df[["mobile", "invoice_id", "date"]].drop_duplicates()

# Monthly Cohort:
    
df["order_month"] = df["date"].dt.to_period("M")
df["cohort"] = df.groupby("mobile")["date"].transform("min").dt.to_period("M")

df_cohort = (
    df.groupby(["cohort", "order_month"])["mobile"].nunique().reset_index(drop=False)
)
df_cohort["period_number"] = (df_cohort.order_month - df_cohort.cohort).apply(
    attrgetter("n")
)

cohort_pivot = df_cohort.pivot_table(
    index="cohort", columns="period_number", values="mobile"
)

cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
retention_matrix = retention_matrix.iloc[:, 1:]

with sns.axes_style("white"):
    fig, ax = plt.subplots(
        1, 2, figsize=(12, 8), sharey=True, gridspec_kw={"width_ratios": [1, 11]}
    )

    # retention matrix
    sns.heatmap(
        retention_matrix,
        mask=retention_matrix.isnull(),
        annot=True,
        fmt=".0%",
        cmap="RdYlGn",
        ax=ax[1],
    )
    ax[1].set_title("Monthly Cohorts: User Retention - Dom. Hotel", fontsize=16)
    ax[1].set(xlabel="# of periods", ylabel="")
    # cohort size
    cohort_size_df = pd.DataFrame(cohort_size).rename(columns={0: "cohort_size"})
    white_cmap = mcolors.ListedColormap(["white"])
    sns.heatmap(
        cohort_size_df, annot=True, cbar=False, fmt="g", cmap=white_cmap, ax=ax[0]
    )

    fig.tight_layout()
    plt.savefig("dom. Hotel - Monthly.png")

# Quarterly Cohort

path = r"/home/sohrab-salehin/Documents/python_scripts/promotion_analysis_project/dom_hotel/mobile_date_id"
list_of_files = os.listdir(path)
list_of_files = [i for i in list_of_files if i[-3:] == "csv"]
df = pd.DataFrame()
for file in list_of_files:
    temp_df = pd.read_csv(path + "//" + file, parse_dates=["Registered Date"])
    df = pd.concat([df, temp_df], ignore_index=True)
df = df.drop_duplicates(subset="ID").reset_index(drop=True)

df = df.rename(
    columns={
        "User Unique Identifier": "mobile",
        "ID": "invoice_id",
        "Registered Date": "date",
    }
)
df.dropna(subset=["mobile"], inplace=True)


df = df[["mobile", "invoice_id", "date"]].drop_duplicates()
df["order_quarter"] = df["date"].dt.to_period("Q")
df["cohort"] = df.groupby("mobile")["date"].transform("min").dt.to_period("Q")

df_cohort = (
    df.groupby(["cohort", "order_quarter"])["mobile"].nunique().reset_index(drop=False)
)
df_cohort["period_number"] = (df_cohort.order_quarter - df_cohort.cohort).apply(
    attrgetter("n")
)

cohort_pivot = df_cohort.pivot_table(
    index="cohort", columns="period_number", values="mobile"
)

cohort_pivot = cohort_pivot[-9:]

cohort_size = cohort_pivot.iloc[:, 0]
retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
retention_matrix = retention_matrix.iloc[:, 1:]

retention_matrix = retention_matrix.iloc[-9:, :9]

with sns.axes_style("white"):
    fig, ax = plt.subplots(
        1, 2, figsize=(12, 8), sharey=True, gridspec_kw={"width_ratios": [1, 11]}
    )

    # retention matrix
    sns.heatmap(
        retention_matrix,
        mask=retention_matrix.isnull(),
        annot=True,
        fmt=".0%",
        cmap="RdYlGn",
        ax=ax[1],
    )
    ax[1].set_title("Quarterly Cohorts: User Retention - Dom. Hotel", fontsize=16)
    ax[1].set(xlabel="# of periods", ylabel="")
    # cohort size
    cohort_size_df = pd.DataFrame(cohort_size).rename(columns={0: "cohort_size"})
    white_cmap = mcolors.ListedColormap(["white"])
    sns.heatmap(
        cohort_size_df, annot=True, cbar=False, fmt="g", cmap=white_cmap, ax=ax[0]
    )

    fig.tight_layout()
    plt.savefig("dom. Hotel - Quarterly.png")