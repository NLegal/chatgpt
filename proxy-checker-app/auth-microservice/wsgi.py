from auth_microservice.app import app

app = create_app()

if __name__ == '__main__':
    app.run()
