from projeto import app #da pasta projeto, importe o arquivo __init__ 


# essa linha abaixo poderia ser apenas "app.run()", sem o if, que funcionaria
if __name__ == "__main__": #Se eu executar o arquivo main, é pra executar app.run()
    app.run(debug=True)