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
        return f"{self.tier_name} - ${self.price:.2f} (Available: {self.get_available_seats()}/{self.capacity})"
    
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
        
        tier_name = tier_name.strip().lower()
        
        if tier_name not in self.tiers:
            raise KeyError("Tier not found.")

        tier = self.tiers[tier_name]

        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise TypeError("Quantity must be integer")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        if not isinstance(discount_percent, (int, float)) or isinstance(discount_percent, bool):
            raise TypeError("Discount must be integer or float")

        if not (0 <= discount_percent <= 50):
            raise ValueError("Discount must be between 0 - 50")
        
        if quantity > tier.get_available_seats():
            return False
        
        tier.sold += quantity
        total_paid = round((quantity * tier.price) * (1 - discount_percent / 100),2)
        booking_id = f"TRX-{len(self.bookings)+1:03d}"
        
        self.bookings.append({
            "booking_id": booking_id,
            "customer": customer_name,
            "tier_key": tier_name,
            "quantity": quantity,
            "total_paid": total_paid
        })
        
        return booking_id
    
    def cancel_booking(self, booking_id, penalty_percent=20.0):
        if not isinstance(penalty_percent, (int, float)) or isinstance(penalty_percent, bool):
            raise TypeError("Penalty must be int or float")
        if not (0 <= penalty_percent <= 100):
            raise ValueError("Penalty must be between 0 - 100")
        
        for i, booking in enumerate(self.bookings):
            if booking_id.lower() == booking['booking_id'].lower():
                tier = self.tiers[booking['tier_key']]
                tier.sold -= booking['quantity']
                total_refund = round(booking['total_paid'] * (1 - penalty_percent / 100),2)
                self.bookings.pop(i)
                return float(total_refund)
        raise KeyError("Booking not found")
    
    def get_revenue(self):
        return round(sum([booking['total_paid'] for booking in self.bookings],0.0),2)
    
    def get_sold_out_tiers(self):
        return {tier.tier_name for tier in self.tiers.values() if tier.get_available_seats() == 0}
    
    def __len__(self):
        return sum(tier.sold for tier in self.tiers.values())
    
    def __str__(self):
        row = [f"EVENT: {self.event_name} ({self.event_code})"]
        if not self.tiers:
            row.append("-- No Tiers --")
        for tier in self.tiers.values():
            row.append(f"- {str(tier)}")
        row.append(f"Total Sold: {len(self)} | Revenue: ${self.get_revenue():.2f}")
        return "\n".join(row)
    
def get_top_performing_events(events: list, min_revenue):
    if not isinstance(min_revenue, (int, float)) or isinstance(min_revenue, bool):
        raise TypeError("Min. revenue must be int or float")
    if min_revenue < 0:
        raise ValueError("Min. revenue must be greater than 0")
    qualified = []
    for event in events:
        if event.get_revenue() >= min_revenue:
            qualified.append(event)
    qualified.sort(key=lambda e: (len(e), e.get_revenue()), reverse=True)
    return [event.event_code for event in qualified]
        
# Inisialisasi Event & Tiers
e1 = Event("EVT-2026   ", "Python Tech Summit")
t_reg = TicketTier("  Regular    ", 50.0, 100)
t_vip = TicketTier("  VIP Lounge      ", 150.0, 2)

e1.add_tier(t_reg)
e1.add_tier(t_vip)

print(e1.tiers)

print(e1)