# -*- coding: utf-8 -*-
# @Author: ander
# @Date:   2021-07-26 12:05:04
# @Last Modified by:   ander
# @Last Modified time: 2021-07-29 15:09:18
import pandas as pd
from .data import provinces_coordinates


def get_platform_pie(df):
    platform_counts = df['platform'].value_counts()
    platform_data = [{"name": name, "value": value} for name, value in platform_counts.items()]
    return {'platform_data': platform_data}


def get_product_line_income_bar(df):
    product_line_incomes = df[['product_line', 'price']].groupby('product_line').sum()
    product_line_incomes = product_line_incomes.sort_values(by='price', ascending=False)
    data = {
        'x_data': product_line_incomes.index.to_list(),
        'y_data': product_line_incomes['price'].to_list()
    }
    return data


def get_daily_income_line(df):
    orders_df = df[df['pay_time'].notna()]
    orders_df['pay_time'] = orders_df['pay_time'].dt.tz_convert('Asia/Shanghai')
    orders_df['pay_time'] = orders_df['pay_time'].dt.date
    start_date, end_date = orders_df['pay_time'].min(), orders_df['pay_time'].max()
    dates_index = pd.date_range(start_date, end_date)
    daily_income = pd.Series(index=dates_index, dtype='float64').fillna(0)
    groupby_pay_time_df = orders_df[['pay_time', 'price']].groupby('pay_time').sum()
    daily_income += groupby_pay_time_df['price']
    daily_income = daily_income.fillna(0.0)
    x_data = [dt.strftime("%Y-%m-%d") for dt in daily_income.index]
    y_data = daily_income.values.tolist()
    return {'x_data': x_data, 'y_data': y_data}


def get_total_income(df):
    total_income = df['price'].sum()
    return {'total_income': total_income}


def get_provinces_sales_map(df):
    def get_province_name(row):
        for province in provinces:
            if row.startswith(province):
                return province

    provinces = provinces_coordinates.keys()
    provinces_data = df['user_address'].apply(get_province_name)
    provinces_sales = []
    provinces_data_value_counts = provinces_data.value_counts()
    min_value = int(provinces_data_value_counts.min())
    max_value = int(provinces_data_value_counts.max())
    for index, value in provinces_data_value_counts.items():
        coordinates = provinces_coordinates[index]
        provinces_sales.append({'name': index, 'value': coordinates + [value]})
    return {
        'provinces_sales': provinces_sales,
        'min_value': min_value,
        'max_value': max_value
    }
