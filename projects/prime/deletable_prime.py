class IDeletableStrategy:
    def get_ways(self):
        pass
class IOps:
    def execute(self):
        pass
import math
from random import randint
class IPrimeChecker:
     def check(self,val:int):
            raise NotImplementedError("abstract method")
class NormalWay(IPrimeChecker):
    def check(self,n:int):
        if n > 1:
            for i in range(2, int(math.sqrt(n))+1):
                # 2 is minimum and n/2 is the highest divider for a integer number
                 if n % i == 0:
                    return False
                    # in case if the number is divisible with any number it will return False.
            return True
            # if not divisible with any number return True therefore it is prime number.
        return False
class FermatWay(IPrimeChecker):
    def power(self,a, n, p):
        res = 1
        # Update 'a' if 'a' >= p
        a = a % p
        while n > 0:

            # If n is odd, multiply
            # 'a' with result
            if n % 2:
                res = (res * a) % p
                n = n - 1
            else:
                a = (a ** 2) % p
                # n must be even now
                n = n // 2
        return res % p
    def check(self,num3:int):
        if num3 < 2:
            return False
        if num3==2 or num3==3:
            return True
        check_times = 5
        looped = 0
        
        while True:
            a = randint(2, num3-1)
            if num3 % a == 0:
                continue
            looped += 1
            if self.power(a, num3-1, num3)!= 1:
                return False
            if looped == check_times:
                break
        return True
class RobinMiller(IPrimeChecker):
    def __init__(self):
        self.set_loop_time(5)
    def check(self, n: int):
        if (n <= 1 or n == 4):
            return False
        if (n <= 3):
            return True
        
        d = n - 1;
        while (d % 2 == 0):
            d //= 2
            
        for _ in range(self._loop_time):
            if (not self._miller_test(d, n)):
                return False
        return True
    def _miller_test(self, d, n):
        a = 2 + randint(1, n - 4)
        x = self.power(a, d, n);

        if (x == 1 or x == n - 1):
            return True;
        while (d != n - 1):
            x = (x * x) % n
            d *= 2;

            if (x == 1):
                return False
            if (x == n - 1):
                return True

        return False
    def set_loop_time(self, n: int):
        self._loop_time = n

    def power(self,x, y, p):
        res = 1
        x = x % p
        while (y > 0):

            if (y & 1):
                res = (res * x) % p

            y = y>>1
            x = (x * x) % p

        return res
class OldWay(IPrimeChecker):
    def check(self,n):  # function for prime numbers
        if n > 1:
            for i in range(2, int(n / 2)+1):
                # 2 is minimum and n/2 is the highest divider for a integer number
                if n % i == 0:
                    return False
                # in case if the number is divisible with any number it will return False.
            return True
class RemoveIthNumber(IOps):
    def __init__(self,ith, number):
        self._ith = ith
        self._number = number
    def execute(self):
        ith = self._ith
        number = self._number
        new_arr = [v for i, v in enumerate(str(number)) if i != ith]
        for i, v in enumerate(new_arr):
            if int(v) != 0:
                break
        new_arr = new_arr[i:]
        return int(''.join(new_arr))
class WithoutMemoization(IDeletableStrategy):
    def set_prime_checker(self, prime_checker: IPrimeChecker):
        self._checker = prime_checker
    def get_ways(self):
        return self._find(self._number)
    def _find(self, number):
        if number < 10:
            return int(self._checker.check(number))
        t =0
        for i in range(len(str(number))):
            new_num = RemoveIthNumber(i, number).execute()
            if self._checker.check(new_num):
                t += self._find(new_num)
        return t
    def set_number(self, number):
        self._number = number
class WithMemoization(IDeletableStrategy):
    def __init__(self):
        self._memo = {}
    def set_prime_checker(self, prime_checker: IPrimeChecker):
        self._checker = prime_checker
    def get_ways(self):
        return self._find(self._number)
    def _find(self, number):
        if number in self._memo:
            return self._memo[number]
        if number < 10:
            return int(self._checker.check(number))
        t =0
        for i in range(len(str(number))):
            new_num = RemoveIthNumber(i, number).execute()
            if self._checker.check(new_num):
                t += self._find(new_num)
        self._memo[number] = t
        return t
    def set_number(self, number):
        self._number = number


class Main:
    def deleteable_ways(number, way = NormalWay(), strategy= WithMemoization()):
        strategy.set_prime_checker(way)
        strategy.set_number(number)
        return strategy.get_ways()
class Example:
    def example_small():
        n = 567629137
        print(Main.deleteable_ways(n))
    def example_big():
        n = 46216567629137
        print(Main.deleteable_ways(n))