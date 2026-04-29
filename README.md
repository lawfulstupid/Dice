# Dice
Roll and analyse arbitrary sets of dice using native Python 3.

Usage:
* `d2`, `d4`, `d6`, `d8`, `d10`, `d12`, `d20`, `d100`, `dF` all in-built basic dice.
* Create a new die with faces values 1 to `n`: `Die(n)`.
* Create a totally custom die: `Die({-1: 2, 0: 2, 1: 2})` creates a FUDGE/FATE die.
* Add, subtract, multiply, divide (floor division), and modulo with normal operators (`+-*/%`). Operands can be dice or integers.
* Shorthand for rolling multiple dice and summing them: `d6.by(3) := d6 + d6 + d6`.
* Combine dice into a tuple: `d4 & d4`.
* Take the max of two dice: `d20 | d20` behaves like a roll with advantage in D&D 5e.
* Compare dice/integers with `==`, `!=`, `<`, `<=`, `>`, `>=`.
* Roll dice: `d20.roll()`.
* Exploding dice: `d20.explode()`.
* Compute expected value: `d6.exp()`.
* Map dice values to new values: `d20.map(lambda n: n + 1)` is equivalent to `d20 + 1`.
* Map dice values to new dice: `d4.map(lambda n: d6.by(n))` is equivalent to rolling a d4, then rolling that many d6s.
* Filter out dice values: `d6.filter(lambda n: n >= 5)` produces PDF `{5: 1, 6: 1}`.
