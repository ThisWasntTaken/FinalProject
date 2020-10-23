from hiu import app

if __name__ == "__main__":
    app.run(port = 6000 + app.config['HIU_ID'], debug = True)