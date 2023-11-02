import pymysql
from app import app
from config import mysql
from flask import jsonify, request


@app.route('/consultar', methods=['GET'])
def consultar():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id_produto, categoria, codigodebarras, descricao_produto, marca_produto, nome_mercado, valor_produto FROM produtos")
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
        cursor.execute("SELECT id_produto, categoria, codigodebarras, descricao_produto, marca_produto, nome_mercado, valor_produto FROM produtos WHERE id_produto =%s", id)
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
        _categoria = _json['categoria']
        _codigodebarras = _json['codigodebarras']
        _descricao_produto = _json['descricao_produto']
        _marca_produto = _json['marca_produto']
        _nome_mercado = _json['nome_mercado']
        _valor_produto = _json['valor_produto']

        if _categoria and _codigodebarras and _descricao_produto and _marca_produto and _nome_mercado and _valor_produto and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO produtos (categoria, codigodebarras, descricao_produto, marca_produto, nome_mercado, valor_produto) VALUES (%s, %s, %s, %s, %s, %s)"
            bindData = (_categoria, _codigodebarras, _descricao_produto, _marca_produto, _nome_mercado, _valor_produto)            
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
        _id_produto = _json['id_produto']
        _categoria = _json['categoria']
        _codigodebarras = _json['codigodebarras']
        _descricao_produto = _json['descricao_produto']
        _marca_produto = _json['marca_produto']
        _nome_mercado = _json['nome_mercado']
        _valor_produto = _json['valor_produto']

        if _categoria and _codigodebarras and _descricao_produto and _marca_produto and _nome_mercado and _valor_produto and request.method == 'PUT':			
            sqlQuery = "UPDATE produtos SET categoria=%s, codigodebarras=%s, descricao_produto=%s, marca_produto=%s, nome_mercado=%s, valor_produto=%s WHERE id_produto=%s"
            bindData = (_categoria, _codigodebarras, _descricao_produto, _marca_produto, _nome_mercado, _valor_produto, _id_produto)
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