from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from checkout.models import Order
from products.models import Product

from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """ Display the user's profile """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                 request, 'Update failed. Please ensure form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
def wishlist(request):

    products = Product.objects.filter(
        users_wishlist=request.user.is_authenticated)
    context = {
        'wishlist': products
    }
    template = 'profiles/wishlist.html'

    return render(request, template, context)


@login_required
def add_to_wishlist(request, product_id):
    """ Add and remove items from users wishlist """
    product = get_object_or_404(Product, pk=product_id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.name + " has been removed from your Wishlist")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.name + " to your Wishlist")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
