# -*- coding: utf-8 -*-
# @Author: ander
# @Date:   2021-07-19 12:26:04
# @Last Modified by:   ander
# @Last Modified time: 2021-07-23 11:33:22
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path("api/order/filter", views.order_filter_api),
    path("api/order/data_vis", views.order_data_vis_api),
]
