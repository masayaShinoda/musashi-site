from decimal import Decimal
from django.conf import settings
from .models import ProductVariant


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart_session_id')
        if not cart:
            cart = self.session['cart_session_id'] = {}
        self.cart = cart

    def add(self, variant_id, quantity=1, override_quantity=False):
        variant_id = str(variant_id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {'quantity': 0, 'price': 0}

        if override_quantity:
            self.cart[variant_id]['quantity'] = quantity
        else:
            self.cart[variant_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, variant_id):
        variant_id = str(variant_id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the variants from the database.
        """
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.filter(
            id__in=variant_ids).select_related('product', 'volume')

        # Create a helper dict for O(1) lookups
        variant_map = {str(v.id): v for v in variants}

        # Loop through the SESSION keys to preserve order and integrity
        for variant_id, session_item in self.cart.items():
            variant = variant_map.get(variant_id)

            if variant:
                # IMPORTANT: Create a NEW dictionary for the template.
                # Do NOT modify 'session_item' directly, or you inject Decimals into the session.
                item = session_item.copy()

                item['variant'] = variant

                # Handle price conversion safely for calculation
                price_val = variant.price if variant.price is not None else 0
                item['price'] = Decimal(price_val)
                item['total_price'] = item['price'] * item['quantity']

                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        # We must re-fetch variants to get accurate prices
        total = Decimal(0)
        # We can reuse the logic from __iter__ to ensure consistency
        for item in self:
            total += item['total_price']
        return total

    def clear(self):
        del self.session['cart_session_id']
        self.save()
