class Package:
    def __init__(self, package_id, address, city, zip_code, deadline, weight, address_index, status='At the hub'):  # Constructor
        """
        Initialize a new package with given details.

        :param package_id: Unique identifier for the package.
        :param address: Delivery address of the package.
        :param city: City for the delivery address.
        :param zip_code: Zip code for the delivery address.
        :param deadline: Delivery deadline for the package.
        :param weight: Weight of the package.
        :param address_index: Index of the package's address in the distance matrix.
        :param status: Current status of the package (default is 'At the hub').
        """
        self.package_id = package_id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.address_index = address_index
        self.status = status # Current status of package
        self.delivery_time = None  # Time when the package is delivered, None if not yet delivered.
        self.is_delivered = False  # Boolean to track whether the package has been delivered.

    def update_status(self, status, delivery_time=None):
        """
        Update the status and delivery time of the package.

        :param status: New status to be assigned to the package.
        :param delivery_time: The time when the package was delivered.
        """
        self.status = status # Update status
        self.is_delivered = (status == 'Delivered') # Set 'is_delivered_ to 'True' if status is 'Delievered
        if delivery_time: # If 'delivery_time is provided
            self.delivery_time = delivery_time # Update 'delivery_time'
            self.delivery_time_formatted = delivery_time.strftime('%I:%M %p')  # Formatted delivery time.

    def __str__(self):
        """
        String representation of the package's details including delivery time.
        """
        delivery_time_formatted = self.delivery_time.strftime('%I:%M %p') if self.delivery_time else 'N/A' # Convert 'delivery_time' to string, otherwise N/A
        return (f"Package ID: {self.package_id}, Address: {self.address}, City: {self.city}, "
                f"Zip: {self.zip_code}, Deadline: {self.deadline}, Weight: {self.weight}, "
                f"Status: {self.status}, Delivery Time: {delivery_time_formatted}") # Return formatted string