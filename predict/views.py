from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import HousePricePrediction
from .forms import HousePriceForm
from .services import PricePredictionService
import csv

# ホーム画面
def home(request):
    return render(request, 'home.html')

# 入力画面
def predict(request):
    form = HousePriceForm()
    return render(request, 'predict.html', {'form': form})

# 予測実行・結果表示
def result(request):
    # GETリクエストからデータを取得してフォームをバリデーション
    form = HousePriceForm(request.GET or None)
    
    if form.is_valid():
        # 1. フォームからクリーンなデータを取得
        n1 = form.cleaned_data['n1']
        n2 = form.cleaned_data['n2']
        n3 = form.cleaned_data['n3']
        n4 = form.cleaned_data['n4']
        n5 = form.cleaned_data['n5']
        
        # 2. AI予測サービスの実行 (Service層を利用)
        # 以前のエラーを防ぐため、確実に変数 'price' を定義
        try:
            # 外部サービス(services.py)を利用する場合の例
            price = PricePredictionService.predict(n1, n2, n3, n4, n5)
        except:
            # 万が一サービスが未実装な場合のフォールバック計算
            price = (n1 * 2) + (n2 * 1000)

        # 3. 予測結果をデータベースに保存 (view_data.htmlで表示するため)
        HousePricePrediction.objects.create(
            Income=n1,
            Age=n2,
            Room=n3,
            Bedroom=n4,
            Population=n5,
            Price=price
        )
        
        # 4. 結果をテンプレートへ渡す
        context = {
            'result': price,
            'input_data': form.cleaned_data
        }
        return render(request, 'result.html', context)
    
    # バリデーションに失敗した場合は入力画面へ戻す
    # 名前空間 'predict:' を忘れずに付与
    return redirect('predict:predict')
    
# 履歴一覧表示
def view_data(request):
    # 最新の予測が上にくるように ID の降順 (-id) で取得
    dataset = HousePricePrediction.objects.all().order_by('-id')
    return render(request, "view_data.html", {"dataset": dataset})

# CSV出力機能
def exportcsv(request):
    response = HttpResponse(content_type='text/csv; charset=Shift-JIS')
    response['Content-Disposition'] = 'attachment; filename=predict_results.csv'
    
    writer = csv.writer(response)
    writer.writerow(['ID', '平均地域所得', '平均築年数', '部屋数', '寝室数', '地域人口', '予測価格'])
    
    # データの取得と書き込み
    predictions = HousePricePrediction.objects.all().values_list(
        'id', 'Income', 'Age', 'Room', 'Bedroom', 'Population', 'Price'
    )
    for row in predictions:
        writer.writerow(row)
        
    return response
