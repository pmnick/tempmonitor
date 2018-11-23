import sys
import os
import calendar
from datetime import datetime
from terminalplot import plot
from bashplotlib.histogram import plot_hist


def parse_line(line):
    str_time, str_temp = line.split(',')
    time = datetime.strptime(str_time, '%Y-%m-%dT%H:%M:%S.%f')
    ts = calendar.timegm(time.timetuple())
    return (ts, float(str_temp.strip()))

# expects first argument to be name of log_file.csv
def main():
    try:
        log_file = sys.argv[1]
    except IndexError:
        sys.exit('Aborted Execution: expected argument specifiying log file to summarize')

    # structure data for histogram and line plot
    x, y = [], []
    with open(log_file, 'r') as f:
        with open('logs/hist.csv', 'w') as hf:
            for line in f.readlines():
                time, temp = parse_line(line)
                # save data to file with single column for histogram
                hf.write('{}\n'.format(temp))

                # populate x and y for line chart
                x.append(time)
                y.append(temp)

    print('SUMMARY OF {}'.format(log_file))
    print('------------------------------------------')
    plot_hist('logs/hist.csv', bincount=100, xlab=True, showSummary=True)
    print('')
    print('------------------------------------------')
    print('')
    plot(x, y)

    os.remove('logs/hist.csv')

if __name__ == "__main__":
    main()
