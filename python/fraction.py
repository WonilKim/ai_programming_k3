# 분자와 분모에 대한 인스턴스 변수가 있는 Fraction이라는 클래스와 
# 분자와 분모를 최대 공약수로 나누어 파벌을 가장 낮은 용어로 줄이는 메서드를 만듭니다. 
# 두 개의 0이 아닌 정수 mand nis의 최대 공약수를 구하는 코드는 다음과 같습니다. 
#
# def GCD(m, n): #Greatest Common Divisor
#     while n != 0:
#         t = n
#         n = m % n
#         m = t
#     return m
#
# fraction.py 파일에 클래스를 저장합니다.
# 참고: 이 클래스는 연습문제 28과 29에서 사용됩니다.

class Fraction:
    def __init__(self, numerator, denominator):
        self._numerator = numerator
        self._denominator = denominator

    @staticmethod
    def GCD(m, n): #Greatest Common Divisor
        while n != 0:
            t = n
            n = m % n
            m = t
        return m
    
    def reduce(self):
        gcd = self.GCD(self._numerator, self._denominator)
        return self._numerator // gcd, self._denominator // gcd
