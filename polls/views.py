from .forms import DocumentForm
from .models import Document
from datetime import datetime
from django_pandas.io import read_frame
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from io import BytesIO
from io import StringIO
from itertools import islice
from openpyxl import Workbook
from rapidfuzz import process, fuzz
import csv
import ipdb
import json
import logging
import numpy as np
import openpyxl
import pandas as pd
import urllib
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)
# Create your views here.


def touploads(request):
    return render(request, "landingpage.html")


def getexcel(pk):
    Doc = Document.objects.get(id=pk)
    filePath = "http://127.0.0.1:8000" + Doc.document.url
    link = urllib.request.urlopen(filePath).read()
    excel = pd.read_excel(link)
    return excel


def data(excel):
    df = pd.DataFrame(excel)
    return df


def tojson(dataFrame):
    json_records1 = dataFrame.reset_index().to_json(orient="records")
    dataJson = json.loads(json_records1)
    return dataJson


def fuzzy(excel, percent_number):
    df = pd.DataFrame(excel)
    NameTests = [name for name in df["NameTest"] if isinstance(name, str)]
    data = {"Matching": [], "Score": [], "Name": []}
    for Name in df["Name"]:
        if isinstance(Name, str):
            match = process.extractOne(
                Name, NameTests, scorer=fuzz.ratio, processor=None, score_cutoff=int(percent_number)
            )
        if match:
            data["Matching"].append(match[0])
            data["Score"].append(match[1])
            data["Name"].append(Name)
    df1 = pd.DataFrame(data)
    return df1


def home(request):
    documents = Document.objects.all()
    return render(request, "home.html", {"documents": documents})


def dataframe(excel):
    excel = pd.DataFrame(excel)
    print(excel)
    return excel


def convert(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=export.csv"
    df = pd.DataFrame()
    print("ddd", df)
    df.to_csv(path_or_buf=response)
    return response


def index(request):
    getmodel = Document.objects.all()
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        # ipdb.set_trace()
        if form.is_valid():
            res = form.save()
            excel = getexcel(res.id)
            dataj = data(excel)
            json_befor = tojson(dataj)
            fuzz = fuzzy(excel, form["percent_number"].data)
            conv = dataframe(fuzz)
            json_after = tojson(fuzz)
            return render(request, "model_form_upload.html", {"befor_tables": json_befor, "after_tables": json_after})
    else:
        form = DocumentForm()
        return render(request, "upload.html", {"form": form})
    return render(
        request,
        "upload.html",
    )
