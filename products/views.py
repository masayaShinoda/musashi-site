from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Product


@require_http_methods(['GET', 'POST'])
def products(request):
    is_htmx_request = request.headers.get('HX-Request')

    products_qs = Product.objects.all().order_by('-date_modified')
    per_page = 1

    # paginator logic
    paginator = Paginator(products_qs, per_page)
    page_number = request.GET.get('page', 1)  # 1 by default

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # if page is not an int, return first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if HTMX request and page number is out of range, return empty content
        if is_htmx_request:
            return HttpResponse("")
        # if standard browser request, return last page
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'is_htmx_request': is_htmx_request,
    }

    # If the request comes from HTMX, return only the product grid HTML.
    if is_htmx_request:
        template = 'partials/_products_list.html'
    else:
        template = 'pages/products.html'

    # If the request is a standard browser load, return the full page
    return render(request, template, context)


@require_http_methods(['GET'])
def product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    context = {
        'product': product
    }

    return render(request, 'pages/product.html', context)
