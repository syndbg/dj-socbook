from django.dispatch import Signal


account_befriended = Signal(providing_args=['account', 'other_account'])
friend_request_accepted = Signal(providing_args=['from_account', 'to_account'])
friend_request_rejected = Signal(providing_args=['from_account', 'to_account'])
friend_request_sent = Signal(providing_args=['from_account', 'to_account'])
new_profile_created = Signal(providing_args=['account'])
