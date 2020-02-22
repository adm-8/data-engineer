#!/usr/bin/env python

import logging

# import the module
import aerospike

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

### OLD Variant

store = {}

def add_customer(customer_id, phone_number, lifetime_value):
    store[customer_id] = {'phone': phone_number, 'ltv': lifetime_value}

def get_ltv_by_id(customer_id):
    item = store.get(customer_id, {})
    if (item == {}):
        logging.error('Requested non-existent customer ' + str(customer_id))
    else:
        return item.get('ltv')

def get_ltv_by_phone(phone_number):
    for v in store.values():
        if (v['phone'] == phone_number):
            return v['ltv']
    logging.error('Requested phone number is not found ' + str(phone_number))

for i in range(0,1000):
    add_customer(i,i,i + 1)

        
for i in range(0,1000):
    assert (i + 1 == get_ltv_by_id(i)), "No LTV by ID " + str(i)
    assert (i + 1 == get_ltv_by_phone(i)), "No LTV by phone " + str(i)
