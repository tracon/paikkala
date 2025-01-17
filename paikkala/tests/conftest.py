from datetime import timedelta

import pytest
from django.test import Client
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from paikkala.models import Program, Room, Row, Zone
from paikkala.tests.demo_data import import_sibeliustalo_zones, create_jussi_program


@pytest.fixture
def sibeliustalo_zones():
    return import_sibeliustalo_zones()


@pytest.fixture
def jussi_program(sibeliustalo_zones):
    return create_jussi_program(sibeliustalo_zones)


@pytest.fixture
def lattia_program():
    room = Room.objects.create(name='huone')
    zone = Zone.objects.create(name='lattia', room=room)
    row = Row.objects.create(zone=zone, start_number=1, end_number=10, excluded_numbers='3,4,5')
    assert row.capacity == 7
    t = now()
    program = Program.objects.create(
        room=zone.room,
        name='program',
        max_tickets=100,
        reservation_start=t,
        reservation_end=t + timedelta(days=1),
    )
    program.rows.set([row])
    return program


@pytest.fixture
def user_client(random_user):
    client = Client()
    client.force_login(random_user)
    client.user = random_user
    return client


@pytest.fixture
def random_user(django_user_model):
    return django_user_model.objects.create_user(username=get_random_string())
