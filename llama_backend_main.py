from app import app

# main driver function
if __name__ == '__main__':
    host_ip = "127.0.0.1"
    app.run(host=host_ip, debug=True, port=5001, use_reloader=False)
