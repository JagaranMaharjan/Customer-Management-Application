from django.http import HttpResponse
from django.shortcuts import redirect


# check user had already login or not
def unauthenticated_user(view_func):
    # created wrapped function
    def wrapper_func(request, *args, **kwargs):
        # if user is already login then
        if request.user.is_authenticated:
            # redirect to home page
            return redirect('home')
        else:
            # if not login then display login page
            return view_func(request, *args, **kwargs)

    # return wrapper function
    return wrapper_func


# set permission to view pages
def allowed_users(allowed_roles=[]):
    def decorator(view_fun):
        def wrapper_func(request, *args, **kwargs):
            # default user group is set to none
            group = None
            # if user group exists in database
            if request.user.groups.exists():
                # hold new value in group i.e. users group
                group = request.user.groups.all()[0].name
            # according to user group
            if group in allowed_roles:
                # display view to user
                return view_fun(request, *args, **kwargs)
            else:
                # otherwise display message
                return HttpResponse("You are not authorized to view this page")

        # return wrapper function
        return wrapper_func

    # return decorators
    return decorator


# restrict views
def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        # default user group is set to none
        group = None
        # if user group exists in database
        if request.user.groups.exists():
            # hold new value in group i.e. users group
            group = request.user.groups.all()[0].name
        # if user group is customer then
        if group == 'customer':
            # redirect to user page
            return redirect('user_page')
        # if user group is admin then
        if group == 'admin':
            # display admin dashboard views
            return view_func(request, *args, **kwargs)

    # return wrapper function
    return wrapper_function
