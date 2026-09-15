import SW18B_UnitTest_globals
import SerialWombatQueue


QUEUETEST_MAX_QUEUE_SIZE = 513
QUEUE_TEST_NUMBER_ITERATIONS = 1000
QUEUE_TIMEOUT_MS = 10


class _ReferenceQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self._data = []

    def push(self, value):
        if len(self._data) >= self.capacity:
            return False

        self._data.append(value & 0xFF)
        return True

    def pop(self):
        if len(self._data) == 0:
            return None

        return self._data.pop(0)

    def count(self):
        return len(self._data)

    def peek(self):
        if len(self._data) == 0:
            return -1

        return self._data[0]


def _wrandom(seed):
    # Deterministic 32-bit xorshift used to reproduce the Arduino test's
    # pseudo-random action/data pattern from a mutable seed.
    x = seed[0] & 0xFFFFFFFF
    x ^= (x << 13) & 0xFFFFFFFF
    x ^= (x >> 17) & 0xFFFFFFFF
    x ^= (x << 5) & 0xFFFFFFFF
    seed[0] = x & 0xFFFFFFFF
    return seed[0]


def _test(designator, value, expected):
    SW18B_UnitTest_globals.test_value(designator, value, expected, 0, 0)




def queueTest(sw):
    queueSizeMax = QUEUETEST_MAX_QUEUE_SIZE
    queueSizeMin = 4
    if sw is SW18B_UnitTest_globals.SW8B_68:
        queueSizeMax = 80

    for queueSize in range(queueSizeMin, queueSizeMax):
        print(f"Queue test: Queue size: {queueSize}")
        swq = SerialWombatQueue.SerialWombatQueue(sw)
        q = _ReferenceQueue(queueSize)

        lfsrSeed = [queueSize]
        queueOffset = _wrandom(lfsrSeed)
        queueOffset &= 0x3FE  # Up to 1022, even numbers
        if sw is SW18B_UnitTest_globals.SW8B_68:
            queueOffset &= 0xE  # Up to 14

        swq.begin(queueOffset, queueSize)
        swq.setTimeout(QUEUE_TIMEOUT_MS)

        for iteration in range(QUEUE_TEST_NUMBER_ITERATIONS):
            action = _wrandom(lfsrSeed)

            if (action >> 30) == 0:  # Add to queue
                count = action % queueSize

                aqSuccess = 0
                queuetempData = bytearray(count)
                for x in range(count):
                    queuetempData[x] = _wrandom(lfsrSeed) & 0xFF

                    if q.push(queuetempData[x]):
                        aqSuccess += 1

                swqSuccess = swq.writeBuffer(queuetempData, count)

                s = f"Q write: it: {iteration}, count: {count}, aq: {aqSuccess}, sw: {swqSuccess}"
                _test(s, swqSuccess, aqSuccess)
                if swqSuccess != aqSuccess:
                    break

            elif (action >> 30) == 1:  # Remove from queue
                count = action % queueSize

                aqSuccess = 0
                queuetempData = bytearray(count)
                for x in range(count):
                    value = q.pop()
                    if value is not None:
                        queuetempData[aqSuccess] = value
                        aqSuccess += 1

                swqTempData = swq.readBytes( aqSuccess)
                swqSuccess = len(swqTempData)

                s = f"Q read count check: it: {iteration}, count: {count}, aq: {aqSuccess}, sw: {swqSuccess}"
                _test(s, swqSuccess, aqSuccess)
                if swqSuccess == aqSuccess:
                    for x in range(aqSuccess):
                        s = f"Q read: it: {iteration}, count: {count}, aq: {aqSuccess}, sw: {swqSuccess}, x: {x}"
                        _test(s, swqTempData[x], queuetempData[x])
                else:
                    break

            elif (action >> 30) == 2:  # Check filled bytes
                s = f"Q count: it: {iteration} "
                _test(s, swq.available(), q.count())

            elif (action >> 30) == 3:  # Check peek
                s = f"Q peek: it: {iteration} "
                _test(s, swq.peek(), q.peek())
