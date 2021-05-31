import pymysql
from app import app
from config import mysql, auth
from flask import jsonify, Response
from flask import flash, request
from contextlib import closing

basic_auth = auth

#Criando as Rotas API para a Tabela Clientes
@app.route('/clientes', methods = ['POST'])
@basic_auth.required
def add_clientes():
	try:
		_json = request.get_json(force = True)
		_id = _json['id']
		_nome = _json['nome']
		_cpf = _json['cpf']
		_email = _json['email']
		_senha = _json['senha']		
		if _nome and _cpf and _email and _senha and request.method == 'POST':			
			sqlQuery = "INSERT INTO cadastro.cliente(id, nome, cpf, email, senha) VALUES(%s, %s, %s, %s, %s)"
			bindData = ( _id, _nome, _cpf, _email, _senha)
			with closing(mysql.connect()) as conn:
				with closing(conn.cursor()) as cursor:
					conn = mysql.connect()
					cursor = conn.cursor(pymysql.cursors.DictCursor)
					cursor.execute(sqlQuery, bindData)
					conn.commit()
					response = jsonify('Employee added successfully!')
					response.status_code = 200
					return response
		else:
			return not_found()
	except Exception as e:
		print(e)
		
@app.route('/clientes', methods = ['GET'])
@basic_auth.required
def clientes():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT id, nome, cpf, email, senha FROM cadastro.cliente")
		userRows = cursor.fetchall()
		response = jsonify(userRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/clientes/<int:id>', methods =['GET'])
@basic_auth.required
def clientes2(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT id, nome, cpf, email, senha FROM cadastro.cliente WHERE id = {}".format(id))
		userRows = cursor.fetchone()
		if not userRows:
			return Response('Usuário não encontrado!', status = 404)
		response = jsonify(userRows)
		response.status_code = 200
		return response

	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/clientes', methods=['PUT'])
@basic_auth.required
def update_clientes():
	try:
		_json = request.get_json(force = True)
		_id = _json['id']
		_nome = _json['nome']
		_cpf = _json['cpf']
		_email = _json['email']
		_senha = _json['senha']
		if _nome and _cpf and _email and _senha and _id and request.method == 'PUT':
			sqlQuery = "UPDATE cadastro.cliente SET nome=%s, cpf=%s, email=%s, senha=%s WHERE id=%s"
			bindData = (_nome, _cpf, _email, _senha, _id)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			response = jsonify('User updated successfully!')
			response.status_code = 200
			return response
		else:
			return not_found()

	except Exception as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

@app.route('/clientes/<int:id>', methods=['DELETE'])
@basic_auth.required
def delete_clientes(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM cadastro.cliente WHERE id ={}".format(id))
		conn.commit()
		response = jsonify('Employee deleted successfully!')
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#Criando as Rotas API para relação JOIN Cliente e Endereço
@app.route('/clientes/<int:id>/enderecos')
@basic_auth.required
def ligacao_cliente_enderecos(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("select cadastro.cliente.nome, cadastro.endereco.rua, cadastro.endereco.numero, cadastro.endereco.bairro, cadastro.endereco.cidade, cadastro.endereco.estado, cadastro.endereco.cep from cadastro.cliente join cadastro.endereco on cadastro.cliente.id = cadastro.endereco.idCliente where cadastro.cliente.id = {}".format(id))
		userRows = cursor.fetchall()
		if not userRows:
			return Response('Endereço do usuário não encontrado!', status = 404)
		response = jsonify(userRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.errorhandler(404)
@basic_auth.required
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)