from django.db import connection

from tenant.models import Tenant


def hostname_from_request(request):
    return request.get_host().split(":")[0].lower()



# def get_tenants_map():
#     return {"thor.polls.local": "thor", "poter.polls.local": "potter"}

def get_tenants_map():
    return dict(Tenant.objects.values_list('subdomain_prefix','schema_name'))

def tenant_schema_from_request(request):
    hostname = hostname_from_request(request)
    tenants_map = get_tenants_map()
    return tenants_map.get(hostname)


def set_tenant_schema_for_request(request):
    schema = tenant_schema_from_request(request)
    with connection.cursor() as cursor:
        cursor.execute("SET search_path to {}".format(schema))



