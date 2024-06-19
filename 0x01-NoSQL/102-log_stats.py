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
        methodRequestCount = len(list(targetCollection.find(
            {"method": method})))
        print("\tmethod {}: {}".format(method, methodRequestCount))
    statusChecks = targetCollection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{statusChecks} status check")
    print("IPs:")
    listOfIPs = [ip['ip'] for ip in targetCollection.find(
        {"ip": {"$regex": "^(\d+(\.|$)){4}"}})]  # noqa
    outputIPs = {}
    for ip in listOfIPs:
        if ip in outputIPs.keys():
            outputIPs[ip] += 1
        else:
            outputIPs[ip] = 1
    top10 = sorted(list(outputIPs.values()), reverse=True)[:10]
    target = []
    for k, v in outputIPs.items():
        if v in top10:
            target.append({k: v})
    target = sorted(target, key=lambda i: list(i.values())[0], reverse=True)
    for item in target:
        print(f"\t{list(item.keys())[0]}: {list(item.values())[0]}")


if __name__ == "__main__":
    generate_status()
