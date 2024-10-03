from flask import Flask, render_template, jsonify
import random
import numpy as np

app = Flask(__name__)

# Simulate sensor data for garbage bins within India
def simulate_sensor_data(num_bins):
    bins = []
    for i in range(num_bins):
        bin_data = {
            "id": f"bin_{i + 1}",
            "fill_level": random.randint(0, 100),  # Fill level in percentage
            "location": (round(random.uniform(6.0, 37.0), 4), round(random.uniform(68.0, 97.0), 4))  # Coordinates within India
        }
        bins.append(bin_data)
    return bins

# Function to optimize routes based on fill levels (descending order)
def optimize_routes(bins):
    # Sort bins by fill level in descending order
    sorted_bins = sorted(bins, key=lambda x: x['fill_level'], reverse=True)

    route = []
    van_path = []
    current_location = np.array([0, 0])  # Starting point (0, 0)
    van_path.append("Start at (0, 0)")

    # Traverse through bins sorted by fill level
    for bin in sorted_bins:
        van_path.append(f"Go to {bin['id']} at location {bin['location']} - Fill Level: {bin['fill_level']}%")
        current_location = bin['location']  # Move to bin location

    van_path.append(f"End at location {current_location}")
    return route, van_path

# Flask route to serve the web page
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to get bin data and van route
@app.route('/get_route')
def get_route():
    sensor_data = simulate_sensor_data(10)  # Simulate data for 10 bins
    _, van_path = optimize_routes(sensor_data)
    return jsonify(van_path)

if __name__ == '__main__':
    app.run(debug=True)
