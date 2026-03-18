# from flask import Flask, render_template
# from backend.api import app as api_app

# app = Flask(__name__)
# app.register_blueprint(api_app) 

# @app.route("/")
# def home():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, render_template
# from backend.api import api_app  # Ensure api_app is a Blueprint in backend/api.py

# app = Flask(__name__)

# # Register the Blueprint correctly
# app.register_blueprint(api_app, url_prefix="/api")  

# @app.route("/")
# def home():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Blueprint, jsonify

# api_app = Blueprint("api", __name__)  # Create the Blueprint

# @api_app.route("/test", methods=["GET"])
# def test():
#     return jsonify({"message": "API is working!"})






# import sys
# import os
# from flask import Flask, render_template

# # Add backend to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

# # Now import the API Blueprint
# from backend.api import api_app  # Ensure api_app is a Blueprint

# app = Flask(__name__)
# app.register_blueprint(api_app, url_prefix="/api")

# @app.route("/")
# def home():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, render_template
# from backend.api import api_app  # Import the Blueprint, NOT a Flask app

# app = Flask(__name__, template_folder="frontend/templates")
# app.register_blueprint(api_app, url_prefix="/api")  # Correct Blueprint registration

# @app.route("/")
# def home():
#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template
from backend.api import api_app  # Import the Blueprint, NOT a Flask app

app = Flask(__name__, 
            template_folder="frontend/templates",  # Tell Flask where templates are
            static_folder="frontend/static")  # Tell Flask where static files are

app.register_blueprint(api_app, url_prefix="/api")  # Correct Blueprint registration

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
