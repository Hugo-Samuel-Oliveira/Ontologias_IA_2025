from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from py2neo import Graph as Neo4jGraph

# --- CONFIGURAÇÕES ---
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "chatbot123" # <<<--- ATUALIZE COM A SUA SENHA
NEO4J_DATABASE = "ifc-chatbot"

class ActionContarElementosNeo4j(Action):
    """Esta ação consulta o Neo4j para contar elementos de um tipo específico."""

    def name(self) -> Text:
        """Nome único da ação, deve corresponder ao domain.yml."""
        return "action_contar_elementos_neo4j"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 1. Obtém a entidade (ex: "IfcWall") da memória da conversa.
        tipo_ifc = tracker.get_slot("tipo_ifc")

        if not tipo_ifc:
            dispatcher.utter_message(text="Não identifiquei o tipo de elemento que você quer contar.")
            return []
        
        # 2. Conecta-se ao Neo4j.
        try:
            graph_db = Neo4jGraph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD), name=NEO4J_DATABASE)
        except Exception as e:
            dispatcher.utter_message(text=f"Não foi possível conectar à base de conhecimento: {e}")
            return []

        # 3. Constrói e executa a consulta Cypher.
        uri_do_tipo = f"http://example.org/ifc/{tipo_ifc}"
        
        query = (
            "MATCH (e:IFCElement)-[:type]->(t:IFCElement) "
            "WHERE t.uri = $uri "
            "RETURN count(e) AS element_count"
        )
        
        result = graph_db.run(query, uri=uri_do_tipo).data()
        
        # 4. Formula e envia a resposta para o utilizador.
        if result:
            count = result[0]['element_count']
            response_text = f"Encontrei {count} elemento(s) do tipo '{tipo_ifc}' no modelo."
        else:
   

         response_text = f"Não encontrei informações sobre elementos do tipo '{tipo_ifc}'."

        dispatcher.utter_message(text=response_text)
        return []