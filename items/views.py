from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.utils.translation import gettext as _ 

from django.utils.translation import gettext_lazy as _lazy

from .forms import NewItemform, EditItemform

from .models import Item, Category

def Items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category_id')
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id = category_id)

    if query:
        items = items.filter(Q(name__icontains= query) | Q(description__icontains = query) | Q(price__icontains = query))

    return render(request, 'item/Items.html', {
        "items": items,
        "query": query,
        "categories": categories,
        "category_id": int(category_id) if category_id else 0
    })

def Detail(request, pk):
    items = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category= items.category, is_sold=False).exclude(pk=pk)

    return render(request, 'item/Detail.html', {
        'item':items,
        'related_item':related_items
    })

@login_required
def New(request):
    if request.method == 'POST':
        form = NewItemform(request.POST, request.FILES)

        if form.is_valid():
            items = form.save(commit=False)
            items.created_by = request.user
            items.save()

            return redirect('item:Detail', pk=items.id)
    else:
        form = NewItemform()

    return render(request, "item/form.html", {
        'form': form,
        "title": _lazy("Add New Item")
    })

@login_required
def Edit(request, pk):
    items = get_object_or_404(Item, pk=pk, created_by = request.user)
    if request.method == 'POST':
        
        form = EditItemform(request.POST, request.FILES, instance=items)
        if form.is_valid():
            form.save()


            return redirect('item:Detail', pk=items.id)
    else:
        form = EditItemform(instance=items)

    return render(request, "item/form.html", {
        'form': form,
        "title": _lazy("Edit Item")
    })

@login_required
def delete(request, pk):
    items = get_object_or_404(Item, pk=pk, created_by = request.user)
    items.delete()

    return redirect("Dashboard:index")