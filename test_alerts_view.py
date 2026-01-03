from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def test_alerts_view(request):
    """Test page to verify modal alerts work"""
    return render(request, 'deposits_test.html')
