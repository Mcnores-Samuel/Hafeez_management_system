#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

def action_on_click(request, data_id):
  return redirect('dashboard')