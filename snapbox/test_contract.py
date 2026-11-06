"""Contract tests — do NOT modify. Both student and peers run this."""
import unittest
from decimal import Decimal

from driver import Driver
from order import Order
from delivery_system import DeliverySystem


class TestDriverContract(unittest.TestCase):
    def test_initial_state(self):
        d = Driver('ali', (1, 2), 'BIKE')
        self.assertEqual(d.username, 'ali')
        self.assertEqual(d.position, (1, 2))
        self.assertEqual(d.service_category, 'BIKE')
        self.assertEqual(d.credit, Decimal('0'))
        self.assertEqual(d.status, 'FREE')
        self.assertIsNone(d.current_order)
        self.assertTrue(d.is_available())

    def test_properties_read_only(self):
        d = Driver('ali', (1, 2), 'BIKE')
        with self.assertRaises(AttributeError):
            d.credit = Decimal('100')
        with self.assertRaises(AttributeError):
            d.username = 'other'


class TestOrderContract(unittest.TestCase):
    def test_initial_state(self):
        o = Order(1, 'BIKE', (0, 0), (5, 5), Decimal('1000'))
        self.assertEqual(o.order_id, 1)
        self.assertEqual(o.service_category, 'BIKE')
        self.assertEqual(o.starting_position, (0, 0))
        self.assertEqual(o.finishing_position, (5, 5))
        self.assertEqual(o.cost, Decimal('1000'))
        self.assertEqual(o.status, 'PENDING')
        self.assertIsNone(o.assigned_driver)
        self.assertTrue(o.is_pending())


class TestDeliverySystemContract(unittest.TestCase):
    def test_empty_system(self):
        s = DeliverySystem()
        self.assertEqual(s.company_credit, Decimal('0'))
        self.assertEqual(s.total_drivers, 0)

    def test_add_driver(self):
        s = DeliverySystem()
        self.assertTrue(s.add_driver('ali', (0, 0), 'BIKE'))
        self.assertEqual(s.total_drivers, 1)
        self.assertFalse(s.add_driver('ali', (1, 1), 'VAN'))
        self.assertEqual(s.total_drivers, 1)

    def test_create_order_cost(self):
        s = DeliverySystem()
        # k=1, d=|18-(-33)|+|10-66|=51+56=107 → cost=(1+107)*100=10800
        oid = s.create_order('VAN', (18, 10), (-33, 66))
        self.assertEqual(oid, 1)
        info = s.get_order(1)
        self.assertEqual(info[0], 'PENDING')
        self.assertIsNone(info[1])
        self.assertEqual(info[2], Decimal('10800'))

    def test_create_order_invalid_same_position(self):
        s = DeliverySystem()
        self.assertIsNone(s.create_order('VAN', (1, 2), (1, 2)))
        self.assertEqual(s._next_order_id, 1)

    def test_full_flow(self):
        s = DeliverySystem()
        s.add_driver('ali', (10, 10), 'VAN')
        oid = s.create_order('VAN', (18, 10), (-33, 66))
        assigned = s.assign_next_order('ali')
        self.assertEqual(assigned, oid)
        self.assertEqual(s.get_order(oid)[0], 'ARRIVED')
        self.assertEqual(s.get_driver('ali')[0], 'BUSY')
        self.assertTrue(s.update_order_status('ali', oid, 'PICKUP'))
        self.assertEqual(s.get_driver('ali')[1], (18, 10))
        self.assertTrue(s.update_order_status('ali', oid, 'DELIVERED'))
        self.assertEqual(s.get_driver('ali')[1], (-33, 66))
        self.assertEqual(s.get_driver('ali')[2], Decimal('8640'))  # 80%
        self.assertEqual(s.company_credit, Decimal('2160'))         # 20%

    def test_invalid_transition(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        s.create_order('BIKE', (1, 1), (5, 5))
        # Cannot go from PENDING directly to PICKUP
        self.assertFalse(s.update_order_status('ali', 1, 'PICKUP'))

    def test_tie_break_oldest_first(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        o1 = s.create_order('BIKE', (5, 0), (10, 0))
        o2 = s.create_order('BIKE', (-5, 0), (-10, 0))
        chosen = s.assign_next_order('ali')
        self.assertEqual(chosen, o1)  # same distance, o1 older


if __name__ == '__main__':
    unittest.main()