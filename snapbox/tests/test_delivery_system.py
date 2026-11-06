import unittest
from decimal import Decimal

from delivery_system import DeliverySystem


class TestAddDriver(unittest.TestCase):
    def test_valid(self):
        s = DeliverySystem()
        self.assertTrue(s.add_driver('ali', (0, 0), 'BIKE'))
        self.assertEqual(s.total_drivers, 1)

    def test_duplicate(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        self.assertFalse(s.add_driver('ali', (1, 1), 'VAN'))

    def test_bad_position_type(self):
        s = DeliverySystem()
        with self.assertRaises(TypeError):
            s.add_driver('ali', [1, 2], 'BIKE')

    def test_bad_position_length(self):
        s = DeliverySystem()
        with self.assertRaises(ValueError):
            s.add_driver('ali', (1,), 'BIKE')

    def test_bool_in_position(self):
        s = DeliverySystem()
        with self.assertRaises(TypeError):
            s.add_driver('ali', (True, 2), 'BIKE')

    def test_bad_category(self):
        s = DeliverySystem()
        with self.assertRaises(ValueError):
            s.add_driver('ali', (0, 0), 'CAR')

    def test_bad_username(self):
        s = DeliverySystem()
        with self.assertRaises(ValueError):
            s.add_driver('ali-123', (0, 0), 'BIKE')


class TestCreateOrder(unittest.TestCase):
    def test_cost_first_order(self):
        s = DeliverySystem()
        # k=1, d=100 → cost = 101*100 = 10100
        oid = s.create_order('BIKE', (0, 0), (50, 50))
        self.assertEqual(oid, 1)
        self.assertEqual(s.get_order(1)[2], Decimal('10100'))

    def test_k_counts_pending_same_category(self):
        s = DeliverySystem()
        s.create_order('BIKE', (0, 0), (10, 0))     # k=1, d=10 → 1100
        s.create_order('BIKE', (0, 0), (10, 0))     # k=2, d=10 → 1200
        self.assertEqual(s.get_order(1)[2], Decimal('1100'))
        self.assertEqual(s.get_order(2)[2], Decimal('1200'))

    def test_same_start_finish_returns_none(self):
        s = DeliverySystem()
        self.assertIsNone(s.create_order('BIKE', (5, 5), (5, 5)))
        self.assertEqual(s.get_order_list('PENDING'), [])


class TestAssign(unittest.TestCase):
    def test_nearest(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        s.create_order('BIKE', (100, 0), (110, 0))
        near = s.create_order('BIKE', (1, 0), (2, 0))
        self.assertEqual(s.assign_next_order('ali'), near)

    def test_no_order(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        self.assertIsNone(s.assign_next_order('ali'))

    def test_busy_driver(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        s.create_order('BIKE', (10, 0), (20, 0))
        s.create_order('BIKE', (11, 0), (21, 0))
        s.assign_next_order('ali')
        with self.assertRaises(RuntimeError):
            s.assign_next_order('ali')

    def test_unknown_driver(self):
        s = DeliverySystem()
        with self.assertRaises(KeyError):
            s.assign_next_order('nobody')


class TestUpdateStatus(unittest.TestCase):
    def test_full_cycle_payments(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        oid = s.create_order('BIKE', (0, 0), (10, 0))  # cost = 1100
        s.assign_next_order('ali')
        s.update_order_status('ali', oid, 'PICKUP')
        s.update_order_status('ali', oid, 'DELIVERED')
        # 80% = 880, 20% = 220
        self.assertEqual(s.get_driver('ali')[2], Decimal('880'))
        self.assertEqual(s.company_credit, Decimal('220'))

    def test_invalid_transition_no_change(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        oid = s.create_order('BIKE', (0, 0), (10, 0))
        s.assign_next_order('ali')
        # ARRIVED → DELIVERED is illegal (must be PICKUP first)
        before = s.get_driver('ali')
        self.assertFalse(s.update_order_status('ali', oid, 'DELIVERED'))
        self.assertEqual(s.get_driver('ali'), before)

    def test_wrong_driver(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        s.add_driver('bob', (0, 0), 'BIKE')
        oid = s.create_order('BIKE', (0, 0), (10, 0))
        s.assign_next_order('ali')
        self.assertFalse(s.update_order_status('bob', oid, 'PICKUP'))


class TestQueries(unittest.TestCase):
    def test_near_drivers_sort_and_tie(self):
        s = DeliverySystem()
        s.add_driver('a', (5, 0), 'BIKE')
        s.add_driver('b', (-5, 0), 'BIKE')   # same distance from origin
        s.add_driver('c', (0, 1), 'BIKE')
        # From origin: c (1), then a and b (5 each — a first by registration)
        self.assertEqual(s.get_near_drivers((0, 0), 3), ['c', 'a', 'b'])

    def test_count_orders(self):
        s = DeliverySystem()
        s.create_order('BIKE', (0, 0), (100, 0))
        s.create_order('VAN', (5, 0), (200, 0))
        # Count of START within 10 from (0,0): both → 2
        self.assertEqual(s.count_orders((0, 0), 10, 'START'), 2)
        # Count of FINISH within 10: none → 0
        self.assertEqual(s.count_orders((0, 0), 10, 'FINISH'), 0)

    def test_nearest_pending(self):
        s = DeliverySystem()
        s.create_order('BIKE', (10, 0), (20, 0))
        near = s.create_order('VAN', (1, 0), (5, 0))
        self.assertEqual(s.get_nearest_pending_order((0, 0)), near)

    def test_nearest_pending_none(self):
        s = DeliverySystem()
        self.assertIsNone(s.get_nearest_pending_order((0, 0)))