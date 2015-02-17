from django.dispatch import Signal


account_befriended = Signal(providing_args=['account', 'other_account'])
friend_request_accepted = Signal(providing_args=[''])
friend_request_sent = Signal(providing_args=['account', 'other_account'])
friend_request_rejected = Signal(providing_args=[])
