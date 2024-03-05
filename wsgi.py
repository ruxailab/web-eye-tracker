from app.main import app
import os

if __name__ == "__main__":
    # app.run(debug=os.environ['FLASK_ENV'])
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
