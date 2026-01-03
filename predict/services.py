import joblib
import numpy as np
import os
from django.conf import settings

class PricePredictionService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            # パスを動的に取得（ml_modelsフォルダに置く場合）
            path = os.path.join(settings.BASE_DIR, 'predict', 'ml_models', 'house_price_prediction_joblib.pkl')
            cls._model = joblib.load(path)
        return cls._model

    @classmethod
    def predict(cls, data_list):
        model = cls.get_model()
        # 入力データをnumpy形式に変換して予測
        input_data = np.array(data_list).reshape(1, -1)
        prediction = model.predict(input_data)
        return round(prediction[0])