import pymysql
from app import app
from config import mysql
from flask import jsonify, request

@app.route('/consultar', methods=['GET'])
def consultar():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id_fabricante, id_produto, codigodebarras, nome_produto, categoria, peso, disponibilidade, valor FROM produtos")
        empRows = cursor.fetchall()
        response = jsonify(empRows)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/consultar/<int:id>', methods=['GET'])
def consultarporid(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id_fabricante, id_produto, codigodebarras, nome_produto, categoria, peso, disponibilidade, valor FROM produtos WHERE id_produto =%s", id)
        empRow = cursor.fetchone()
        response = jsonify(empRow)
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:        
        _json = request.json
        _id_fabricante = _json['id_fabricante']
        _codigodebarras = _json['codigodebarras']
        _nome_produto = _json['nome_produto']
        _categoria = _json['categoria']
        _peso = _json['peso']
        _disponibilidade = _json['disponibilidade']
        _valor = _json['valor']

        if _id_fabricante and _codigodebarras and _nome_produto and _categoria and _peso and _disponibilidade and _valor and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO produtos (id_fabricante, codigodebarras, nome_produto, categoria, peso, disponibilidade, valor) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            bindData = (_id_fabricante, _codigodebarras, _nome_produto, _categoria, _peso, _disponibilidade, _valor)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Produto adicionado com sucesso!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()          
     
@app.route('/atualizar', methods=['PUT'])
def atualizar():
    try:
        _json = request.json
        _id_fabricante = _json['id_fabricante']
        _id_produto = _json['id_produto']
        _codigodebarras = _json['codigodebarras']
        _nome_produto = _json['nome_produto']
        _categoria = _json['categoria']
        _peso = _json['peso']
        _disponibilidade = _json['disponibilidade']
        _valor = _json['valor']

        if _id_fabricante and _codigodebarras and _nome_produto and _categoria and _peso and _disponibilidade and _valor and request.method == 'PUT':			
            sqlQuery = "UPDATE produtos SET id_fabricante=%s, codigodebarras=%s, nome_produto=%s, categoria=%s, peso=%s, disponibilidade=%s, valor=%s WHERE id_produto=%s"
            bindData = (_id_fabricante, _codigodebarras, _nome_produto, _categoria, _peso, _disponibilidade, _valor, _id_produto)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Produto atualizado com sucesso!')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/deletar/<int:id>', methods=['DELETE'])
def deletar(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM produtos WHERE id_produto=%s", id)
		conn.commit()
		response = jsonify('Produto deletado com sucesso!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response
        
if __name__ == "__main__":
    app.run()