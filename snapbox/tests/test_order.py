import unittest
from decimal import Decimal

from order import Order


class TestOrder(unittest.TestCase):
    def test_initial(self):
        o = Order(7, 'TRUCK', (0, 0), (10, 10), Decimal('2000'))
        self.assertEqual(o.order_id, 7)
        self.assertEqual(o.status, 'PENDING')
        self.assertIsNone(o.assigned_driver)
        self.assertTrue(o.is_pending())

    def test_read_only(self):
        o = Order(1, 'BIKE', (0, 0), (1, 1), Decimal('100'))
        for attr in ('order_id', 'service_category', 'starting_position',
                     'finishing_position', 'cost', 'status', 'assigned_driver'):
            with self.assertRaises(AttributeError):
                setattr(o, attr, None)

    def test_is_pending(self):
        o = Order(1, 'BIKE', (0, 0), (1, 1), Decimal('100'))
        o._set_status('ARRIVED')
        self.assertFalse(o.is_pending())