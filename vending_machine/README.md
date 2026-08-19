# Vending Machine

A small vending machine simulation used as a pytest practice subject, with two implementation
versions and matching test suites.

## Files

- `vending_machine.py` — Main `VendingMachine` implementation: coin insertion, item selection,
  stock/price lookup, change calculation, refunds, and custom errors
  (`InsufficientFundsError`, `OutOfStockError`).
- `vending_machine_v1.py` — An earlier/alternate version of the same machine, with its own
  `get_stock`/`get_price` helpers and slightly different behavior, kept for comparison.
- `test_vending_machine.py` — Test suite for `vending_machine.py` (smoke tests, parametrized
  purchases, error cases, refunds, stock changes).
- `test_vending_machine_v1.py` — Equivalent test suite for `vending_machine_v1.py`.

## Running

```powershell
python -m pytest vending_machine
```
