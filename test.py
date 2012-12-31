import re

if __name__ == "__main__":
    test1 = " version = '1.2.3' "
    test2 = " version = u'1.2.3' "
    test3 = ' version = "1.2.3" '
    test4 = " version='1.2.3' "
    test5 = " self.version='1.2.3' "
    test6 = " version='1.0' "
    test7 = " version='10' "

    pattern = r'version\s*=\s*\D+([\d.][\d.][\d.]+\d+?)'
    # old_pattern = r'version\s*=\s*\D+([\d.]*\d+)'
    tests = [test1, test2, test3, test4, test5, test6, test7]
    for test in tests:
        print repr(re.findall(pattern, test))