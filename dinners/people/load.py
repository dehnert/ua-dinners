#!/usr/bin/python

import sys
import os

if __name__ == '__main__':
    cur_file = os.path.abspath(__file__)
    django_dir = os.path.abspath(os.path.join(os.path.dirname(cur_file), '..'))
    proj_dir = os.path.abspath(os.path.join(django_dir, '..'))
    sys.path.append(django_dir)
    sys.path.append(proj_dir)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import people.models

import datetime
import json

fields = [
    # Django field       Input field
    ('krb_name'        , 'KRB_NAME'),
    ('office_location' , 'OFFICE_LOCATION' ),
    ('first_name'      , 'FIRST_NAME'      ),
    ('year'            , 'YEAR'            ),
    ('unit_name'       , 'UNIT_NAME'       ),
    ('last_name'       , 'LAST_NAME'       ),
]
def load_people(them):
    django_people = people.models.AthenaPerson.objects.all()
    stat_changed = 0
    stat_mut_ign = 0
    stat_unchanged = 0
    stat_del = 0
    stat_pre_del = 0
    stat_add = 0
    stat_pt_created = 0
    for django_person in django_people:
        mutable = django_person.person_type.mutable
        if django_person.krb_name in them:
            # great, they're still in the dump
            changed = False
            ware_person = them[django_person.krb_name]
            del them[django_person.krb_name]
            if django_person.person_type.name != ware_person['PERSON_TYPE']:
                changed = True
                if mutable:
                    django_person.person_type, pt_created = people.models.PersonType.objects.get_or_create(name=ware_person['PERSON_TYPE'])
                    if pt_created:
                        stat_pt_created += 1
            for dp_key, w_key in fields:
                if django_person.__dict__[dp_key] != ware_person[w_key]:
                    changed = True
                    if mutable:
                        django_person.__dict__[dp_key] = ware_person[w_key]
            if changed:
                if mutable:
                    django_person.mod_date = datetime.date.today()
                    django_person.save()
                    stat_changed += 1
                else:
                    stat_mut_ign += 1
            else:
                stat_unchanged += 1
        else:
            if django_person.del_date is None:
                if mutable:
                    django_person.del_date = datetime.date.today()
                    stat_del += 1
                    django_person.save()
                else:
                    stat_mut_ign += 1
            else:
                stat_pre_del += 1
    for krb_name, ware_person in them.items():
        django_person = people.models.AthenaPerson()
        django_person.person_type, pt_created = people.models.PersonType.objects.get_or_create(name=ware_person['PERSON_TYPE'])
        if pt_created:
            stat_pt_created += 1
        for dp_key, w_key in fields:
            django_person.__dict__[dp_key] = ware_person[w_key]
        django_person.add_date = datetime.date.today()
        stat_add += 1
        django_person.save()
    stats = {
        'changed': stat_changed,
        'mut_ign': stat_mut_ign,
        'unchanged': stat_unchanged,
        'del': stat_del,
        'pre_del': stat_pre_del,
        'add': stat_add,
        'pt_created': stat_pt_created,
    }
    return stats


if __name__ == '__main__':
    them = json.loads(sys.stdin.read())
    stats = load_people(them)
    print """
Changed:            %(changed)6d
Change ignored:     %(mut_ign)6d
Unchanged:          %(unchanged)6d
Deleted:            %(del)6d
Already Deleted:    %(pre_del)6d
Added:              %(add)6d
PeopleType created: %(pt_created)6d""" % stats
