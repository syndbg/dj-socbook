from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET

from activities.models import Activity, Notification


@login_required
def notifications(request):
    account = request.user
    notifications = Notification.objects.filter(to_account=account)
    return render(request, '', {'notifications': notifications})


@require_POST
@login_required
def mark_seen_notification(request, notification_id):
    notification = Notification.objects.filter(pk=notification_id).first()
    if not notification:
        return HttpResponse(status=404)

    notification.seen = True
    notification.save(update_fields=['seen'])
    return HttpResponse(status=200)

