#!/usr/bin/env python
#
#  testing_exceptions.py
#  
#  Copyright 2026 svicente <svicente@svicente-linux-SP>
#  


try:
    entrada_usuario = int(input("Digite a sua idade: "))
    
    vl_divisao = 100/entrada_usuario
    print(vl_divisao)
    #soma = vl_divisao + "Sergio"
except ValueError as except_ve:
    print('Você não digitou um número inteiro válido!')
    print("Detalhes do erro: ", except_ve)
except TypeError as except_te:
    print('Você não pode dividir um número por uma string')
    print("Detalhes do erro: ", except_te)
except Exception as except_generic:
    print("Detalhes do erro: ", except_generic)
    
finally:
    print('Código encerrado')    
    
    

