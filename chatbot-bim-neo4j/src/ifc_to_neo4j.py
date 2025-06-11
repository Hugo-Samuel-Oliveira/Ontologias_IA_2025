import ifcopenshell
from rdflib import Graph as RdfGraph, Namespace, URIRef, Literal, RDF
from py2neo import Graph as Neo4jGraph
import re
import logging

# Configuração de logging para um feedback claro do processo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURAÇÕES ---
IFC_FILE_PATH = "C:\\Users\\Samuel\\Documents\\Repositorios\\chatbot-bim-neo4j\\data\\Building-Architecture.ifc"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "chatbot123" # <<<--- ATUALIZE COM A SUA SENHA
NEO4J_DATABASE = "ifc-chatbot"

logging.info("Iniciando o processo de importação do IFC para o Neo4j...")

# --- 1. CONECTAR AO NEO4J ---
try:
    graph_db = Neo4jGraph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD), name=NEO4J_DATABASE)
    graph_db.delete_all()
    logging.info(f"Conectado ao Neo4j e o banco de dados '{NEO4J_DATABASE}' foi limpo.")
except Exception as e:
    logging.error(f"Não foi possível conectar ao Neo4j. Verifique as suas credenciais e se o banco está ativo. Erro: {e}")
    exit()

# --- 2. CARREGAR O MODELO IFC ---
try:
    model = ifcopenshell.open(IFC_FILE_PATH)
    # CORREÇÃO: A linha abaixo foi alterada para não usar len(model), que causa o erro.
    logging.info(f"Modelo IFC carregado com sucesso. A processar entidades...")
except Exception as e:
    # A exceção real estava a ser mascarada. O erro agora seria mais claro se ifcopenshell.open falhasse.
    logging.error(f"Não foi possível abrir ou processar o arquivo IFC em '{IFC_FILE_PATH}'. Erro: {e}")
    exit()

# --- 3. CRIAR GRAFO RDF INTERMEDIÁRIO ---
# Esta etapa usa o padrão RDF para estruturar os dados antes de enviá-los ao Neo4j
ns = Namespace("http://example.org/ifc/")
rdf_graph = RdfGraph()

# ALTERAÇÃO: Em vez de selecionar apenas "IfcProduct", iteramos por TUDO no modelo.
# Depois, filtramos apenas os elementos que têm um GlobalId, que é o que nos interessa.
# Isso garante que não perdemos nenhum elemento como Portas, Janelas, etc.
elementos_com_id = 0
for element in model:
    if hasattr(element, "GlobalId") and element.GlobalId:
        elementos_com_id += 1
        uri = URIRef(ns[element.GlobalId])
        rdf_graph.add((uri, RDF.type, URIRef(ns[element.is_a()])))
        if hasattr(element, "Name") and element.Name:
            rdf_graph.add((uri, ns["name"], Literal(element.Name)))

logging.info(f"Grafo RDF intermediário gerado com {len(rdf_graph)} triplas a partir de {elementos_com_id} entidades com GlobalId.")


# --- 4. ENVIAR PARA O NEO4J ---
# Itera sobre as triplas RDF e as traduz para consultas Cypher
tx = graph_db.begin()
for s, p, o in rdf_graph:
    def sanitize_relation_name(predicate):
        name = str(predicate).split("/")[-1].split("#")[-1]
        return re.sub(r'\W|^(?=\d)', '_', name)

    s_uri = str(s)
    pred_sanitized = sanitize_relation_name(p)

    if isinstance(o, URIRef):
        o_uri = str(o)
        query = (
            f"MERGE (a:IFCElement {{uri: $s_uri}}) "
            f"MERGE (b:IFCElement {{uri: $o_uri}}) "
            f"MERGE (a)-[r:{pred_sanitized}]->(b)"
        )
        tx.run(query, s_uri=s_uri, o_uri=o_uri)
    else:
        o_val = str(o)
        query = (
            f"MERGE (a:IFCElement {{uri: $s_uri}}) "
            f"SET a.{pred_sanitized} = $o_val"
        )
        tx.run(query, s_uri=s_uri, o_val=o_val)
graph_db.commit(tx)
logging.info("Grafo carregado com sucesso no Neo4j!")