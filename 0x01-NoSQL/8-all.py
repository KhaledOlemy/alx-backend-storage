#!/usr/bin/env python3
def list_all(mongo_collection):
    """List add dbs in mongodb"""
    return mongo_collection.find()
