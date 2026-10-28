class Crate:
    def __init__(self, crate_id, max_weight):
        if not isinstance(crate_id, str):
            raise TypeError("Crate ID must be string.")
        
        self.crate_id = crate_id.strip()
        
        if "CR-" not in self.crate_id[0:3] or not self.crate_id[3:].isnumeric():
            raise ValueError("Wrong format")
        
        if not isinstance(max_weight, (int, float)) or isinstance(max_weight, bool):
            raise TypeError("Max Weight must be integer or float.")
        
        self.max_weight = float(max_weight)

        if max_weight <= 0:
            raise ValueError("Max Weight must be greater than 0.")
        
        self.items = []
        
    def __str__(self):
        row = [f"Crate {self.crate_id} ({self.get_current_weight():.2f}/{self.max_weight:.2f} kg)"]
        if not self.items:
            row.append("-- Empty --")
        else:
            for item in self.items:
                row.append(f"- {item['name']} ({item['category']}): {item['weight']:.2f} kg")
        
        return '\n'.join(row)
   
    def get_current_weight(self):
        return float(round(sum(item['weight'] for item in self.items),2)) if self.items else 0.0
    
    def get_categories(self):
        return set(item['category'] for item in self.items)
    
    def add_item(self, name, weight, category="general"):
        if not isinstance(name, str) or not isinstance(category, str):
             raise TypeError("Name and Category must be string.")
        name = name.strip()
        category = category.strip()
        if not name or not category:
            raise ValueError("Must be fill the name and category")
        
        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            raise TypeError("Max Weight must be integer or float.")
        weight = float(weight)
        if weight <= 0:
            raise ValueError("Weight must be greater than 0.")
        
        if (self.get_current_weight() + weight) > self.max_weight:
            return False
        
        self.items.append({
            'name': name,
            'weight': weight,
            'category': category.strip().lower()
        })
        return True
    
    def remove_item(self, name):
        for i, item in enumerate(self.items):
            if name.lower() == item['name'].lower():
                return self.items.pop(i)
        raise KeyError("Item not found")
            
    
def get_overloaded_crates(crates: list, threshold_percent):
    if threshold_percent < 0 or threshold_percent > 100:
        raise ValueError("Threshold must be between 0 - 100")
    
    overtreshold = []
    
    for crate in crates:
        if (crate.get_current_weight() / crate.max_weight) * 100 >= threshold_percent:
            overtreshold.append({'crate_id': crate.crate_id, 'weight':crate.max_weight}, 'percent': )
    
    overtreshold.sort(key=lambda item: item['weight'], reverse=True)
    output = [item['crate_id'] for item in overtreshold]
    return output