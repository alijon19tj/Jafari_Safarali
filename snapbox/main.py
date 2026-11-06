"""CLI for Snapbox — matching the Quera problem format."""
import re
import sys
from decimal import Decimal

from delivery_system import DeliverySystem


POS_RE = re.compile(r'\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)')


def parse_position(token: str) -> tuple:
    m = POS_RE.fullmatch(token)
    if not m:
        raise ValueError(f'invalid position: {token}')
    return (int(m.group(1)), int(m.group(2)))


def split_line(line: str):
    """Split a line into tokens, but keep (x, y) positions as one token."""
    tokens = []
    i = 0
    n = len(line)
    while i < n:
        # Skip whitespace
        while i < n and line[i].isspace():
            i += 1
        if i >= n:
            break
        if line[i] == '(':
            # Find matching ')'
            j = line.find(')', i)
            if j == -1:
                raise ValueError('unclosed parenthesis')
            tokens.append(line[i:j+1])
            i = j + 1
        else:
            j = i
            while j < n and not line[j].isspace():
                j += 1
            tokens.append(line[i:j])
            i = j
    return tokens


def fmt_decimal(d: Decimal) -> str:
    if d == d.to_integral_value():
        return str(int(d))
    return str(d)


def main():
    system = DeliverySystem()
    output = []

    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            parts = split_line(line)
        except ValueError:
            output.append('invalid input')
            continue
        if not parts:
            continue
        cmd = parts[0]

        try:
            if cmd == 'END':
                break

            elif cmd == 'ADD-DRIVER':
                username = parts[1]
                position = parse_position(parts[2])
                category = parts[3]
                if system.add_driver(username, position, category):
                    output.append('user added successfully')
                else:
                    output.append('user previously added')

            elif cmd == 'CREATE-ORDER':
                category = parts[1]
                start = parse_position(parts[2])
                finish = parse_position(parts[3])
                oid = system.create_order(category, start, finish)
                if oid is None:
                    output.append('invalid order')
                else:
                    output.append(str(oid))

            elif cmd == 'ASSIGN-NEXT-ORDER':
                username = parts[1]
                if username not in system._drivers:
                    output.append('invalid driver name')
                    continue
                try:
                    oid = system.assign_next_order(username)
                except RuntimeError:
                    output.append('driver is already busy')
                    continue
                if oid is None:
                    output.append('there is no order right now')
                else:
                    output.append(f'{oid} assigned to {username}')

            elif cmd == 'GET-DRIVER':
                username = parts[1]
                info = system.get_driver(username)
                if info is None:
                    output.append('invalid driver name')
                else:
                    status, pos, credit = info
                    output.append(f'{status} ({pos[0]}, {pos[1]}) {fmt_decimal(credit)}')

            elif cmd == 'ORDER-UPDATE':
                new_status = parts[1]
                username = parts[2]
                try:
                    oid = int(parts[3])
                except ValueError:
                    output.append('wrong order-id')
                    continue
                if username not in system._drivers:
                    output.append('invalid driver name')
                    continue
                try:
                    ok = system.update_order_status(username, oid, new_status)
                except ValueError:
                    output.append('invalid status')
                    continue
                if not ok:
                    order = system._orders.get(oid)
                    if order is None or order.assigned_driver is not system._drivers.get(username):
                        output.append('wrong order-id')
                    else:
                        output.append('invalid status')
                else:
                    output.append('status changed successfully')

            elif cmd == 'GET-ORDER':
                try:
                    oid = int(parts[1])
                except ValueError:
                    output.append('invalid order')
                    continue
                info = system.get_order(oid)
                if info is None:
                    output.append('invalid order')
                else:
                    status, driver_name, cost = info
                    driver_name = driver_name if driver_name is not None else 'None'
                    output.append(f'{status} {driver_name} {fmt_decimal(cost)}')

            elif cmd == 'GET-ORDER-LIST':
                status = parts[1]
                ids = system.get_order_list(status)
                if not ids:
                    output.append('None')
                else:
                    output.append(' '.join(str(i) for i in ids))

            elif cmd == 'GET-DRIVER-LIST':
                status = parts[1]
                names = system.get_driver_list(status)
                if not names:
                    output.append('None')
                else:
                    output.append(' '.join(names))

            elif cmd == 'GET-NEAR-DRIVER':
                position = parse_position(parts[1])
                count = int(parts[2])
                names = system.get_near_drivers(position, count)
                if not names:
                    output.append('None')
                else:
                    output.append(' '.join(names))

            elif cmd == 'GET-CNT-ORDER':
                position = parse_position(parts[1])
                distance = int(parts[2])
                endpoint = parts[3]
                cnt = system.count_orders(position, distance, endpoint)
                output.append(str(cnt))

            elif cmd == 'GET-NEAREST-PENDING-ORDER':
                position = parse_position(parts[1])
                oid = system.get_nearest_pending_order(position)
                output.append(str(oid) if oid is not None else 'None')

            elif cmd == 'GET-COMPANY':
                output.append(fmt_decimal(system.get_company_credit()))

            else:
                output.append(f'unknown command: {cmd}')

        except (ValueError, TypeError, KeyError):
            output.append('invalid input')

    sys.stdout.write('\n'.join(output))
    if output:
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()