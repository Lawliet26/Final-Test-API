from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class MenuItemAnonThrottle(AnonRateThrottle):
    scope = 'menu_items_anon'
    
class MenuItemUserThrottle(UserRateThrottle):
    scope = 'user'