from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    """Vista de inicio de sesión."""
    if request.user.is_authenticated:
        return redirect('panelcontrol:inicio')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('panelcontrol:inicio')

    return render(request, 'cuentas/login.html', {'form': form})


def logout_view(request):
    """Vista de cierre de sesión."""
    logout(request)
    return redirect('cuentas:login')