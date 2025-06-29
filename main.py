import uvicorn

from api.app import app


def main():
    uvicorn.run(app, port=8080)


if __name__ == "__main__":
    main()
