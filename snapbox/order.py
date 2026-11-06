from decimal import Decimal


class Order:
    """Фармоишро нигоҳ медорад: id, навъи восита, маконҳо, арзиш, ҳолат."""

    def __init__(
        self,
        order_id: int,
        service_category: str,
        starting_position: tuple,
        finishing_position: tuple,
        cost: Decimal,
    ):
        self._order_id = order_id
        self._service_category = service_category
        self._starting_position = starting_position
        self._finishing_position = finishing_position
        self._cost = cost
        self._status = 'PENDING'
        self._assigned_driver = None

    @property
    def order_id(self):
        return self._order_id

    @property
    def service_category(self):
        return self._service_category

    @property
    def starting_position(self):
        return self._starting_position

    @property
    def finishing_position(self):
        return self._finishing_position

    @property
    def cost(self):
        return self._cost

    @property
    def status(self):
        return self._status

    @property
    def assigned_driver(self):
        return self._assigned_driver

    def is_pending(self) -> bool:
        return self._status == 'PENDING'

    # ---------- Internal methods ----------
    def _set_status(self, new_status: str) -> None:
        self._status = new_status

    def _set_assigned_driver(self, driver) -> None:
        self._assigned_driver = driver