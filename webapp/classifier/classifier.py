import pickle

import numpy as np

from util.preprocess import preprocess, target_names, target_names_ru

class SVCmodel:

    # Инициализация модели по пути с .pickle файлами - path
    def __init__(self, path: str):
        # путь к эмбеддингу
        vecPath = path + "/vec.pickle"
        # путь к модели
        svcPath = path + "/svc.pickle"

        # Загрузка tf-idf эмбеддинга
        self.vectorizer = None
        with open(vecPath, 'rb') as f:
            self.vectorizer = pickle.load(f)

        # Загрузка SVC модели
        self.svc = None
        with open(svcPath, 'rb') as f:
            self.svc = pickle.load(f)

    # Классификация переданного текста
    def transform(self, text: str) -> str:
        # Препроцессин и веторизация
        processedText = preprocess(text)
        vectorized = self.vectorizer.transform([processedText])

        # Классификация - вывод npмассив
        out = self.svc.predict(vectorized)
        # Выделение числа - ID класса из массива np.array -> int
        clsId = np.squeeze(out)
        # Получить название класса
        cls = target_names_ru[clsId]

        return cls
