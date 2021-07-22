from collections import deque
from datetime import datetime, timedelta

from flask import Flask, request


app = Flask(__name__)


SUM_SINCE_TIMEDELTA = timedelta(hours=1)


live_data = {}
__data_shape_str = """
example of live_data after (correctly) posting 12345 to key "meow" twice:
{
    "meow":
        [
            [  # this layer is now a deque, not just a list
                (12345, <first_timestamp>),
                (12345, <second_timestamp>)
            ],
            24690
        ]
}
"""



def _remove_old_data(key, timestamp):
    """
    Clean up the current sum for the given metric.

    Removes all entries of live_data[key] with a timestamp
    more than SUM_SINCE_TIMEDELTA before timestamp.
    """
    active_deque, _current_sum = live_data[key]
    try:
        while timestamp - active_deque[0][1] > SUM_SINCE_TIMEDELTA:
            tuple_to_drop = active_deque.popleft()
            live_data[key][1] -= tuple_to_drop[0]

    except IndexError:  # assumed to mean "you removed them all"
        del live_data[key]

@app.route("/metric/<key>/", methods=["POST"])
def store_value(key):
    """
    Store and sum a POSTed value for the given metric.

    Accepts data of shape { "value": 12345 }.
    """
    data = request.get_json()
    value = data.get('value', None)

    if value is not None:
        now = datetime.now()

        if key not in live_data.keys():
            live_data[key] = [deque(), 0]

        live_data[key][0].append((value, now))
        live_data[key][1] += value

        _remove_old_data(key, now)

        return {}, 200

    else:  # TODO: handle errors/validation with proper HTTP codes
        return {}, 500


@app.route("/metric/<key>/sum", methods=["GET"])
def read_value(key):
    """
    Return the sum total for a given key.

    Will update current sum to respect SUM_SINCE_TIMEDELTA relative to now.
    """
    try:
        _remove_old_data(key, datetime.now())
    except KeyError:
        pass  # key wasn't previously recorded, we'll return 0 below

    ret_value = live_data.get(
        key,
        [None, 0]
    )[1]

    return {"value": ret_value}, 200
