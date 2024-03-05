import unittest
from ctypes import CDLL
from time import sleep
import random
import socket
import struct
lib = CDLL("./libprefixes.so")


class PrefixManagerTest(unittest.TestCase):
    def setUp(self):
        self.test_length = 10000
        self.add_ip_passed = 0
        self.add_ip_failed = 0
        self.check_ip_passed = 0
        self.check_ip_failed = 0
        self.delete_prefix_pass = 0
        self.delete_prefix_fail = 0

    @staticmethod
    def generate_ip_address():
        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

    @staticmethod
    def ip_to_uint(ip):
        return struct.unpack('>I', socket.inet_aton(ip))[0]

    def test_add_check_delete_prefix(self):
        for _ in range(self.test_length):
            ip_address = self.generate_ip_address()
            mask = random.randint(0, 24)
            ip_uint = self.ip_to_uint(ip_address)
            result = lib.add(ip_uint, mask)
            if result == 1:
                self.add_ip_passed += 1
            else:
                self.add_ip_failed += 1

            result = lib.check(ip_uint)
            if result == 1:
                self.check_ip_passed += 1
            else:
                self.check_ip_failed += 1

            result = lib.delete_prefix(ip_uint, mask)
            if result == 1:
                self.delete_prefix_pass += 1
            else:
                self.delete_prefix_fail += 1

        sleep(1)

    def results_print(self):
        print(f"Ip add module test passed: {self.add_ip_passed}, failed: {self.add_ip_failed}")
        print(f"Ip check module test passed: {self.check_ip_passed}, failed: {self.check_ip_failed}")
        print(f"Ip delete module test passed: {self.delete_prefix_pass}, failed: {self.delete_prefix_fail}")

    def tearDown(self):
        self.results_print()


if __name__ == '__main__':
    unittest.main()
    print("Done")
