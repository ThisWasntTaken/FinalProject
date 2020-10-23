from hip import app

if __name__ == "__main__":
    app.run(port = 7000 + app.config['HIP_ID'], debug = True)