import requests
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductVariant, Category, OrderItem
from .cart import Cart
from .forms import OrderForm
from .utils import send_telegram_message


@require_http_methods(['GET', 'POST'])
def products(request):
    is_htmx_request = request.headers.get('HX-Request')
    page_number = request.GET.get('page', 1)  # 1 by default

    products_qs = Product.objects.all()
    per_page = 10

    # retrieve selected category IDs
    selected_category_ids = request.GET.getlist('category')

    if selected_category_ids:
        products_qs = products_qs.filter(
            categories__id__in=selected_category_ids).distinct()
        # if filters change, reset
        if not is_htmx_request:
            page_number = 1

    products_qs = products_qs.order_by('-date_modified')

    # paginator logic
    paginator = Paginator(products_qs, per_page)

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

    # fetch all categories for filter menu
    categories = Category.objects.all().order_by('name')

    context = {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'is_htmx_request': is_htmx_request,
        'categories': categories,
        'selected_categories': selected_category_ids,
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


def render_cart_updates(request, cart):
    """
    Returns the sidebar content. 
    The sidebar template MUST contain the badge OOB swap logic.
    """
    return render(request, 'partials/_cart_sidebar_content.html', {'cart': cart})


@require_http_methods(["POST"])
def cart_add(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    cart.add(variant_id=variant.id, quantity=quantity)
    return render_cart_updates(request, cart)


@require_http_methods(["DELETE", "POST"])
def cart_remove(request, variant_id):
    cart = Cart(request)
    cart.remove(variant_id)
    return render_cart_updates(request, cart)


@require_http_methods(['POST'])
def cart_update(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    try:
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            # override_quantity=True replaces the number instead of adding to it
            cart.add(variant_id=variant.id, quantity=quantity,
                     override_quantity=True)
        else:
            # If user types 0, remove the item
            cart.remove(variant_id)
    except ValueError:
        pass

    # Reuse existing helper to render the sidebar content
    return render_cart_updates(request, cart)


@require_http_methods(["GET", "POST"])
def checkout(request):
    cart = Cart(request)

    # 1. Redirect if cart is empty
    if len(cart) == 0:
        return redirect('products')

    if request.method == 'POST':
        form = OrderForm(request.POST)

        # --- START TURNSTILE VALIDATION ---
        turnstile_token = request.POST.get('cf-turnstile-response')

        # 1. Check if token exists
        if not turnstile_token:
            return render(request, 'pages/checkout.html', {
                'cart': cart,
                'form': form,
                'turnstile_error': "Please complete the security check."
            })

        # 2. Verify with Cloudflare API
        verify_response = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data={
                'secret': settings.TURNSTILE_SECRET_KEY,
                'response': turnstile_token
            },
            timeout=5
        ).json()

        # 3. Check if verification failed
        if not verify_response.get('success'):
            return render(request, 'pages/checkout.html', {
                'cart': cart,
                'form': form,
                'turnstile_error': "Security check failed. Please refresh and try again."
            })
        # --- END TURNSTILE VALIDATION ---

        if form.is_valid():
            # 2. Save Order
            order = form.save()

            # 3. Save Order Items & Build Telegram Message
            msg_lines = [
                f"<b>New Order #{order.id}</b>",
                f"Name: {order.first_name} {order.last_name}",
                f"Phone: {order.phone}",
            ]

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['variant'].product,
                    variant=item['variant'],
                    quantity=item['quantity']
                )
                # Add to message
                msg_lines.append(
                    f"- {item['quantity']}x {item['variant'].product.name} ({item['variant'].volume.name})")

            # Add Total
            msg_lines.append(f"\n<b>Total: ${cart.get_total_price()}</b>")
            if order.remarks:
                msg_lines.append(f"Remarks: {order.remarks}")

            # 4. Send Telegram Notification
            send_telegram_message("\n".join(msg_lines))

            # 5. Clear Cart and Redirect to Success
            cart.clear()
            return render(request, 'pages/checkout_success.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'pages/checkout.html', {'cart': cart, 'form': form})
