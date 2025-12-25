import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from items.models import Item
from .models import Cart, CartItem

def validate_quantity(quantity):
    try:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError
        return quantity
    except (ValueError, TypeError):
        return None


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def add_to_cart(request, item_id):
    try:
        item = get_object_or_404(Item, id=item_id)
        quantity = validate_quantity(request.POST.get('quantity', 1))

        if quantity is None:
            return JsonResponse({'success': False, 'message': 'Invalid quantity'}, status=400)

        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            item=item,
            defaults={'quantity': quantity, 'price_at_addition': item.price}
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        return get_cart_data(request)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@login_required
def get_cart_data(request):
    try:
        cart = Cart.objects.filter(user=request.user, is_active=True).first()
        
        if not cart:
            return JsonResponse({
                'success': True,
                'cart_exists': False,
                'cart_items': [],
                'total_cart_price': '0.00',
                'total_items_in_cart': 0,
                'message': 'Your cart is empty.'
            })
            
        cart_items = cart.items.select_related('item').all()
        total_cart_price = sum(float(item.total_price) for item in cart_items)

        cart_items_data = []
        for cart_item in cart_items:
            cart_items_data.append({
                'item_id': cart_item.item.id,
                'item_name': str(cart_item.item.name),
                'item_image_url': cart_item.item.image.url if cart_item.item.image else None,
                'quantity': cart_item.quantity,
                'price_at_addition': str(cart_item.price_at_addition),
                'total_price': str(cart_item.total_price),
            })

        total_items_in_cart = cart_items.aggregate(Sum('quantity'))['quantity__sum'] or 0

        return JsonResponse({
            'success': True,
            'cart_exists': True,
            'cart_items': cart_items_data,
            'total_cart_price': f"{total_cart_price:.2f}",
            'total_items_in_cart': total_items_in_cart
        })

    except Cart.DoesNotExist:
        return JsonResponse({
            'success': True,
            'cart_exists': False,
            'cart_items': [],
            'total_cart_price': '0.00',
            'total_items_in_cart': 0,
            'message': 'Your cart is empty.'
        })


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def update_cart_item_quantity(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity < 1:
            cart_item.delete()
        else:
            cart_item.quantity = new_quantity
            cart_item.save()

        return get_cart_data(request)

    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'Item not found in cart.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def remove_from_cart(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_item = get_object_or_404(CartItem, cart=cart, item_id=item_id)
        item_name = str(cart_item.item)
        cart_item.delete()
        
        cart_data = get_cart_data(request).content
        response_data = json.loads(cart_data)
        response_data['message'] = f"'{item_name}' has been removed from your cart."
        response_data['success'] = True
        
        return JsonResponse(response_data)
        
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({'success': False, 'message': 'Item not found in cart.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)