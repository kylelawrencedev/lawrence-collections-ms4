from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from checkout.models import Order


from .models import UserProfile, OrderInquiry
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


def order_inquiry(request):

    if request.method == 'POST':
        message = request.POST['message']
        order_number = request.POST['order_number']

        inquiry = OrderInquiry( message=message,
                               order_number=order_number)

        # send email
        send_mail('Order Inquiry',
                  'There has been an inquiry for '
                  '. Sign into the admin panel for more info.',
                  'kylelawrence19@gmail.com',
                  [settings.DEFAULT_FROM_EMAIL])

        messages.success(
            request,
            "Your inquiry has been submitted, " +
            "we will get back to you shortly.")

        return redirect(request, 'profiles/profile.html')



#@login_required
#def wishlist(request):

#   product = Product.objects.filter(
#        wishlists=request.user)
#    context = {
#        'wishlists': wishlists,
#    }
#    template = 'profiles/wishlist.html'
#
#    return render(request, template, context)


#@login_required
#def add_to_wishlist(request, item_id):
#    """ Add and remove items from users wishlist """
#    product = get_object_or_404(Product, pk=item_id)
#    if product.wishlists.filter(id=request.user.id).exists():
#        product.wishlists.remove(request.user)
#        messages.success(request, product.name + " has been removed from your Wishlist")
#    else:
#       product.wishlists.add(request.user)
#        product.messages.success(request, "Added " + product.name + " to your Wishlist")
#    return HttpResponseRedirect(request.META["HTTP_REFERER"])
