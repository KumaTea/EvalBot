def analyze_stat(stat: str):
    used_time = ''
    peak_mem = ''
    for line in stat.split('\n'):
        if 'Elapsed (wall clock) time (h:mm:ss or m:ss)' in line:
            used_time = line.split(': ')[1]
        elif 'Maximum resident set size (kbytes): ' in line:
            peak_mem = line.split(': ')[1]
    return used_time, peak_mem
