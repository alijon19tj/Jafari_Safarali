import unittest
from decimal import Decimal

from driver import Driver


class TestDriver(unittest.TestCase):
    def test_initial_values(self):
        d = Driver('ali', (1, 2), 'VAN')
        self.assertEqual(d.username, 'ali')
        self.assertEqual(d.position, (1, 2))
        self.assertEqual(d.service_category, 'VAN')
        self.assertEqual(d.credit, Decimal('0'))
        self.assertEqual(d.status, 'FREE')
        self.assertIsNone(d.current_order)
        self.assertTrue(d.is_available())

    def test_read_only(self):
        d = Driver('ali', (1, 2), 'BIKE')
        for attr in ('username', 'position', 'service_category', 'credit', 'status', 'current_order'):
            with self.assertRaises(AttributeError):
                setattr(d, attr, None)

    def test_is_available_after_status_change(self):
        d = Driver('ali', (0, 0), 'BIKE')
        d._set_status('BUSY')
        self.assertFalse(d.is_available())
        d._set_status('FREE')
        self.assertTrue(d.is_available())