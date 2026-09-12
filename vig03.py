"""
Odds utilities: American <-> decimal conversion, implied probabilities,
overround (vig), and applying a margin to true probabilities.

American odds:
  +150 means bet 100 to win 150 (decimal 2.50)
  -200 means bet 200 to win 100 (decimal 1.50)
Decimal odds:
  total return per 1 staked, inclusive of stake (must be > 1).
"""

# --- single-price converters -------------------------------------------------

def fusa_to_dec(usa):
    # Plus money: usa/100 is the profit on a 100 stake.
    # Minus money: 100/|usa| is the profit on a |usa| stake.
    if -100 < usa < 100:
        raise ValueError('American odds must be >= 100 or < -100')
    elif usa > 0:
        return 1 + usa / 100
    elif usa < 0:
        return 1 - 100 / usa


def fdec_to_usa(dec):
    # dec >= 2 is plus money; 1 < dec < 2 is minus money (favourite).
    if dec <= 1:
        raise ValueError('decimal odds must be > 1')
    elif dec >= 2:
        return 100 * (dec - 1)
    elif 1 < dec < 2:
        return -100 / (dec - 1)


def gusa_to_dec(usa):
    """Convert a list of American prices to decimal."""
    return [fusa_to_dec(x) for x in usa]


def gdec_to_usa(dec):
    """Convert a list of decimal prices to American."""
    return [fdec_to_usa(x) for x in dec]


# --- input helpers -----------------------------------------------------------

def get_int(m):
    """Integer in 1..m inclusive."""
    while True:
        n_s = input('(?) ')
        try:
            n = int(n_s)
            if n < 1 or n > m:
                print('value out of range')
                continue
            return n
        except:
            print('bad input')
            continue


def get_float():
    while True:
        x_s = input('(?) ')
        try:
            return float(x_s)
        except:
            print('bad input')
            continue


def get_usa():
    """One American price; rejects the illegal open interval (-100, 100)."""
    while True:
        x_s = input('(?) ')
        try:
            x = float(x_s)
            if -100 < x < 100:
                print('American odds must be >= 100 or < -100')
                continue
            return x
        except:
            print('bad input')
            continue


def get_dec():
    """One decimal price; must be strictly greater than 1."""
    while True:
        x_s = input('(?) ')
        try:
            x = float(x_s)
            if x <= 1:
                print('decimal odds must be > 1')
                continue
            return x
        except:
            print('bad input')
            continue


# --- market maths ------------------------------------------------------------

def implied(usa):
    """
    From a book of American prices:
      raw implied p_i = 1 / decimal_i
      overround = sum(p_i) - 1          (vig as a fraction)
      norm      = p_i / sum(p_i)        (fair probs after removing juice)
    Additive overround: each side is priced as if multiplied by (1+vig)
    when going the other direction (see apply_margin).
    """
    dec = gusa_to_dec(usa)
    prob = [1 / x for x in dec]
    over = sum(prob)
    norm = [x / over for x in prob]
    vig = over - 1
    return norm, vig


def apply_margin(prob, vig):
    """
    Take a list of probabilities that already sum to 1 and a vig fraction
    (e.g. 0.05 for 5%). Price each outcome at
        decimal = 1 / (p * (1 + vig))
    then convert to American. Same multiplicative markup on every side.
    """
    dec = [1 / (x * (1 + vig)) for x in prob]
    return gdec_to_usa(dec)


# --- menu --------------------------------------------------------------------

while True:

    print('\n\n')
    print('(1) convert between American and decimal odds')
    print('(2) calculate overround and implied probability')
    print('(3) apply margin to get odds from probabilities')
    print('(4) quit\n')

    main_choice = get_int(4)
    print('\n')

    if main_choice == 4:
        break

    elif main_choice == 1:
        print('(1) convert American to decimal')
        print('(2) convert decimal to American\n')
        n = get_int(2)

        if n == 1:
            print('\nenter American odds')
            usa = get_usa()
            print('\ndecimal odds', fusa_to_dec(usa))

        if n == 2:
            print('\nenter decimal odds')
            dec = get_dec()
            print('\nAmerican odds', fdec_to_usa(dec))

    elif main_choice == 2:
        # Build a full market, strip juice, print fair % and overround.
        print('(1) American odds')
        print('(2) decimal odds\n')
        amer = get_int(2)
        print('\nenter the number of distinct possible outcomes')
        n = get_int(100)
        print('\n')

        if amer == 1:
            usa = []
            for i in range(n):
                print('enter odds for outcome', i + 1)
                usa.append(get_usa())
            print('\n')
            norm, vig = implied(usa)
            for i in range(n):
                print('implied probability of outcome', i + 1, 100 * norm[i], '%')
            print('overround', 100 * vig, '%')

        elif amer == 2:
            dec = []
            for i in range(n):
                print('enter odds for outcome', i + 1)
                dec.append(get_dec())
            print('\n')
            # implied() is written for American lists; convert first.
            usa = gdec_to_usa(dec)
            norm, vig = implied(usa)
            for i in range(n):
                print('implied probability of outcome', i + 1, 100 * norm[i], '%')
            print('overround', 100 * vig, '%')

    elif main_choice == 3:
        # User percents need not sum to 100; they are renormalized first.
        print('enter number of distinct possible outcomes')
        n = get_int(100)
        prob = []
        for i in range(n):
            print('enter probability', i + 1, '(%)')
            prob.append(0.01 * get_float())
        total = sum(prob)
        prob = [x / total for x in prob]
        print('\nenter overround (%)')
        vig = get_float() / 100
        usa = apply_margin(prob, vig)
        dec = gusa_to_dec(usa)
        print('\n')
        for i in range(n):
            print('outcome', i + 1, 'USA', usa[i], 'DEC', dec[i])
