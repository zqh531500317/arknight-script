
# 支持 py installer
if __name__ == '__main__':
    try:

        from module.app import create_app
    except Exception as e:
        print(e)
    app = create_app()
    app.run(host='0.0.0.0')
