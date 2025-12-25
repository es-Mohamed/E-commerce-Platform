from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from items.models import Item
from cart.models import Cart
from .models import conversation, conversationMessage

from .forms import conversationmessageform

@login_required
def new_conversation(request, item_pk):
    items = get_object_or_404(Item, pk = item_pk)

    if items.created_by == request.user :
        return redirect("Dashboard:index")
    
    conversations = conversation.objects.filter(items = items).filter(members__in = [request.user.id])

    if conversations:
        return redirect('conversation:detail', pk=conversations.first().id)
    
    if request.method == "POST":
        form = conversationmessageform(request.POST)

        if form.is_valid():
            conversations = conversation.objects.create(items = items)
            conversations.members.add(request.user)
            conversations.members.add(items.created_by)
            conversations.save()

            conversation_message = form.save(commit = False)
            conversation_message.conversation = conversations
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect("item:Detail", pk = item_pk)
        
    else:
        form = conversationmessageform()

    return render(request, "conversation/new.html", {
            "form": form
        })

@login_required
@require_http_methods(["POST"])
def create_order_conversation(request):
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            return JsonResponse({'success': False, 'message': "No admin user configured."}, status=500)

        cart = Cart.objects.get(user=request.user, is_active=True)
        cart_items = cart.items.all()
        if not cart_items.exists():
            return JsonResponse({'success': False, 'message': "Your cart is empty."}, status=400)

        message_content = f"New Order Request from {request.user.username}:\n\n"
        total_order_price = 0
        for item in cart_items:
            message_content += f"- {item.item.name} (Quantity: {item.quantity}) at {item.price_at_addition:.2f} EGP each.\n"
            total_order_price += item.total_price
        message_content += f"\nTotal Order Price: {total_order_price:.2f} EGP"

        new_convo = conversation.objects.create()
        new_convo.members.add(request.user, admin_user)

        conversationMessage.objects.create(
            conversation=new_convo,
            content=message_content,
            created_by=request.user
        )

        cart.is_active = False
        cart.save()

        return JsonResponse({
            'success': True,
            'message': "Your order request has been sent successfully!",
            'conversation_url': redirect('conversation:detail', pk=new_convo.id).url
        })

    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'message': "You do not have an active cart."}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': "An unexpected error occurred."}, status=500)

@login_required
def inbox(request):
    conversations = conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required
def detail(request, pk):
    """
    Displays a single conversation and handles the sending of new messages.
    """
    # Retrieve the specific conversation, ensuring the user is a member
    conversation_obj = get_object_or_404(conversation.objects.filter(members__in=[request.user.id]), pk=pk)

    if request.method == 'POST':
        form = conversationmessageform(request.POST)
        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation_obj
            conversation_message.created_by = request.user
            conversation_message.save()
            # No need to save conversation_obj unless you have a last_updated field to modify
            return redirect('conversation:detail', pk=pk)
    else:
        form = conversationmessageform()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation_obj,
        'form': form
    })