from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from .models import Product


@require_http_methods(['GET'])
def products(request):
    products = Product.objects.all().order_by('-date_modified')

    # paginator logic
    paginator = Paginator(products, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    # If the request comes from HTMX, return only the product grid HTML.
    if request.headers.get('HX-Request'):
        template = 'partials/products_list.html'
    else:
        template = 'pages/products.html'

    # If the request is a standard browser load, return the full page
    return render(request, template, context)


@require_http_methods(['POST'])
def product_details(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    # TODO

    return 0
