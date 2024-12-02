from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
import random
import math

app = Flask(__name__)
app.secret_key = "your_secret_key" 

authorized_pincodes = {
    "12345": "12345",  # Example: pincode = "12345", password = "12345"
    # Add other pincodes and passwords here
    "201204": "201204"
}

# Predefined unique nearby locations around Modinagar with distinct area names
NEARBY_LOCATIONS = {
    "Modinagar Central": (28.8401, 77.5801),
    "Modinagar West": (28.8345, 77.5789),
    "Modinagar East": (28.8368, 77.5754),
    "Modinagar North": (28.8352, 77.5790),
    "Modinagar South": (28.8371, 77.5812),
    "Modinagar Sector 1": (28.8390, 77.5777),
    "Modinagar Sector 2": (28.8338, 77.5765),
    "Modinagar Sector 3": (28.8322, 77.5749),
    "Modinagar Sector 4": (28.8410, 77.5823),
    "Modinagar Market": (28.8360, 77.5780),
    "Modinagar Park": (28.8340, 77.5760),
    "Modinagar Railway Station": (28.8325, 77.5755),
    "Modinagar Bus Depot": (28.8375, 77.5795),
    "Modinagar Hospital": (28.8400, 77.5805),
    "Modinagar School": (28.8355, 77.5775)
}

# Simulate sensor data for bins
def simulate_sensor_data(num_bins):
    bins = []
    for i in range(num_bins):
        bin_data = {
            "id": f"bin_{i + 1}",
            "fill_level": random.randint(0, 100),
            "location": random.choice(list(NEARBY_LOCATIONS.values()))
        }
        bins.append(bin_data)
    return bins

# Calculate the distance between two coordinates
def calculate_distance(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Radius of the Earth in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Optimize routes by prioritizing bin fill level and proximity to user
def optimize_routes(bins, user_location):
    bins.sort(key=lambda bin: (-bin['fill_level'], calculate_distance(bin['location'], user_location)))
    route = []
    for bin in bins:
        location_name = get_area_name(bin['location'])
        route.append({
            "id": bin['id'],
            "fill_level": f"{bin['fill_level']}%",
            "location_name": location_name
        })
    
    user_location_name = get_area_name(user_location)
    route.insert(0, {
        "id": "user_location",
        "fill_level": "N/A",
        "location_name": user_location_name
    })
    
    return route

# Get the area name based on coordinates
def get_area_name(coordinates):
    for area, coords in NEARBY_LOCATIONS.items():
        if coordinates == coords:
            return area
    return "Unknown Area"

# Simulate user's current location
def get_current_location():
    return (28.8336, 77.5770)  # Default to Modinagar

@app.route('/')
def index():
    return render_template('index.html')  # Login page

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    pincode = data.get('pincode')
    password = data.get('password')

    if pincode in authorized_pincodes and authorized_pincodes[pincode] == password:
        session['logged_in'] = True  # Set the session to logged in
        return jsonify({"success": True, "message": "Login successful"})
    else:
        return jsonify({"success": False, "message": "Invalid login"}), 401

    
@app.route('/post_login')
def post_login():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('post_login.html')  # Render the post-login page

@app.route('/route_optimization')
def route_optimization():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('route_optimization.html')

@app.route('/get_route')
def get_route():
    sensor_data = simulate_sensor_data(10)
    user_location = get_current_location()
    optimized_route = optimize_routes(sensor_data, user_location)
    return jsonify(route=optimized_route)

@app.route('/main')
def main():
    if not session.get('logged_in'):
        return redirect(url_for('index'))  # Redirect to login if not logged in
    return render_template('main.html')  # Render the main route optimization page


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)