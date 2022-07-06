# Secret Message Simulations
Simulations that transmit bits of a message based on the timely removal of packets from a buffer. These times are based on either an 
exponential or uniform distribution (exponential.py vs uniform.py)

The buffer also receives these packets from a source that generates them at different times depending on the distribution

Given a maximum buffer size of 20 packets, we can adjust parameters like the number of bits in a message and the initial number of
packets in the buffer to determine the probability of the buffer overflowing (number of packets in the buffer exceeds the max capacity)
and the probability of the buffer underflowing (a packet needs to be removed from the buffer to transmit a bit but the buffer is empty)

For a chosen set of parameters, the simulation is run 500 times to ensure valid results which are then tabulated for easy viewing
