from datetime import datetime, timedelta

from flask import Flask, request

app = Flask(__name__)

live_data = {}
data_shape_str = """
example after (correctly) posting 12345 to key "meow" twice:
{
    "meow":
        [
            [
                (12345, <first_timestamp>),
                (12345, <second_timestamp>)
            ],
            24690
        ]
}
"""

def _remove_old_data(key, timestamp):
    for entry in live_data[key][0]:
        if timestamp - entry[1] > timedelta(seconds=10):
            live_data[key][1] -= entry[0]
            live_data[key][0].remove(entry)
        else:
            break  # elements are in order!
    if len(live_data[key][0]) == 0:
        del live_data[key]

@app.route("/metric/<key>/", methods=["POST"])
def store_value(key):
    data = request.get_json()
    value = data.get('value', None)
    if value is not None:
        if key not in live_data.keys():
            live_data[key] = [[], 0]
        now = datetime.now()
        live_data[key][0].append((value, now))
        live_data[key][1] += value
        _remove_old_data(key, now)
        return {}, 200
    else:  # TODO: handle errors/validation with proper HTTP codes
        return {}, 500


@app.route("/metric/<key>/sum", methods=["GET"])
def read_value(key):
    try:
        _remove_old_data(key, datetime.now())
    except KeyError:
        pass  # key wasn't previously recorded, we'll return 0 below

    ret_value = live_data.get(
        key,
        ([], 0)
    )[1]
    return {"value": ret_value}, 200
