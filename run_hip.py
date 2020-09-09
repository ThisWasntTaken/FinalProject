from hip import app

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-hip_id')
    args = parser.parse_args()
    hip_id = args.hip_id
    app.config['SESSION_COOKIE_NAME'] = "hip_" + str(hip_id)
    app.config['hip_ID'] = int(hip_id)
    app.run(port = 7000 + app.config['hip_ID'], debug = True)