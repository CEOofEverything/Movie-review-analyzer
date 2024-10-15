from django.shortcuts import render
from .forms import ReviewForm
from .utils import predict_rating, get_review_status, clear_text


def submit_review(request):
    result = None  # Переменная для хранения результата
    review = None  # Переменная для храненеия отзыва пользователя

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data['text']
            text = clear_text(review)
            status = get_review_status(text)
            rating = predict_rating(text, status)

            # Передаем результат для отображения на той же странице
            result = {
                'review': review,
                'rating': rating,
                'status': status
            }
    else:
        form = ReviewForm()
    return render(
                    request,
                    'analyze/submit_review.html',
                    {'review': review, 'form': form, 'result': result}
                )
