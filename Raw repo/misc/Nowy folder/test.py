import time

start_time = time.time()

time.sleep(1)

elapsed_time = time.time() - start_time

print(elapsed_time)
print("Hours = " + str(int(elapsed_time / (60*60))) + ":" +  str(int((elapsed_time % (60*60))/60)))