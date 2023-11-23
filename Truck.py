# Truck.py

from datetime import datetime, timedelta

class Truck:
    def __init__(self, truck_id, delivery_speed=18, capacity=16):  # Constructor
        self.truck_id = truck_id # Initialize truck ID
        self.delivery_speed = delivery_speed  # Speed of the truck in miles per hour
        self.capacity = capacity  # Maximum number of packages the truck can carry
        self.packages = []  # List to store packages loaded onto the truck
        self.total_miles = 0  # Total miles traveled by the truck
        self.current_location_index = 0  # Assuming index 0 is the hub
        self.current_time = datetime.strptime('08:00 AM', '%I:%M %p')  # Default starting time

    def load_package(self, package):
        """Load a package onto the truck if there's available capacity."""
        if len(self.packages) < self.capacity: # Check if number of 'packages' is less than trucks 'capacity'
            self.packages.append(package) # Add 'package' to 'packages'
            package.update_status('En Route')  # Update package status to 'En Route'
        else:  # If truck is full
            print(f"Truck {self.truck_id} is full and cannot load any more packages.") # Print full statement

    def deliver_package(self, package, distance):
        """Deliver a package and update truck's total mileage and time."""
        # Ensure package #9 is not delivered before 10:20 AM
        update_time = datetime.strptime('10:20 AM', '%I:%M %p') # Initialize 'update_time'
        if package.package_id == 9 and self.current_time < update_time: # Check if package #9 and before 10:20 AM
            print("Package #9 cannot be delivered before 10:20 AM. It will be reattempted later.") # Print unsuccessful delivery message
            return False  # Delivery attempt was unsuccessful

        # Print the distance being used for delivery
        print(f"Delivering package {package.package_id} from location index {self.current_location_index} to {package.address_index}. Distance: {distance} miles.")

        # Calculate delivery time based on distance
        delivery_time = self.current_time + timedelta(hours=distance / self.delivery_speed)
        package.update_status('Delivered', delivery_time)  # Update package status to 'Delivered'
        self.total_miles += distance  # Update total miles
        self.current_location_index = package.address_index  # Update current location
        self.current_time = delivery_time  # Update current time
        return True  # Delivery was successful

    def return_to_hub(self, distance_matrix):
        """Simulate the truck's return to the hub and update its mileage."""
        return_distance = distance_matrix[self.current_location_index][0] # Calculate 'return_distance'
        self.total_miles += return_distance  # Update total miles for the return trip
        self.current_location_index = 0  # Reset location to the hub
        self.current_time += timedelta(hours=return_distance / self.delivery_speed)  # Calculate and update 'current_time'
        print(f"Truck {self.truck_id} returning to hub, total miles: {self.total_miles}") # Print return message

    def __str__(self):
        """String representation of the truck's current package load."""
        return f"Truck {self.truck_id} -> Packages: {[p.package_id for p in self.packages]}" # Create and return formatted string