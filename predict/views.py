from django.shortcuts import render
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import joblib
from .models import HousePricePrediction
from django.http import HttpResponse
import csv

def home(request):
    return render(request, 'home.html')

def predict(request):
    return render(request, 'predict.html')

def result(request):
    model = pd.read_pickle("house_price_prediction_pdtopickle.pickle")
    
    var1 = float(request.GET['n1'])
    var2 = float(request.GET['n2'])
    var3 = float(request.GET['n3'])
    var4 = float(request.GET['n4'])
    var5 = float(request.GET['n5'])

    pred = model.predict(np.array([var1, var2, var3, var4, var5]).reshape(1,-1))
    pred = round(pred[0])

    HousePricePrediction.objects.create(Income=var1, Age=var2, Room=var3, Bedroom=var4, Population=var5, Price=pred)    
    
    price = str(pred)
        
    return render(request, 'result.html', {'result':price})

def view_data(request):
    data = {"dataset": HousePricePrediction.objects.all()}
    return render(request, "view_data.html", data)

def exportcsv(request):
    parameters = HousePricePrediction.objects.all()
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    response['Content-Disposition'] = 'attachment; filename=predresults.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', '平均地域所得', '平均築年数', '1戸あたり平均部屋数', '1戸あたり寝室数', '地域人口', '予測住宅価格'])
    studs = parameters.values_list('id','Income', 'Age', 'Room', 'Bedroom', 'Population', 'Price')
    for std in studs:
        writer.writerow(std)
    return response

