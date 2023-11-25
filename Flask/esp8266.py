from flask import Flask, request
import sqlite3
import time

app = Flask(__name__)
app.debug = True

temperature = None
humidity = None
pressure = None
altitude = None
light = None
uv_intensity = None

def insert_data_to_database():
    conn = sqlite3.connect('condition.db')
    c = conn.cursor()
    
    c.execute("CREATE TABLE IF NOT EXISTS conditions (timestamp TEXT, temperature REAL, humidity REAL, pressure REAL, altitude REAL, light REAL, uv_intensity REAL)")
    current_time = get_current_time()  # Get current time using Python's time library
    # print(current_time)
    c.execute("INSERT INTO conditions VALUES (?, ?, ?, ?, ?, ?, ?)",
              (current_time, temperature, humidity, pressure, altitude, light, uv_intensity))
    
    conn.commit()
    conn.close()

def show_all_data():
    conn = sqlite3.connect('condition.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM conditions")
    items = c.fetchall()
    for item in items:
        print(item)
    
    conn.close()

def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S')  # Format the current time as a string

@app.route('/esp8266', methods=['POST'])
def receive_data():
    if request.method == 'POST':
        data = request.get_json()
        global temperature, humidity, pressure, altitude, light, uv_intensity
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        pressure = data.get('pressure')
        altitude = data.get('altitude')
        light = data.get('light')
        uv_intensity = data.get('UVIntensity')
        # Insert data into the database
        insert_data_to_database()
        # Show all data from the database
        # show_all_data()
        # time.sleep(10)  # Delay for 5 seconds
        return "Data received successfully", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)