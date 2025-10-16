from main import app

# AWS Beanstalk looks for an 'application' callable by default
application = app

if __name__ == "__main__":
    application.run()