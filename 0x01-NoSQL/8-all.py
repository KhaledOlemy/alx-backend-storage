#!/usr/bin/env python3
"""List all databases in mongodb"""
def list_all(mongo_collection):
    """List all dbs in mongodb"""
    return mongo_collection.find()
