from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from accounts.models import Account


@login_required
def index(request):
    return redirect('activities:activities')


def search(request):
    search_query = request.GET('search_query', '')
    if search_query:
        results = {}
        results['accounts'] = Account.objects.filter(Q(profile__display_name__icontains=search_query) |
                                                     Q(first_name__icontains=search_query) |
                                                     Q(last_name__icontains=search_query))
        return render(request, 'search_results.html', {'search_query': search_query, 'results': results})

    return render(request, 'search.html')
