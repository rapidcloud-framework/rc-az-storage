import json
import os
import pprint
import sys
import requests
import ipaddress
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from azure.identity import DefaultAzureCredential
from azure.identity import AzureAuthorityHosts
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient

def get_locations():
    # Acquire a credential object using CLI-based authentication.
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()

    subs_client = SubscriptionClient(credential)
    entities = subs_client.subscriptions.list_locations(subscription_id)

    locations = []

    for location in list(entities):
        output_dict = {}
        label = f"{location.display_name}"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = location.name
        locations.append(output_dict)
    return locations

def pp(d):
    print(pprint.pformat(d))

def get_resource_groups(params):
    # Acquire a credential object using CLI-based authentication.
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)
    group_list = resource_client.resource_groups.list()
    resource_groups = []
    sorted_entities = sorted(group_list, key=lambda x: x.name.lower(), reverse=False)
    rc_rgs = list(filter(lambda x: x.tags is not None and x.tags.get('profile') is not None and x.tags.get('profile') == params.get('env') ,sorted_entities))
    other_rgs = list(filter((lambda x: x.tags is None) ,sorted_entities))
    additional_rgs = list(filter((lambda x: x.tags is not None and x.tags.get('profile') is None) ,sorted_entities))

    final_list = rc_rgs + other_rgs + additional_rgs
    
    # for item in list(final_list):
    #     print(item.name)

    #sorted_entities = sorted(group_list, key=lambda x: x.name.lower(), reverse=False)
    for group in list(final_list):
        output_dict = {}
        is_rc = ""
        if not group.tags:
            label = f"{group.name} ({group.location})"
        else:
            if group.tags is not None:
                if group.tags.get('profile') is not None:
                    if group.tags.get('profile').lower() == params.get('env').lower():
                        is_rc = "value"
            if is_rc == '':
                label = f"{group.name} ({group.location})"
            else:
                label = f"{group.name} ({group.location}) (Managed by Rapid Cloud)"
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = group.name
        output_dict['value']['scope'] = group.id
        resource_groups.append(output_dict)
    return resource_groups

def get_storage_accounts():
    SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", None)
    storage_client  = StorageManagementClient(credential=DefaultAzureCredential(), subscription_id=SUBSCRIPTION_ID)
    storage_accounts  =  storage_client.storage_accounts.list()

    accounts = []
    
    for sa in list(storage_accounts):
        output_dict = {}
        label = sa.name
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = label
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = sa.name
        accounts.append(output_dict)
    return accounts

def get_subnets():
    # Acquire a credential object using CLI-based authentication.
    SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", None)
    network_client = NetworkManagementClient(credential=DefaultAzureCredential(), subscription_id=SUBSCRIPTION_ID)
    vnets = network_client.virtual_networks.list_all()

    subnets = []

    for vnet in list(vnets):
        for subnet in vnet.subnets:
            output_dict = {}
            label = f"{vnet.name} - {subnet.name} ({subnet.address_prefix})"
            output_dict['value'] = {}
            output_dict['type'] = "Theia::Option"
            output_dict['label'] = label
            output_dict['value']['type'] = "Theia::DataOption"
            output_dict['value']['value'] = subnet.id
            subnets.append(output_dict)
    return subnets

def get_managed_identities():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    token = get_new_token()
    api_call_headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.ManagedIdentity/userAssignedIdentities?api-version=2023-01-31",
                            headers=api_call_headers, verify=False)
    
    identities = []

    response2 = json.loads(response.text)
    for identity in response2['value']:
        output_dict = {}
        output_dict['value'] = {}
        output_dict['type'] = "Theia::Option"
        output_dict['label'] = identity['name']
        output_dict['value']['type'] = "Theia::DataOption"
        output_dict['value']['value'] = identity['id']
        identities.append(output_dict)
    return identities

def get_new_token():
    tokenCredential = DefaultAzureCredential()
    scope = "https://management.core.windows.net/.default"
    access_token = tokenCredential.get_token(scope)
    return access_token.token

def get_new_token_old():
    tenant_id = os.environ["AZURE_TENANT_ID"]
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]

    token_req_payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'resource': 'https://management.azure.com/'
        }

    auth_server_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
    token_response = requests.post(auth_server_url, data=token_req_payload, verify=False, allow_redirects=False)
    
    if token_response.status_code !=200:
            print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
            sys.exit(1)

    tokens = json.loads(token_response.text)
    return tokens['access_token']


def custom_endpoint(action, params, boto3_session, user_session):
    if action == "resourcegroups":
        return get_resource_groups(params)
    elif action == "subnets":
        return get_subnets()
    elif action == "locations":
        return get_locations()
    elif action == "managedidentities":
        return get_managed_identities()
    elif action == "storage_accounts":
        return get_storage_accounts()
    else:
        pp(f"no such endpoint: {action}")
        return ["no such endpoint"]

    return []