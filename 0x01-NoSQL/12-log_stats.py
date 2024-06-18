#!/usr/bin/env python3
"""Status Report"""
from pymongo import MongoClient


def generate_status():
    """Generate a status report"""
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    client = MongoClient('mongodb://127.0.0.1:27017')
    targetCollection = client.logs.nginx
    nOfRequests = targetCollection.count_documents({})
    print(f"{nOfRequests} logs")
    print("Methods:")
    for method in methods:
        methodRequestCount = targetCollection.find({"method": method})
        print("\tmethod {}: {}".format(method, methodRequestCount))
    statusChecks = targetCollection.count_documents({"method": "GET", "path": "/status"})
    print(f"{statusChecks} status check")

if __name__ == "__main__":
    generate_status()
