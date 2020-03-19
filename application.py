from waitress import serve
from app import create_app
import argparse

# A parser to choose the required environment to run the app
parser = argparse.ArgumentParser()
parser.add_argument('-env', '--environment', required=False, default='d')
args = parser.parse_args()

application = create_app(args.environment)


if __name__ == '__main__':
    if args.environment == 'p' or args.environment == 's':
        serve(application, host='0.0.0.0', port=80)
    else:
        application.run()
