#!/usr/bin/env python3
"""creates a list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """creates a list of school having a specific topic"""
    return mongo_collection.find({"topics": topic})
