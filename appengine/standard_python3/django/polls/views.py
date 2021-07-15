from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from collections import Counter
import uuid

from .models import Choice, Question, Product

def home(request):
    products = Product.objects.all()[:3]
    return render(request, "home.html",{
        'products':products
    })

def about(request):
    return render(request, "about.html",{})

def product(request, pid):
    product = Product.objects.get(id=pid)
    return render(request, "product.html",{
        'product':product
    })

def thanks(request):
    products = {}
    total = 0.00
    transactionId = uuid.uuid1()
    if request.COOKIES.get('basket'):
        ids = request.COOKIES.get('basket').split(',')
        products = Product.objects.filter(id__in=ids)
        quantities = []
        for p in products:
            p.quantity = ids.count(str(p.id))
            total = round(total + float(p.price) * p.quantity,2)
    return render(request, "thanks.html",{
        'products':products,
        'total':total+5.99,
        'transactionId': transactionId
    })

def contact(request):
    return render(request, "contact.html",{})

def payment(request):
    products = {}
    total = 0.00
    transactionId = uuid.uuid1()
    if request.COOKIES.get('basket'):
        ids = request.COOKIES.get('basket').split(',')
        products = Product.objects.filter(id__in=ids)
        quantities = []
        for p in products:
            p.quantity = ids.count(str(p.id))
            total = round(total + float(p.price) * p.quantity,2)
    return render(request, "payment.html",{
        'products':products,
        'total':total+5.99,
        'transactionId': transactionId
    })

def products(request):
    products = Product.objects.all()
    return render(request, "products.html",{
        'products':products
    })

def basket(request):
    products = {}
    total = 0.00
    if request.COOKIES.get('basket'):
        ids = request.COOKIES.get('basket').split(',')
        products = Product.objects.filter(id__in=ids)
        quantities = []
        for p in products:
            p.quantity = ids.count(str(p.id))
            total = round(total + float(p.price) * p.quantity,2)
    return render(request, "basket.html",{
        'products':products,
        'total':total
    })

def searchResults(request):
    products = Product.objects.all()
    results = len(products)
    return render(request, "searchResults.html",{
        'products':products,
        'results':results
    })

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,))
        )
