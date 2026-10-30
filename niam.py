class TicketTier:
    def __init__(self, tier_name, price, capacity):
        if not isinstance(tier_name, str):
            raise TypeError("Tier Name must be string")
        if not tier_name.strip():
            raise ValueError("Fill the tier name.")
        
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise TypeError("Price must be integer or float.")
        if price <= 0:
            raise ValueError("Price must be greater than 0.")
        
        if not isinstance(capacity, int) or isinstance(capacity, (float, bool)):
            raise TypeError("Capacity must be integer")
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0.")
        
        self.tier_name = tier_name.strip().title()
        self.price = float(price)
        self.capacity = capacity
        self.sold = 0
        
    def get_available_seats(self):
        return self.capacity - self.sold
    
    def __str__(self):
        return f"{self.tier_name} - ${self.price} (Available: {self.get_available_seats()}/{self.capacity})"
    
class Event:
    def __init__(self, event_code, event_name):
        if not isinstance(event_code, str):
            raise TypeError("Event code must be string")
        self.event_code = event_code.strip()
        if not (self.event_code.startswith("EVT-") and len(self.event_code[4:]) == 4 and self.event_code[4:].isdecimal()):
            raise ValueError("Wrong format.")
        
        if not isinstance(event_name, str):
            raise TypeError("Event name must be string")
        self.event_name = event_name.strip()
        if not self.event_name:
            raise ValueError("Fill the event name.")
        
        self.tiers = {}
        self.bookings = []
        
    def add_tier(self, tier):
        if not isinstance(tier, TicketTier):
            raise TypeError("Tier must be instance from TicketTier")
        for t in self.tiers:
            if tier.tier_name.lower() == t:
                raise ValueError("Tier already exists")
        self.tiers[tier.tier_name.lower()] = tier
        
    def book_tickets(self, customer_name, tier_name, quantity, discount_percent=0):
        if not isinstance(customer_name, str):
            raise TypeError("Customer name must be string")
        customer_name = customer_name.strip()
        if not customer_name:
            raise ValueError("Fill the customer name")
        
        if not isinstance(tier_name, str):
            raise TypeError("Tier name must be string")
        tier_name = tier_name.strip()
        for tier in self.tiers:
            if tier_name.lower() == tier:
                raise KeyError("Tier not found")
        
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("Quantity must be integer")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        if not isinstance(discount_percent, (int, float)) or isinstance(discount_percent, bool):
            raise TypeError("Discount must be integer or float")
        if discount_percent <= 0 or discount_percent > 50:
            raise ValueError("Discount must be between 0 - 50")
        
               
                
        
# Inisialisasi Event & Tiers
e1 = Event("EVT-2026   ", "Python Tech Summit")
t_reg = TicketTier("  Regular    ", 50.0, 100)
t_vip = TicketTier("  VIP Lounge      ", 150.0, 2)

e1.add_tier(t_reg)
e1.add_tier(t_vip)

print(e1.tiers)
