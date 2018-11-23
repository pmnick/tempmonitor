import sys
import os
from bashplotlib.histogram import plot_hist

# expects first argument to be name of log_file.csv
def main():
    try:
        log_file = sys.argv[1]
        print('log_file {}'.format(log_file))
    except IndexError:
        sys.exit('Aborted Execution: expected argument specifiying log file to summarize')

    with open(log_file, 'r') as f:
        with open('logs/hist.csv', 'w') as hf:
            for line in f.readlines():
                _, temp = line.split(',')
                hf.write('{}\n'.format(temp.strip())) # already includes ne

    plot_hist('logs/hist.csv', bincount=100, xlab=True, showSummary=True)

    os.remove('logs/hist.csv')

if __name__ == "__main__":
    main()
