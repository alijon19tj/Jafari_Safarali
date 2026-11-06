"""Tests for the creative extension: 'cancel_order'.

Added behaviour (not part of base contract):
    DeliverySystem.cancel_order(order_id: int) -> bool

Rules:
- Only PENDING orders can be cancelled.
- Assigned order cannot be cancelled (must complete or be handled separately).
- On success, the order is removed from the system permanently.
- Cost is not paid back anywhere; the id is not reused.
"""
import unittest
from decimal import Decimal

from delivery_system import DeliverySystem


class TestCancelOrder(unittest.TestCase):
    def test_cancel_pending(self):
        s = DeliverySystem()
        oid = s.create_order('BIKE', (0, 0), (10, 0))
        self.assertTrue(s.cancel_order(oid))
        self.assertIsNone(s.get_order(oid))

    def test_cancel_unknown(self):
        s = DeliverySystem()
        self.assertFalse(s.cancel_order(999))

    def test_cancel_assigned_fails(self):
        s = DeliverySystem()
        s.add_driver('ali', (0, 0), 'BIKE')
        oid = s.create_order('BIKE', (1, 1), (5, 5))
        s.assign_next_order('ali')
        self.assertFalse(s.cancel_order(oid))
        self.assertEqual(s.get_order(oid)[0], 'ARRIVED')

    def test_cancel_does_not_refund(self):
        s = DeliverySystem()
        s.create_order('BIKE', (0, 0), (10, 0))
        s.cancel_order(1)
        self.assertEqual(s.company_credit, Decimal('0'))