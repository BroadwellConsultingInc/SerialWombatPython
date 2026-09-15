import SW18B_UnitTest_globals


def _wrandom(seed):
    # Deterministic 32-bit xorshift used by the Arduino unit tests.
    x = seed[0] & 0xFFFFFFFF
    x ^= (x << 13) & 0xFFFFFFFF
    x ^= (x >> 17) & 0xFFFFFFFF
    x ^= (x << 5) & 0xFFFFFFFF
    seed[0] = x & 0xFFFFFFFF
    return seed[0]


def echoTest(sw):
    seed = [1]

    for i in range(5000):
        passed = True
        tx = bytearray(8)

        for b in range(1, 8):
            tx[b] = _wrandom(seed) & 0x1F

        tx[0] = ord('!')

        count, rx = sw.sendPacket(tx)
        rx = bytearray(rx)

        if len(rx) < 8:
            passed = False
        else:
            if rx[0] != ord('!'):
                passed = False

            for b in range(1, 8):
                if tx[b] != rx[b]:
                    passed = False

        if passed:
            SW18B_UnitTest_globals.pass_(i)
        else:
            SW18B_UnitTest_globals.fail(i)
