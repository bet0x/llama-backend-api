from app import app

# main driver function
if __name__ == '__main__':
    host_ip = "0.0.0.0"
    app.run(host=host_ip, debug=True, port=5720, use_reloader=False)
