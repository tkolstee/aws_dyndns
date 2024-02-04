#!/usr/bin/env python

import dotenv
import requests
import ipaddress
import boto3
import json

def get_curr_ip():
    r = requests.get('https://api.ipify.org/')
    r.raise_for_status()
    ip_str = r.content.decode().strip()
    current_ip = ipaddress.ip_address(ip_str)
    return current_ip

def get_records(zoneid, record, client):
    response = client.list_resource_record_sets(
        HostedZoneId=zoneid,
        StartRecordName=record,
        StartRecordType='A'
    )
    recordset = response['ResourceRecordSets'][0]
    if recordset['Name'] != record:
        raise KeyError(f"Record {record} not found!")
    reg_ip = ipaddress.ip_address(recordset['ResourceRecords'][0]['Value'])
    return reg_ip, recordset

cfg = dotenv.dotenv_values()
current_ip = get_curr_ip()
print(f"My IP is {current_ip}")

client = boto3.client(
    'route53', 
    aws_access_key_id=cfg['AWS_ACCESS_KEY'], 
    aws_secret_access_key=cfg['AWS_SECRET_KEY']
)
reg_ip, recordset = get_records(cfg['ZONEID'], cfg['RECORD'], client)
print(f"Registered IP is {reg_ip}")

if not current_ip == reg_ip:
    recordset['ResourceRecords'][0]['Value'] = str(current_ip)
    req = {
        'HostedZoneId': cfg['ZONEID'],
        'ChangeBatch': {
            'Comment': f"Dynamic DNS update of {cfg['RECORD']}",
            'Changes': [{ 'Action': 'UPSERT', 'ResourceRecordSet': recordset }]
        }
    }
    print(req)
    resp = client.change_resource_record_sets(**req)




