from decimal import Decimal


class Driver:
    """Ронандаро нигоҳ медорад: ном, макон, навъи восита, кредит, ҳолат."""

    def __init__(self, username: str, position: tuple, service_category: str):
        self._username = username
        self._position = position
        self._service_category = service_category
        self._credit = Decimal('0')
        self._status = 'FREE'
        self._current_order = None

    @property
    def username(self):
        return self._username

    @property
    def position(self):
        return self._position

    @property
    def service_category(self):
        return self._service_category

    @property
    def credit(self):
        return self._credit

    @property
    def status(self):
        return self._status

    @property
    def current_order(self):
        return self._current_order

    def is_available(self) -> bool:
        return self._status == 'FREE'

    # ---------- Internal methods (used by DeliverySystem) ----------
    def _set_status(self, new_status: str) -> None:
        self._status = new_status

    def _set_position(self, new_position: tuple) -> None:
        self._position = new_position

    def _add_credit(self, amount: Decimal) -> None:
        self._credit = self._credit + amount

    def _set_current_order(self, order) -> None:
        self._current_order = order