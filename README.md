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
