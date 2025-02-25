from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from users.models import UserProfile

@login_required
def product_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'products/product_list.html', {'products': products, 'categories': categories})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product, Category

@login_required
def add_product(request):
    if request.user.role not in ["admin", "trader", "sales"]:
        return JsonResponse({"error": "You do not have permission to create a product."}, status=403)

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category_id = request.POST.get('category')
        image = request.FILES.get('image', None)  # Optional image

        category = Category.objects.get(id=category_id) if category_id else None

        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image,  # If no image is uploaded, it will be None
            seller=request.user
        )

        return redirect('product_list')

    categories = Category.objects.all()
    return render(request, 'products/add_product.html', {'categories': categories})


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
