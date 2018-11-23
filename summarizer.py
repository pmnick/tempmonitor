
import sys


# expects first argument to be name of log_file.csv
def main():
    max_t = None
    min_t = None
    n = 0
    sum = 0
    log_file = sys.argv[1]

    with open(log_file) as f:
        for line in f.readlines():
            ts, temp = line.split(',')
            temp = float(temp)
            if max_t is None:
                max_t = min_t = temp
            max_t = max(max_t, temp)
            min_t = min(min_t, temp)
            sum += temp
            n += 1

    print 'max: {}'.format(max_t)
    print 'min: {}'.format(min_t)
    print 'avg: {}'.format(sum/n)


if __name__ == "__main__":
    main()
