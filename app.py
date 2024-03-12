from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

def calculate_search_area(last_known_position, search_radius):
    """
    Function to calculate the search area based on the last known position of the aircraft.
    Args:
        last_known_position (tuple): Tuple containing latitude and longitude of last known position.
        search_radius (float): Radius (in kilometers) around the last known position to search within.
    Returns:
        list: List of latitude and longitude points defining the search area.
    """
    lat, lon = last_known_position
    # Generate random points within the search radius around the last known position
    num_points = 100
    random_points = np.random.uniform(low=-1, high=1, size=(num_points, 2))
    random_points /= np.linalg.norm(random_points, axis=1)[:, np.newaxis]
    random_points *= search_radius
    random_points += np.array([lat, lon])
    return random_points.tolist()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        radius = float(request.form['radius'])
        last_known_position = (latitude, longitude)
        search_area = calculate_search_area(last_known_position, radius)
        return jsonify({'search_area': search_area})
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
