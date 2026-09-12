# vig03

Small command-line tool for sportsbook prices.

It converts American and decimal odds, strips juice from a market to get implied probabilities, and applies a margin to fair probabilities to get a book.

This is pricing plumbing, not a model of a sport.

## Requirements

Python 3. No third-party packages.

```bash
python vig03.py
```

## Menu

1. **Convert** one American price to decimal, or the reverse.
2. **Implied probabilities** from a full market (American or decimal). Prints the renormalized probabilities and the overround.
3. **Apply margin.** Enter outcome probabilities (percents need not sum to 100; they are renormalized) and an overround percent. Prints American and decimal prices on every side.
4. Quit.

## Maths

American \(\leftrightarrow\) decimal:

- \(usa > 0\): \(\mathrm{dec} = 1 + usa/100\)
- \(usa < 0\): \(\mathrm{dec} = 1 - 100/usa\)
- \(|usa| < 100\) is rejected (not a valid American price)

Implied from a book:

- raw \(p_i = 1/\mathrm{dec}_i\)
- overround \(= \sum p_i - 1\)
- fair \(p_i \leftarrow p_i / \sum p_j\)

Margin on fair probabilities \(p\) with vig \(v\):

\[
\mathrm{dec}_i = \frac{1}{p_i(1+v)}
\]

Same multiplicative markup on every outcome.

## What this is for

- Checking a 1X2 or two-way book for juice
- Turning a model probability vector into a priced market
- Converting screens between US and decimal

## What not to trust it for

- It does not estimate probabilities from data. Garbage \(p\) in, coherent junk prices out.
- The margin is **uniform** across sides. Real books shade favorites, longs, and limits differently.
- It does not handle each-way, dead-heat, rule-4, or Asian-handicap settlement.
- Implied probabilities assume the listed outcomes are the whole sample space. Missing a push/draw will mis-state the overround.

## License

Use as you like for a portfolio or a desk calculator.

# dixon_sweep.cpp

Dixon–Coles football score model. Prints 1X2 and BTTS while \(\rho\) runs from \(-0.15\) to \(0\).

This is a desk calculator, not a fitted model. You type two goal means. The code does not estimate them from results.

Dixon_sweep

No libraries beyond the C++ standard headers.

## Model

Home and away goals start as independent Poisson with means \(\mu_H\), \(\mu_A\). The joint mass on goals \(0\)–\(30\) is then reweighted on four cells only:

| cell | factor |
|------|--------|
| (0,0) | \(1 - \mu_H\mu_A\rho\) |
| (0,1) | \(1 + \mu_H\rho\) |
| (1,0) | \(1 + \mu_A\rho\) |
| (1,1) | \(1 - \rho\) |

That is the Dixon–Coles \(\tau\). Marginal \(P(H=0)\) and \(P(A=0)\) stay Poisson (so “home scores” / “away scores” barely move). Draw and BTTS move.

Legal \(\rho\) for a given match:

\[
\max(-1/\mu_H,-1/\mu_A)\;\le\;\rho\;\le\;\min\bigl(1,\;1/(\mu_H\mu_A)\bigr).
\]

Typical fitted football values sit near \(-0.13\) to \(-0.05\). \(\rho=0\) is plain independent Poisson.

## Output

Each line:

`rho    home    draw    away    btts`

As \(\rho\) rises toward \(0\), draw and BTTS should fall. If a cell goes negative, \(\rho\) is outside the interval above.

Grid is truncated at 30 goals. Total mass is slightly under 1. Fine for a comparison table; divide by the sum of the matrix if you want prices that add to 1.

## What not to trust it for

- Estimating \(\mu\) or \(\rho\) from data
- Live in-play (means do not decay with time)
- Asian handicaps, exact score, or correlated vig across markets
- Means so small that \(-0.15\) is illegal

## Related

Python twin: the `soccer_dixon` sweep. Pricing utilities: `vig03.py`.

