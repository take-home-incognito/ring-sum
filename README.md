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

# notes the second

(after getting the 10-second version working/tested)

Couple things about the above - the ring buffer thing is less relevant than I thought
when one does not have a continuous input stream It's a similar idea, but with manual cleanup
on each request.

Also, the resolution thing isn't terribly pressing, since it's a simple timedelta comparison
we get the python default (ms, I think? would have to check) for free.

# further development ideas

- as noted in code, I don't do much parsing/validation of incoming requests, that's a no-go outside of theoretical exercise land
- memory could be a real concern in a production-type scenario, unless we have some restrictions on input
- things also get very interesting in a distributed model, I haven't addressed that at all
- performance would be greatly improved (on realistic loads, at least) by using a "bucketing" strategy
  - "last hour" = last 60 minutes, give each one a bucket.
    - *61* buckets total, since N and N-60 will both contain portions-of-a-minute that are relevant
  - each "bucket" is effectively a linked list, with each node containing a value and a timestamp
  - in addition to the linked list, a bucket knows its sum total
  - on a GET request, we can simply sum the totals of buckets N-59 through N-1 (inclusive) with the (more expensive to calcluate) partial totals of buckets N and N-60.
  - I would also see about having a cron job (or scheduled GET ping?) every second to handle the "manual" updating of data structures I do now. Being able to clean up the data structures every second on the second would be extremely useful.

# final cleanup notes

- really glad I remember deques exist, that makes me feel way better about performance
- docstrings are always nice for cleaning up a file before merge
- I definitely think my "next steps" would be input handling / error responses
