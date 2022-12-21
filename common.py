from collections import defaultdict
import json
from typing import Any
from tabulate import tabulate
import os
import time
import psutil

def get_mem_info(pid: int) -> dict[str, int]:
  res = defaultdict(int)
  for page in psutil.Process(pid).memory_maps():
    res['rss'] += page.rss
    res['pss'] += page.pss
    res['uss'] += page.private_clean + page.private_dirty
    res['shared'] += page.shared_clean + page.shared_dirty
    if page.path.startswith('/'):
      res['shared_file'] += page.shared_clean + page.shared_dirty
  return res

class MemoryMonitor():
  def __init__(self, pids: list[int]=None):
    if pids is None:
      pids = [os.getpid()]
    self.pids = pids

  def add_pid(self, pid: int):
    assert pid not in self.pids
    self.pids.append(pid)

  def _refresh(self):
    self.data = {pid: get_mem_info(pid) for pid in self.pids}
    return self.data

  def table(self) -> str:
    self._refresh()
    table = []
    keys = list(list(self.data.values())[0].keys())
    now = str(int(time.perf_counter() % 1e5))
    for pid, data in self.data.items():
      table.append((now, str(pid)) + tuple(self.format(data[k]) for k in keys))
    return tabulate(table, headers=["time", "PID"] + keys)

  def str(self):
    self._refresh()
    keys = list(list(self.data.values())[0].keys())
    res = []
    for pid in self.pids:
      s = f"PID={pid}"
      for k in keys:
        v = self.format(self.data[pid][k])
        s += f", {k}={v}"
      res.append(s)
    return "\n".join(res)

  @staticmethod
  def format(size: int) -> str:
    for unit in ('', 'K', 'M', 'G'):
      if size < 1024:
        break
      size /= 1024.0
    return "%.1f%s" % (size, unit)


def create_list() -> list[Any]:
  with open("instances_train2017.json") as f:
    obj = json.load(f)
    return obj["annotations"]


if __name__ == "__main__":
  # import torch
  monitor = MemoryMonitor()
  print(monitor.str())
  lst = create_list()
  print(monitor.str())
  del lst; import gc; gc.collect()
  print(monitor.str())