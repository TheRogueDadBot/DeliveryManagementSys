# Main.py
# Author: Eric Jacobs
# Student ID: 010580832
# Title: C950 WGUPS Routing Program

import csv
from datetime import datetime, timedelta
from HashTable import HashTable
from Package import Package
from Truck import Truck

# Constants for CSV file paths
CSV_DIRECTORY = '/Users/ericjacobs/Desktop/Software I/Project/C950/CSV/'

def load_address_data(filename):
    """Load address data from CSV file to create a mapping of address to index."""
    address_index_map = {} # Initialize empty library
    with open(filename) as csvfile: # Temporary refer to file as 'csvfile' within 'with' block
        address_reader = csv.reader(csvfile) # Creates CSV reader object to read from 'csvfile'
        for index, row in enumerate(address_reader):# Iterate over each row in CSV file
            address = row[2].strip() #Extract 'address' from third row
            address_index_map[address] = index # Map 'address' to to 'index'
    # Print the address_index_map
    """print("Address Index Map:")
    for address, index in address_index_map.items():
        print(f"{address}: {index}")"""
    return address_index_map

def load_package_data(filename, hash_table, address_index_map): # address_index_map is created in load_address_data funciton
    """Load package data from CSV file and insert into the hash table."""
    with open(filename) as csvfile:  # 'with' makes sure file closes after execution
        package_reader = csv.reader(csvfile) # Creates CSV reader object to read from 'csvfile'
        for row in package_reader:  # Iterate over each row in CSV file
            package_id = int(row[0]) # Assign first column of CSV fil as package_id
            full_address = row[1].strip() # Retrieve address.  strip() removes whitespace 
            address_index = address_index_map.get(full_address) # Use 'full address' to to find index in 'address index map'
            if address_index is None:  # Error tracking
                print(f"Error: Address '{full_address}' not found for package {package_id}.")
                continue
            package_data = Package(package_id, row[1], row[2], row[4], row[5], row[6], address_index, 'At Hub') # Create Paackage data object
            hash_table.insert(package_id, package_data) # Insert package data into hash table

def load_distance_data(filename):
    """Load distance data from CSV file."""
    distances = [] # Initialize empty list
    with open(filename) as csvfile: # Open file as 'csvfile'
        distance_reader = csv.reader(csvfile) # Open CSV reader object
        for row_index, row in enumerate(distance_reader): # Iterate over each row
            # Convert each element to float and handle empty strings
            processed_row = [float(dist.strip()) if dist.strip() else 0.0 for dist in row] # Process each row
            distances.append(processed_row) # Add row to 'distances' list
            #Debugging
            '''print(f"Raw row {row_index}: {row}")
            print(f"Processed row {row_index}: {processed_row}")'''

    # Mirror the lower triangular part to the upper part
    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            distances[i][j] = distances[j][i]

    #Debugging
    '''print("\nComplete Distance Matrix:")
    for row in distances:
        print(row)'''

    return distances

def find_nearest_neighbor(current_location, packages, distance_matrix):
    """Find the nearest unvisited address for delivery."""
    nearest_distance = float('inf') #Initialize to infinitly large value
    nearest_package = None # Initiate 'nearest_package to 'None'
    for package in packages: #Iterate over packages
        package_location = package.address_index # Retrieve 'address_index' from current 'package'
        distance_to_package = distance_matrix[current_location][package_location] # Calculate distance to package
        if distance_to_package < nearest_distance and not package.is_delivered: # Set conditions
            nearest_distance = distance_to_package # Set new 'nearest_distance'
            nearest_package = package # Set new 'nearest_package'
    return nearest_package, nearest_distance # Return updated values

def load_packages_onto_trucks(trucks, hash_table):
    """Manually load packages onto specified trucks."""
    # Packages assignment for each truck
    truck_packages = { 
        1: [1, 14, 16, 15, 29, 30, 31, 34, 37, 40, 19, 20, 13, 4, 8, 10],
        2: [3, 18, 36, 38, 2, 11, 39, 25, 6],
        3: [9, 32, 28, 5, 7, 12, 17, 21, 22, 23, 24, 26, 27, 33, 35]
    } #Create a dictionary where truck ID is key and values are packages

    for truck_id, package_ids in truck_packages.items(): # Iterate over 'truck_packages' dictionary
        for package_id in package_ids: # Iterate over each 'package_id' in 'package_ids'
            package = hash_table.lookup(package_id) # Look up 'package' in 'hash_table' using 'package_id'
            if package: # If package is found
                trucks[truck_id - 1].load_package(package) # Load package.  Truck index starts at 0

def simulate_truck_delivery(truck, hash_table, distance_matrix, address_index_map):
    """Simulate delivery for a single truck."""
    current_location = 0  # Start from the hub
    high_priority_packages = [6, 25]  # List of high-priority packages

    # Deliver high-priority packages first if they are on the truck
    for package_id in high_priority_packages:
        package = next((p for p in truck.packages if p.package_id == package_id), None)
        if package and not package.is_delivered:
            distance_to_package = distance_matrix[current_location][package.address_index]
            truck.deliver_package(package, distance_to_package)
            # Debugging
            print(f"Delivering high-priority package {package.package_id} from location index {current_location} to {package.address_index}. Distance: {distance_to_package} miles.")
            current_location = package.address_index
            truck.packages.remove(package)  # Remove delivered package from truck

    # Continue with regular delivery for remaining packages
    while truck.packages:
        nearest_package, distance_to_package = find_nearest_neighbor(current_location, truck.packages, distance_matrix)
        if nearest_package:
            # Debugging
            print(f"Delivering package {nearest_package.package_id} from location index {current_location} to {nearest_package.address_index}. Distance: {distance_to_package} miles.")
            truck.deliver_package(nearest_package, distance_to_package)
            current_location = nearest_package.address_index
        else:
            break

    # Calculate the distance from the last delivery location back to the hub
    distance_to_hub = distance_matrix[current_location][0]  # Assuming the hub is at index 0
    truck.total_miles += distance_to_hub
    print(f"Truck {truck.truck_id} returning to hub from location index {current_location}. Distance: {distance_to_hub} miles.")

def simulate_delivery(trucks, hash_table, distance_matrix, address_index_map):
    """Simulate the delivery process for all trucks."""
    truck_2_departure_time = datetime.strptime('09:10 AM', '%I:%M %p') # Initiate 'truck_2_departure_time'
    truck_3_departure_time = datetime.strptime('10:30 AM', '%I:%M %p') # Initiate 'truck_3_departure_time'
    start_time = datetime.strptime('08:00 AM', '%I:%M %p') # Inititate 'start_time' for other trucks.  Convert string to 'datetime' object
    trucks[0].current_time = start_time # Assign 'start_time'
    trucks[1].current_time = truck_2_departure_time # Set 'current_time' to 9:10 AM
    trucks[2].current_time = truck_3_departure_time # Set 'current_time' to 10:30 AM
    simulate_truck_delivery(trucks[0], hash_table, distance_matrix, address_index_map) # Simulate delivery truck 1
    simulate_truck_delivery(trucks[1], hash_table, distance_matrix, address_index_map) # Simulate delivery truck 2
    simulate_truck_delivery(trucks[2], hash_table, distance_matrix, address_index_map) # Simulate delivery truck 3

def display_all_package_statuses(hash_table):
    """Display the status of all packages."""
    for package_id in range(1, 41): # Loop through package IDs
        package = hash_table.lookup(package_id) # Look up each package.  Returns object.
        if package: # Check if package is found
            print(str(package)) # Print package information as a string
        else: # If package doesn't exist
            print(f"Package ID {package_id} not found.") # Print not found message

def display_truck_info(trucks):
    """Display information about each truck."""
    for truck in trucks: # Iterate through each 'truck' in 'trucks' list
        print(f"Truck {truck.truck_id} -> Return Time: {truck.current_time.strftime('%I:%M %p')}, Total Mileage: {truck.total_miles}, Packages: {[p.package_id for p in truck.packages]}") # Print information

def check_package_status(package_id, hash_table):
    """Check the status of a specific package."""
    package = hash_table.lookup(package_id) # Look up package.
    if package: # Check if package exists
        return str(package) # Return package information as a string
    else: # If package doesn't exist
        return f"No package found with ID {package_id}" # Print no package found message

def calculate_package_delivery_times(trucks, distance_matrix):
    """Calculate the delivery times for all packages."""
    for truck in trucks: # Iterate over each 'truck' in 'trucks list
        current_time = truck.current_time # Set 'current_time'
        current_location = 0 # Set 'current_location' to hub
        for package in truck.packages: # Initiate nested loop that iterates over each 'package' in 'truck'
            package_location = package.address_index # Retrieve 'address_index' and set as 'package_location'
            travel_time = calculate_delivery_time(distance_matrix[current_location][package_location]) # Calculate travel time to package
            current_time += timedelta(minutes=travel_time) # Add 'travel_time' to 'current_time'
            package.delivery_time = current_time # Set package's delivery time
            current_location = package_location # Update current location

def calculate_delivery_time(distance):
    """Calculate delivery time in minutes given a distance."""
    speed = 18  # Truck speed in miles per hour
    return (distance / speed) * 60 # Calculate and return delivery time

def display_package_status_at_time(hash_table, specific_time):
    """Display the status of all packages at a specific time."""
    for package_id in range(1, 41): # Iterate through package IDs
        package = hash_table.lookup(package_id) # Look up 'package-id', set as 'package'
        if package: # Check if package is found
            status = "At Hub" # Initial status assignment
            if package.delivery_time: # Check for delivery time
                if package.delivery_time <= specific_time: # If 'delivery_time' is less or equal to 'specific-time'
                    status = f"Delivered at {package.delivery_time.strftime('%I:%M %p')}" # Update status
                else: # If 'delivery_time' is greater than 'specific_time'
                    status = "En Route" # Set status
            address = package.address # Retrieve address
            deadline = package.deadline    
            print(f"Package ID: {package_id}, Status: {status}, Deadline: {deadline} Address: {address}") # Print package information
        else: # If no package is found
            print(f"Package ID {package_id} not found.") # Print not found message

def main():
    """Main function to execute the program."""
    package_hash_table = HashTable() # Create hash table instance
    address_index_map = load_address_data(CSV_DIRECTORY + 'Address.csv') # Load address data
    load_package_data(CSV_DIRECTORY + 'Package.csv', package_hash_table, address_index_map) # Load package data
    distance_matrix = load_distance_data(CSV_DIRECTORY + 'Distance.csv') # Load distance data
    #Debugging
    """print("Complete Distance Matrix:")
    for row in distance_matrix:
        print(row)"""
    truck1, truck2, truck3 = Truck(1), Truck(2), Truck(3) # Create truck instances
    trucks = [truck1, truck2, truck3] # Create truck list
    load_packages_onto_trucks(trucks, package_hash_table) # Load packages onto trucks
    calculate_package_delivery_times(trucks, distance_matrix) # Calculate package delivery times
    simulate_delivery(trucks, package_hash_table, distance_matrix, address_index_map) # Simulate package deliver

    while True: # Infinite loop
        print("\nOptions:\n1. Check Package Status\n2. Display All Package Statuses\n3. Display Truck Information\n4. Display Total Mileage\n5. Exit") # Print options to user
        choice = input("Enter your choice: ") # Ask user for input choice
        if choice == '1': # Option 1: Check package status
            package_id_input = input("Enter package ID to check status: ") # Ask user for package ID
            if package_id_input.isdigit(): # Check for only digits
                package_id = int(package_id_input) # Convert 'package_id_input' to int, then store as 'package_id
                package = package_hash_table.lookup(package_id) # Look up package object
                if package: # Check if package is found
                    # Display all details of the found package
                    print(f"Package ID: {package.package_id}")
                    print(f"Address: {package.address}")
                    print(f"City: {package.city}")
                    print(f"Zip Code: {package.zip_code}")
                    print(f"Deadline: {package.deadline}")
                    print(f"Weight: {package.weight}")
                    print(f"Status: {package.status}")
                    if package.delivery_time: # Check if delivery time is available
                        print(f"Delivery Time: {package.delivery_time.strftime('%I:%M %p')}") # Print delivery time
                    else: # If delivery is unavailable
                        print("Delivery Time: N/A") # Print N/A
                else: # If package # is not found
                    print(f"No package found with ID {package_id}") # Print no package found
            else: # If not digit
                print("Invalid input. Please enter a numeric package ID.") # Print invalid input message
        elif choice == '2': # Option 2: Display all package statuses at a specific time
            time_input = input("Enter the time (HH:MM AM/PM) to check package statuses: ") # Request time input
            try: # Create a try block
                specific_time = datetime.strptime(time_input, '%I:%M %p') # Parse user's input into 'datetime' object
                display_package_status_at_time(package_hash_table, specific_time) # If parse is successful, display statues of all packages at given time
            except ValueError: # Catch error if parse is unsuccessful
                print("Invalid time format. Please enter time in HH:MM AM/PM format.") # Print invalid format message
        elif choice == '3': # Option 3: Display truck information
            display_truck_info(trucks) # Display truck information
        elif choice == '4': # Option 4: Display total mileage
            total_mileage = sum(truck.total_miles for truck in trucks) # Calculate 'total_milage'
            print(f"Total mileage by all trucks: {total_mileage}") # Print total mileage
        elif choice == '5': # Option 5: Exit the program
            print("Exiting program.") # Print exit message
            break # Terminate 'while True' loop
        else: # If input is not 1-5
            print("Invalid choice. Please enter a number between 1 and 5.") # Print input error message

if __name__ == "__main__":
    main()