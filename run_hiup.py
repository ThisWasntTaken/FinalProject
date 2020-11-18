from hiup import app

if __name__ == "__main__":
    app.run(port = 6000 + 10 * int(app.config['HIU_ID']) + int(app.config['HIP_ID']), debug = True)