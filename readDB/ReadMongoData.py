# This program needed to connect to MongoDB for TravelExperts hosted on Atlas
# It has functions to get the data from different tables/collections
# If the Online DB is not accessible, you need to host it on Atlas.
# Create and Atlas account https://cloud.mongodb.com/ and add a username and open network IP address
# Configure your username and passwork below
# You can get the cluster URL from Atlas. On the cluster check the connection instructions (click connect)

# pip install pymongo dnspython

from pymongo import MongoClient
import pandas as pd

DB_USERNAME = "gacasti"
DB_PASSWORD = "1234321"
DB_CLUSTER_URL = "cluster0.jg6vs.mongodb.net"

# Connect the MongoDB
# ======================
# Making a Connection with MongoClient
client = MongoClient(
    f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CLUSTER_URL}")
# database
db = client["travelexperts"]


def getBookingDetails():
    # collection
    bookingdetails_table = db["bookingdetails"].find({})
    bookingdetails = pd.DataFrame(bookingdetails_table)
    bookingdetails.set_index("_id", inplace=True)
    return bookingdetails


def getBookings():
    bookings_table = db["bookings"].find({})
    bookings = pd.DataFrame(bookings_table)
    bookings.set_index("_id", inplace=True)
    return bookings


# bookings_with_details = pd.merge(bookings, bookingdetails, on="BookingId")
# print(bookings_with_details)


def getAgents():
    agents_table = db["agents"].find({})
    agents = pd.DataFrame(agents_table)
    agents.set_index("_id", inplace=True)
    return agents


def getFees():
    fees_table = db["fees"].find({})
    fees = pd.DataFrame(fees_table)
    fees.set_index("_id", inplace=True)
    return fees


def getRegions():
    regions_table = db["regions"].find({})
    regions = pd.DataFrame(regions_table)
    regions.set_index("_id", inplace=True)
    return regions


def getClasses():
    classes_table = db["classes"].find({})
    classes = pd.DataFrame(classes_table)
    classes.set_index("_id", inplace=True)
    return classes


def getProductsSuppliers():
    products_suppliers_table = db["products_suppliers"].find({})
    products_suppliers = pd.DataFrame(products_suppliers_table)
    products_suppliers.set_index("_id", inplace=True)
    return products_suppliers


def getSuppliers():
    suppliers_table = db["suppliers"].find({})
    suppliers = pd.DataFrame(suppliers_table)
    suppliers.set_index("_id", inplace=True)
    return suppliers


def getProducts():
    products_table = db["products"].find({})
    products = pd.DataFrame(products_table)
    products.set_index("_id", inplace=True)
    return products


def getCustomers():
    customers_table = db["customers"].find({})
    customers = pd.DataFrame(customers_table)
    customers.set_index("_id", inplace=True)
    return customers


# Data collections
myBookingsDetails = getBookingDetails()
myBookings = getBookings()
myProductSuppliers = getProductsSuppliers()
mySuppliers = getSuppliers()
myRegions = getRegions()
myClass = getClasses()
myAgents = getAgents()
myCustomers = getCustomers()

# Dataset for: bookings, bookingDetails, supplier, and productSupplier
bookings_with_details = pd.merge(myBookings, myBookingsDetails, on="BookingId")
bookings_with_details_and_prod_supplier = pd.merge(bookings_with_details,
                                                   myProductSuppliers,
                                                   on="ProductSupplierId")
booking_sales_by_supplier = pd.merge(bookings_with_details_and_prod_supplier,
                                     mySuppliers,
                                     on="SupplierId")
booking_sales_by_supplier_by_region = pd.merge(booking_sales_by_supplier,
                                               myRegions,
                                               on="RegionId")

booking_sales_by_customer = pd.merge(bookings_with_details,
                                     myCustomers,
                                     on="CustomerId")
booking_sales_by_customer_by_agent = pd.merge(booking_sales_by_customer,
                                              myAgents,
                                              on="AgentId")

booking_sales_by_region_by_agent = pd.merge(booking_sales_by_customer_by_agent,
                                            myRegions,
                                            on="RegionId")

# Dataset for: bookings, bookingDetails, agent, and class

print(booking_sales_by_region_by_agent)