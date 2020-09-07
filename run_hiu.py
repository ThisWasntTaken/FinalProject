from hiu import app

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-hiu_id')
    args = parser.parse_args()
    hiu_id = args.hiu_id
    app.config['SESSION_COOKIE_NAME'] = "hiu_" + str(hiu_id)
    app.config['HIU_ID'] = int(hiu_id)
    app.run(port = 6000 + app.config['HIU_ID'], debug = True)