#!/usr/bin/env python

import aerospike
import logging
from aerospike import predicates as p
import pprint


# Configure the client
config = {
  'hosts': [ ('127.0.0.1', 3000) ]
}

# Create a client and connect it to the cluster
try:
  client = aerospike.client(config).connect()
except:
  import sys
  print("failed to connect to the cluster with", config['hosts'])
  sys.exit(1)

NAMESPACE = 'test'
TABLE = 'NoSQL_HW'

def make_key(customer_id):
    return (NAMESPACE, TABLE, customer_id)

def add_customer(customer_id, phone_number, lifetime_value):
    try:
        # Make a key
        key = make_key(customer_id)
        
        # Write a record
        client.put(key, {
            'phone': phone_number,
            'ltv': lifetime_value
        })
        
        print("Row for customer {0} with phone_number {1} and lifetime_value {2} added successfully!".format(customer_id, phone_number, lifetime_value))
        
    except ex.RecordError as e:
        print("Error: {0} [{1}]".format(e.msg, e.code))
        

def get_ltv_by_id(customer_id):
    try:
        # Make a key
        key = make_key(customer_id)
        
        # Getting data by id
        (key, meta, item) = client.get(key)

        if (item == {}):
            logging.error('Requested non-existent customer ' + str(customer_id))
        else:
            return item.get('ltv')
     
    except ex.RecordError as e:
        print("Error: {0} [{1}]".format(e.msg, e.code))
        


def get_ltv_by_phone(phone_number):
    print(NAMESPACE,' ', TABLE)    
    query = client.query(NAMESPACE, TABLE)
    query.select('phone', 'ltv')
    query.where(p.equals('phone', phone_number))
    records = query.results( {'total_timeout':2000})
    print(records)
    
    
    for v in store.values():
        if (v['phone'] == phone_number):
            return v['ltv']
    logging.error('Requested phone number is not found ' + str(phone_number))

for i in range(0,1000):
    add_customer(i,i,i + 1)

        
for i in range(0,1000):
    assert (i + 1 == get_ltv_by_id(i)), "No LTV by ID " + str(i)
    assert (i + 1 == get_ltv_by_phone(i)), "No LTV by phone " + str(i)
    print("Row with index {0} getted successfully!".format(i))
    
# Closing connection
client.close()
