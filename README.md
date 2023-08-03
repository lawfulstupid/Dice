# Dice
Analyse probability distributions of complex dice rolls. Uses Python 3.

Usage:
* Running: `python -i dice.py`
* `d2`, `d4`, `d6`, `d8`, `d10`, `d12`, `d20`, `d100` all in-built basic dice.
* Create a new die with faces values 1 to `n`: `d(n)`.
* Create a totally custom die: `Die({-1: 2, 0: 2, 1: 2})` creates a fudge die.
* Add, subtract, multiply, divide (floor division), and modulo with normal operators (`+-*/%`). Operands can be dice or integers.
* Combine dice into a tuple: `d4 & d4`.
* Take the max of two dice: `d20 | d20` behaves like a roll with advantage in D&D 5e.
* Compare dice/integers with `==`, `!=`, `<`, `<=`, `>`, `>=`.
* Roll dice: `d20.roll()`.
* Map dice values to new values: `d20.map(lambda n: n + 1)` is equivalent to `d20 + 1`.
* Map dice values to new dice: `d20.flatMap(lambda n: d(n))` is equivalent to rolling a d20, then rolling a die with face value between 1 and the result.
* Filter out dice values (maps approved values to themselves and rejected values to 0, or the provided failValue): `d6.filter(lambda n: n >= 5)` produces p.d.f `{0: 4/6, 5: 1/6, 6: 1/6}`.
