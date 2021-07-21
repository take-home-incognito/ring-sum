# ring-sum
take home coding challenge july 2021

# notes the first

(written after I got my routes confirmed working, before any actual "problem solving")

So the "trick" here is the same thing your smart speakers do - if you *know*
you only care about the past N time periods (1 hour for us, 5 seconds for your speaker),
you can store an incoming data stream in a "ring buffer". Effectively, we're going to
reserve space for a full set of N time periods, then store our data in the reserved
space at location (current_time % size_of_buffer).

Because the problem as stated is very hard to test (I'm not gonna sit here for >1 hours
of manual testing), I'm going to start out by solving a smaller problem. Once my
"sum from the last 10 seconds" code is working and I'm happy with my tests, I'll scale up.

Resolution is also going to be kind of tricky - to start, I'll say "last 10 seconds" means
"when rounded to the nearest second, all events that are <= 10 seconds ago". I anticipate
this getting to miliseconds pretty easily before submission.
