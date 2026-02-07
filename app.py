from flask import Flask, jsonify
from weather import weather_bp
from flasgger import Swagger
from news import news_bp
from ip_location import ip_location_bp

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(weather_bp)
app.register_blueprint(news_bp)
app.register_blueprint(ip_location_bp)

@app.route('/third-party-service', methods=['GET'])
def third_party_service_root():
    """
       Welcome endpoint
       ---
       responses:
         200:
           description: Welcome message
           schema:
             type: object
             properties:
               message:
                 type: string
       """
    return jsonify({'message': 'Welcome to the Third Party Service API'})

if __name__ == '__main__':
    app.run(debug=True, port=7000)