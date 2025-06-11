# Ontologias_IA_2025

Este repositório no GitHub serve como um hub central para o desenvolvimento e a documentação das ontologias do projeto [Insira o Nome do Projeto]. Aqui, você encontrará todos os arquivos e artefatos relacionados à modelagem de conhecimento, cobrindo uma ampla gama de assuntos pertinentes aos nossos objetivos.

Uma das nossas principais iniciativas atuais é a implementação do Plano Mestre para um Chatbot de Projetos BIM, que utiliza Rasa e Neo4j.

Este projeto consiste em desenvolver um assistente virtual inteligente, projetado para consultar as informações complexas de modelos BIM. Para isso, estamos utilizando uma arquitetura robusta que inclui:

Neo4j: Como nossa base de conhecimento, modelando os dados do BIM em um banco de dados em grafo para capturar as ricas interconexões entre os elementos do projeto.
Python com ifcopenshell: Para processar os arquivos IFC e alimentar nosso grafo de conhecimento.
Rasa Open Source: Como a plataforma de IA conversacional que entende as perguntas dos usuários e busca as respostas no Neo4j.
O plano de execução é dividido em fases detalhadas, começando pela configuração completa do ambiente de desenvolvimento, passando pela construção do grafo de conhecimento a partir de um modelo IFC, até a configuração do chatbot em Rasa e a implementação de ações customizadas que conectam a conversa do usuário com as consultas ao banco de dados.