import print_progress

from time import sleep

# make a list
items = list(range(0, 57))
i = 0
l = len(items)

# Initial call to print 0% progress
print_progress.print_progress(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
for item in items:
    # Do stuff...
    sleep(0.1)
    # Update Progress Bar
    i += 1
    print_progress.print_progress(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
