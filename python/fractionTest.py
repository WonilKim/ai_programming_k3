from fraction import Fraction

def main():
    print('** start')
    
    number = input('Enter a positive number less than 1 : ')
    if(number[0] == '0'):
        precision = len(number[2])
    elif (number[0] == '.'):
        precision = len(number[1])
    else:
        print('Enter correct number')

    numer = int(float(number) * 10**precision)
    denom = int(10**precision)

    #
    # numer = int(input('Enter numerator : '))
    # denom = int(input('Enter denominator : '))

    frac = Fraction(numer, denom)
    numer_reduced, denom_reduced = frac.reduce()

    if denom_reduced == 1:
        print('Reduction: {}'.format(numer_reduced))

    else:
        print('Reduction: {} / {}'.format(numer_reduced, denom_reduced))
    

    main()