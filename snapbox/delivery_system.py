from decimal import Decimal

from driver import Driver
from order import Order


VALID_CATEGORIES = ('BIKE', 'VAN', 'TRUCK')
VALID_DRIVER_STATUSES = ('FREE', 'BUSY')
VALID_ORDER_STATUSES = ('PENDING', 'ARRIVED', 'PICKUP', 'DELIVERED')

# Transitions allowed for an order
ALLOWED_TRANSITIONS = {
    'PENDING': {'ARRIVED'},
    'ARRIVED': {'PICKUP'},
    'PICKUP': {'DELIVERED'},
    'DELIVERED': set(),
}


def _validate_position(position, name='position'):
    if not isinstance(position, tuple):
        raise TypeError(f'{name} must be a tuple')
    if len(position) != 2:
        raise ValueError(f'{name} must have exactly 2 elements')
    for coord in position:
        if isinstance(coord, bool) or not isinstance(coord, int):
            raise TypeError(f'{name} coordinates must be int (not bool)')


def _validate_category(category, name='service_category'):
    if not isinstance(category, str):
        raise TypeError(f'{name} must be a string')
    if category not in VALID_CATEGORIES:
        raise ValueError(f'{name} must be one of {VALID_CATEGORIES}')


def _validate_username(username):
    if not isinstance(username, str):
        raise TypeError('username must be a string')
    if not (1 <= len(username) <= 25):
        raise ValueError('username must be 1..25 characters')
    if not all(c.isascii() and c.isalnum() for c in username):
        raise ValueError('username must contain only English letters and digits')


def _validate_positive_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f'{name} must be int')
    if value <= 0:
        raise ValueError(f'{name} must be positive')


def _validate_non_negative_int(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f'{name} must be int')
    if value < 0:
        raise ValueError(f'{name} must be non-negative')


def _manhattan(a: tuple, b: tuple) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class DeliverySystem:
    """Системаи идоракунии ронандагон ва фармоишҳо."""

    def __init__(self):
        self._drivers = {}          # username -> Driver (ordered)
        self._orders = {}           # order_id -> Order (ordered)
        self._next_order_id = 1
        self._company_credit = Decimal('0')

    # ---------- Properties ----------
    @property
    def company_credit(self) -> Decimal:
        return self._company_credit

    @property
    def total_drivers(self) -> int:
        return len(self._drivers)

    # ---------- Drivers ----------
    def add_driver(self, username: str, position: tuple, service_category: str) -> bool:
        _validate_username(username)
        _validate_position(position)
        _validate_category(service_category)

        if username in self._drivers:
            return False

        self._drivers[username] = Driver(username, position, service_category)
        return True

    def get_driver(self, username: str):
        if not isinstance(username, str):
            raise TypeError('username must be a string')
        driver = self._drivers.get(username)
        if driver is None:
            return None
        return (driver.status, driver.position, driver.credit)

    def get_driver_list(self, status: str) -> list:
        if not isinstance(status, str):
            raise TypeError('status must be a string')
        if status not in VALID_DRIVER_STATUSES:
            raise ValueError('invalid driver status')
        result = []
        for username, driver in self._drivers.items():
            if driver.status == status:
                result.append(username)
        return result

    # ---------- Orders ----------
    def create_order(self, service_category: str, starting_position: tuple, finishing_position: tuple):
        _validate_category(service_category)
        _validate_position(starting_position, 'starting_position')
        _validate_position(finishing_position, 'finishing_position')

        if starting_position == finishing_position:
            return None

        # k = count of PENDING orders of same category, INCLUDING the new one
        pending_count = 1
        for order in self._orders.values():
            if order.service_category == service_category and order.is_pending():
                pending_count += 1

        distance = _manhattan(starting_position, finishing_position)
        cost = Decimal(100) * Decimal(pending_count + distance)

        order_id = self._next_order_id
        self._next_order_id += 1

        self._orders[order_id] = Order(
            order_id=order_id,
            service_category=service_category,
            starting_position=starting_position,
            finishing_position=finishing_position,
            cost=cost,
        )
        return order_id

    def get_order(self, order_id: int):
        _validate_positive_int(order_id, 'order_id')
        order = self._orders.get(order_id)
        if order is None:
            return None
        driver = order.assigned_driver
        driver_name = driver.username if driver is not None else None
        return (order.status, driver_name, order.cost)

    def get_order_list(self, status: str) -> list:
        if not isinstance(status, str):
            raise TypeError('status must be a string')
        if status not in VALID_ORDER_STATUSES:
            raise ValueError('invalid order status')
        result = []
        for order_id, order in self._orders.items():
            if order.status == status:
                result.append(order_id)
        return result

    # ---------- Assignment ----------
    def assign_next_order(self, username: str):
        if not isinstance(username, str):
            raise TypeError('username must be a string')
        if username not in self._drivers:
            raise KeyError(username)

        driver = self._drivers[username]
        if driver.status == 'BUSY':
            raise RuntimeError('driver is already busy')

        candidates = []
        for order in self._orders.values():
            if order.is_pending() and order.service_category == driver.service_category:
                candidates.append(order)

        if not candidates:
            return None

        best = None
        best_distance = None
        for order in candidates:
            dist = _manhattan(driver.position, order.starting_position)
            if best is None or dist < best_distance:
                best = order
                best_distance = dist
            elif dist == best_distance and order.order_id < best.order_id:
                best = order
                best_distance = dist

        best._set_status('ARRIVED')
        best._set_assigned_driver(driver)
        driver._set_status('BUSY')
        driver._set_current_order(best)
        return best.order_id

    # ---------- Status update ----------
    def update_order_status(self, username: str, order_id: int, new_status: str) -> bool:
        if not isinstance(username, str):
            raise TypeError('username must be a string')
        _validate_positive_int(order_id, 'order_id')
        if not isinstance(new_status, str):
            raise TypeError('new_status must be a string')
        if new_status not in VALID_ORDER_STATUSES:
            raise ValueError('invalid new_status')

        if username not in self._drivers:
            raise KeyError(username)

        driver = self._drivers[username]
        order = self._orders.get(order_id)

        if order is None:
            return False
        if order.assigned_driver is not driver:
            return False
        if new_status not in ALLOWED_TRANSITIONS[order.status]:
            return False

        # Apply transition side effects
        if new_status == 'PICKUP':
            driver._set_position(order.starting_position)
        elif new_status == 'DELIVERED':
            driver._set_position(order.finishing_position)
            driver_share = (order.cost * Decimal('0.8'))
            company_share = (order.cost * Decimal('0.2'))
            driver._add_credit(driver_share)
            self._company_credit = self._company_credit + company_share
            driver._set_status('FREE')
            driver._set_current_order(None)

        order._set_status(new_status)
        return True

    # ---------- Search ----------
    def get_near_drivers(self, position: tuple, count: int) -> list:
        _validate_position(position)
        _validate_non_negative_int(count, 'count')

        free_drivers = [d for d in self._drivers.values() if d.status == 'FREE']
        # Stable sort by distance; old registration order preserved on ties
        ordered = sorted(free_drivers, key=lambda d: _manhattan(position, d.position))
        return [d.username for d in ordered[:count]]

    def count_orders(self, position: tuple, distance: int, endpoint: str) -> int:
        _validate_position(position)
        _validate_non_negative_int(distance, 'distance')
        if not isinstance(endpoint, str):
            raise TypeError('endpoint must be a string')
        if endpoint not in ('START', 'FINISH'):
            raise ValueError('endpoint must be START or FINISH')

        total = 0
        for order in self._orders.values():
            point = order.starting_position if endpoint == 'START' else order.finishing_position
            if _manhattan(position, point) <= distance:
                total += 1
        return total

    def get_nearest_pending_order(self, position: tuple):
        _validate_position(position)

        best = None
        best_distance = None
        for order in self._orders.values():
            if not order.is_pending():
                continue
            dist = _manhattan(position, order.starting_position)
            if best is None or dist < best_distance:
                best = order
                best_distance = dist
            elif dist == best_distance and order.order_id < best.order_id:
                best = order
                best_distance = dist
        return best.order_id if best is not None else None

    def get_company_credit(self) -> Decimal:
        return self._company_credit


    def cancel_order(self, order_id: int) -> bool:
        """Бекор кардани фармоиши PENDING. True агар бекор шуд, False дар акси ҳол."""
        _validate_positive_int(order_id, 'order_id')
        order = self._orders.get(order_id)
        if order is None or not order.is_pending():
            return False
        del self._orders[order_id]
        return True