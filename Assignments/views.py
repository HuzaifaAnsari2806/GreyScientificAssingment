from django.shortcuts import redirect
from django.conf import settings

def login(request):
    auth0_domain = settings.AUTH0_DOMAIN
    client_id = settings.CLIENT_ID
    redirect_uri = 'http://localhost:8000/hospital/auth/callback'
    return redirect(f"https://{auth0_domain}/authorize?response_type=token&client_id={client_id}&redirect_uri={redirect_uri}")

def callback(request):
    # Handle the callback from Auth0
    return redirect('/hospital/patients_records')

def logout(request):
    logout_url = f"https://{settings.AUTH0_DOMAIN}/v2/logout?returnTo=http://localhost:8000//hospital/patients_records"
    request.session.flush()
    return redirect(logout_url)
