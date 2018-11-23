max_t = None
min_t = None
n = 0
sum = 0

with open('temp_log_2_archive_1.txt') as f:
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



