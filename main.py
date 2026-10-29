# class Crate:
#     def __init__(self, crate_id, max_weight):
#         if not isinstance(crate_id, str):
#             raise TypeError("Crate ID must be string.")
        
#         self.crate_id = crate_id.strip()
        
#         if "CR-" not in self.crate_id[0:3] or not self.crate_id[3:].isnumeric():
#             raise ValueError("Wrong format")
        
#         if not isinstance(max_weight, (int, float)) or isinstance(max_weight, bool):
#             raise TypeError("Max Weight must be integer or float.")
        
#         self.max_weight = float(max_weight)

#         if max_weight <= 0:
#             raise ValueError("Max Weight must be greater than 0.")
        
#         self.items = []
        
#     def __str__(self):
#         row = [f"Crate {self.crate_id} ({self.get_current_weight():.2f}/{self.max_weight:.2f} kg)"]
#         if not self.items:
#             row.append("-- Empty --")
#         else:
#             for item in self.items:
#                 row.append(f"- {item['name']} ({item['category']}): {item['weight']:.2f} kg")
        
#         return '\n'.join(row)
   
#     def get_current_weight(self):
#         return float(round(sum(item['weight'] for item in self.items),2)) if self.items else 0.0
    
#     def get_categories(self):
#         return set(item['category'] for item in self.items)
    
#     def add_item(self, name, weight, category="general"):
#         if not isinstance(name, str) or not isinstance(category, str):
#              raise TypeError("Name and Category must be string.")
#         name = name.strip()
#         category = category.strip()
#         if not name or not category:
#             raise ValueError("Must be fill the name and category")
        
#         if not isinstance(weight, (int, float)) or isinstance(weight, bool):
#             raise TypeError("Max Weight must be integer or float.")
#         weight = float(weight)
#         if weight <= 0:
#             raise ValueError("Weight must be greater than 0.")
        
#         if (self.get_current_weight() + weight) > self.max_weight:
#             return False
        
#         self.items.append({
#             'name': name,
#             'weight': weight,
#             'category': category.strip().lower()
#         })
#         return True
    
#     def remove_item(self, name):
#         for i, item in enumerate(self.items):
#             if name.lower() == item['name'].lower():
#                 return self.items.pop(i)
#         raise KeyError("Item not found")
            
    
# def get_overloaded_crates(crates: list, threshold_percent):
#     if threshold_percent < 0 or threshold_percent > 100:
#         raise ValueError("Threshold must be between 0 - 100")
    
#     overtreshold = []
    
#     for crate in crates:
#         if (crate.get_current_weight() / crate.max_weight) * 100 >= threshold_percent:
#             overtreshold.append({
#                 'crate_id': crate.crate_id,
#                 'percent': (crate.get_current_weight() / crate.max_weight) * 100
#             })
    
#     overtreshold.sort(key=lambda item: item['percent'], reverse=True)
#     output = [item['crate_id'] for item in overtreshold]
#     return output

# ------------------------------------------------------    
class TicketTier:
    def __init__(self, tier_name, price, capacity):
        if not isinstance(tier_name, str):
            raise TypeError("Tier Name must be string")
        if not tier_name.strip():
            raise ValueError("Fill the tier name")
        
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise ValueError("Price must be integer/float.")
        if price < 0:
            raise ValueError("Price must be greater than 0")
        
        if not isinstance(capacity, int) or isinstance(capacity, (float, bool)):
            raise TypeError("Capacity must be integer.")
        if capacity < 0:
            raise ValueError("Price must be greater than 0")
        
        self.tier_name = tier_name.title()
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
            raise TypeError("Event Code must be string")
        
        self.event_code = event_code.strip()
        
        if not self.event_code.startswith("EVT-") or len(self.event_code[3:]) == 4 or self.event_code[3:].isdecimal():
            raise ValueError("The Event Code is not in the correct format.")
        
        if not isinstance(event_name, str):
            raise TypeError("Event Name must be string")
        
        self.event_name = event_name.strip()
        
        if not self.event_name:
            raise ValueError("Fill the Event Name.")
        
        self.tiers = {}
        self.bookings = []
        
    def add_tier(self, tier):
        if not isinstance(tier, TicketTier):
            raise TypeError("A Tier is not an instance of a Ticket Tier.")
        for t in self.tiers.values():
            if tier.tier_name.lower() == t.lower:
                raise ValueError("Tier already exists")
        
        
        
    def book_tickets(self, customer_name, tier_name, quantity, discount_percent = 0.0):
        if not isinstance(customer_name, str):
            raise TypeError("Customer Name must be string.")
        customer_name = customer_name.strip()
        if not customer_name:
            raise ValueError("Fill the Customer Name.")
        
        if not isinstance(tier_name, str):
            raise TypeError("Tier Name must be string.")
        tier_name = tier_name.strip()
        
