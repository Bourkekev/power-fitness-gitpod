from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm


def all_products(request):
    """ A view to show all products, sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            # allow case insensitive sorting
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            # exclude products with no sale price
            if sortkey == 'sale_price':
                products = products.exclude(sale_price__isnull=True)

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You did not enter any search terms!")
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # create string to sort by
    requested_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'requested_categories': categories,
        'requested_sorting': requested_sorting,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product detail """

    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)

    context = {
        'product': product,
        'reviews': reviews
    }
    return render(request, 'products/product_detail.html', context)


@staff_member_required
def add_product(request):
    """ Adds a product to the shop """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product successfully added')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           'Failed to add product. \
                            Please ensure the form is valid.')
    else:
        form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@staff_member_required
def edit_product(request, product_id):
    """ edit_product:

    * Edits an existing product

    \n Args:
    1. request: the POST request data from the form
    2. product_id: the ID of the product to be edited

    \n Returns:
    * The form, the product

    \n Redirects
    * User back to product page
    """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(
            request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Updated product successfully.')
            return redirect(reverse('product_detail',
                                    args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. \
                Please ensure the form is valid.')

    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are now editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@staff_member_required
def delete_product(request, product_id):
    """ Delete a product """

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


def review_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    print(product)
    if request.method == 'POST':
        # print(request.user)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            # print(product.id)
            review.product = product
            review.save()
            messages.success(request, 'Product review successfully submitted')
            print("success")
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            print("fail")
            messages.error(request,
                           'Failed to add product review. \
                            Please ensure the form is valid.')
    else:
        form = ReviewForm(instance=product)
    template = 'products/add_review.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)
