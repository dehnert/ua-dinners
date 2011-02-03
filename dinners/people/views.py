from django.forms import Form, EmailField
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

import ldap
import ldap.filter

class EmailForm(Form):
    email = EmailField()

def ldap_get_filter_from_dict(filter_dict):
    filter_list = filter_dict.items()
    tmplstr = "(&"
    for key, value in filter_list:
        tmplstr += "(" + key + "=%s)"
    tmplstr += ")"
    values = [value for key,value in filter_list]
    filterstr = ldap.filter.filter_format(tmplstr, values)
    print filterstr, filter_dict
    return filterstr

def get_ldap_data(filterstr, fields):
    con = ldap.open('ldap.mit.edu')
    con.simple_bind_s("", "")
    dn = "dc=mit,dc=edu"
    result = con.search_s('dc=mit,dc=edu', ldap.SCOPE_SUBTREE, filterstr, fields)
    if len(result) > 0:
        ret = {}
        for key in result[0][1]:
            ret[key] = result[0][1][key][0]
        return True, ret
    else:
        return False, "No results found"

def search_person(http_request, ):
    data = {}
    error = None
    if 'email' in http_request.GET:
        form = EmailForm(http_request.GET)
        if form.is_valid():
            email = form.cleaned_data['email']
            filterstr = ldap_get_filter_from_dict({'mail':email})
            fields = ['mail', 'cn', 'ou', 'uid', ]
            success, data = get_ldap_data(filterstr, fields)
            if success:
                pass
            else:
                error = data
                data = None
    else:
        form = EmailForm()

    context = {
        'form': form,
        'error': error,
        'data': data,
        'pagename': 'search',
    }
    return render_to_response('people/search.html', context, context_instance=RequestContext(http_request), )
