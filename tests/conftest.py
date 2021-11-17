from collections import namedtuple
import os
from psutil import Process
from itertools import groupby
from _pytest.nodes import Item
from _pytest.terminal import TerminalReporter

LEAK_LIMIT = 10 * 1024 * 1024  # 100 MiB

_proc = Process(os.getpid())


def get_consumed_ram() -> int:
    return _proc.memory_info().rss


START = 'START'
END = 'END'
ConsumedRamLogEntry = namedtuple('ConsumedRamLogEntry', ('nodeid', 'on', 'consumed_ram'))
consumed_ram_log = []


def pytest_runtest_setup(item: Item) -> None:
    log_entry = ConsumedRamLogEntry(item.nodeid, START, get_consumed_ram())
    consumed_ram_log.append(log_entry)


def pytest_runtest_teardown(item: Item) -> None:
    log_entry = ConsumedRamLogEntry(item.nodeid, END, get_consumed_ram())
    consumed_ram_log.append(log_entry)


def pytest_terminal_summary(terminalreporter: TerminalReporter) -> None:
    terminalreporter.section("Memory usage")
    grouped = groupby(consumed_ram_log, lambda entry: entry.nodeid)
    for node_id, (start_entry, end_entry) in grouped:
        leaked = end_entry.consumed_ram - start_entry.consumed_ram
        if leaked > LEAK_LIMIT:
            terminalreporter.write('LEAKED {}MuB in {}\n'.format(leaked / 1024 / 1024, node_id))
