import re
import joblib
import string
from bs4 import BeautifulSoup

# Пути до моделей
lr_neg_model_path = 'models/logistic_regression_model_neg_rating.pkl'
lr_pos_model_path = 'models/logistic_regression_model_pos_rating.pkl'
lr_sentiment_model_path = 'models/logistic_regression_model.pkl'

# Путь до tf-idf векторайзера
vectorizer_path = 'vectorizer/tfidf_vectorizer.pkl'

# Загрузим предварительно обученные модели и tf-idf векторайзер
lr_neg_model = joblib.load(lr_neg_model_path)
lr_pos_model = joblib.load(lr_pos_model_path)
lr_sentiment_model = joblib.load(lr_sentiment_model_path)

vectorizer = joblib.load(vectorizer_path)


# Функция для очистки текста
def clear_text(text: str) -> str:
    """
    Очищает текст от HTML-тегов, ссылок, специальных символов и знаков препинания.
    Args:
        text (str): Исходный текст.
    Returns:
        str: Очищенный текст.
    """
    # Переводим текст в нижний регистр
    text = text.lower()
    # Удаляем html тэги
    text = BeautifulSoup(text, "html.parser").get_text()
    # Удаляем квадратные скобки
    text = re.sub(r'\[[^]]*\]', '', text)
    # Удаляем знаки препинания
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Удаляем ссылки
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Удаляем спец. символы и цифры
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text


def predict_rating(text: str, rating: str) -> int:
    """
    Предсказывает рейтинг на основе текста отзыва и его статуса.
    Args:
        text (str): Очищенный текст отзыва.
        rating (str): Статус отзыва (положительный или отрицательный).

    Returns:
        int: Предсказанный рейтинг.
    """
    text_vector = vectorizer.transform([text])
    if rating == "Positive":  # Положительный отзыв
        pred_rating = lr_pos_model.predict(text_vector)
    else:  # Отрицательный отзыв
        pred_rating = lr_neg_model.predict(text_vector)
    return pred_rating[0]


def get_review_status(text: str) -> str:
    """
    Определяет статус отзыва (положительный или отрицательный).
    Args:
        text (str): Очищенный текст отзыва.
    Returns:
        str: Статус отзыва ("Positive" для положительного, "Negative" для отрицательного).
    """
    text_vector = vectorizer.transform([text])
    # Предсказание тональности отзыва
    sentiment = lr_sentiment_model.predict(text_vector)
    return "Positive" if sentiment[0] == 1 else "Negative"
