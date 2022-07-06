from tabulate import tabulate
import random
import math

# i = number of initial packets in buffer
# m = number of bits in bit sequence
# sims = number of simulations to be performed
i = [2, 6, 10, 14, 18]
m = [16, 32]
sims = 500

# Creates a random string of 1's and 0's based on m 
# and generates a sequence of times when packets will
# be transmitted based on an exponential distribution
def message_encode(m, exp_median, message_times):
    message = ""
    i = 0
    # generate sequence of bits
    for x in range(m):
        message += str(random.randint(0,1))
            
    # determine times when packets are released from buffer based on bit
    for y in message:
        if y == '0':
            message_times.append(message_times[i] + random.uniform(0, exp_median))
        else:
            message_times.append(message_times[i] + random.uniform(exp_median, 5))
        i += 1

# Generates a sequence of times at which the source
# will generate packets that will be sent to the buffer
# (based on exponential distribution)
def source_generate(i, m, exp_max, exp_rate, source_times):
    # keep generating times until the max amount of time is exceeded 
    while source_times[i] < m * exp_max:
        val = random.expovariate(exp_rate)
        # ensure value does not exceed max exponential value
        if val <= exp_max:
            source_times.append(source_times[i] + val)
            i += 1
        
# Runs one instance of simulation and determines
# if a buffer overflow/underflow/neither occured
def run(B, CB, message_times, source_times, overflow, underflow):
    count = 0
    for i in message_times:
        add_to_buffer = 0
        # add packets from source to buffer first
        while source_times[count] <= i:
            add_to_buffer += 1
            count += 1
        CB += add_to_buffer
        # now check for buffer overflow/underflow
        if CB > B:
            overflow.append(1)
            underflow.append(0)
            return
        if CB == 0:
            overflow.append(0)
            underflow.append(1)
            return
        CB -= 1 # release packet from buffer
    # end of loop, no overflow/underflow
    overflow.append(0)
    underflow.append(0)
            
# Main function to run the 500 simulations
# and determine probabilities of buffer
# overflow and underflow
def simulate(i_val, m_val, sims):
    B = 20 # max size of the buffer
    exp_max = 5 # max value of exponential distribution
    exp_rate = 1 # exponential distribution rate
    exp_median = -math.log(0.5) # median value of exponential distribution
    overflow = []
    underflow = []

    #run simulation 500 times
    for i in range(sims):
        CB = i_val # current size of the buffer
        message_times = [0]
        source_times = [0]
        message_encode(m_val, exp_median, message_times)
        source_generate(0, m_val, exp_max, exp_rate, source_times)
        run(B, CB, message_times, source_times, overflow, underflow)
            
    # calculate overflow/underflow probabilities
    overflow_prob = 0
    underflow_prob = 0
    for i in overflow:
        overflow_prob += i
    for j in underflow:
        underflow_prob += j
    overflow_prob = overflow_prob / sims
    underflow_prob = underflow_prob / sims
    return overflow_prob, underflow_prob

# Create a tabulated table of data
table = []
for m_val in m:
    for i_val in i:
        overflow_p, underflow_p = simulate(i_val, m_val, sims)
        row = [m_val, i_val, overflow_p, underflow_p]
        table.append(row)

print(tabulate(table, headers=["m","i", "P(Overflow)", "P(Underflow)"]))
