import time
import sys

sys.path.insert(0, "../randmac/")
import randmac


def bench():
    iterations = 10000
    time0 = time.time()
    for number in range(iterations):
        test()
    time1 = time.time()
    total = time1 - time0
    print("{} iterations time is {}".format(iterations, total))


def test():
    """
    randmac.py 00-00-00-00-00-00
    randmac.py 00-00-00-00-00-00 -f
    randmac.py 00:00:00:00:00:00
    randmac.py 00:00:00:00:00:00 -f
    randmac.py 00.00.00.00.00.00
    randmac.py 00.00.00.00.00.00 -f
    randmac.py 0000.0000.0000
    randmac.py 0000.0000.0000 -f
    randmac.py 000000000000
    randmac.py 000000000000 -f
    """
    for mac in [
        "00-00-00-00-00-0f",
        "00:00:00:00:00:0F",
        "0000.0000.000f",
        "00.00.00.00.0F.00",
        "00000000000f",
    ]:
        # print("input {}".format(mac))
        mac = randmac.nic_portion(mac)
        # print("output nic {}".format(mac))
        mac = randmac.twelve_digit_mac(mac)
        # print("output mac {}".format(mac))
        # print("")


if __name__ == "__main__":
    bench()
