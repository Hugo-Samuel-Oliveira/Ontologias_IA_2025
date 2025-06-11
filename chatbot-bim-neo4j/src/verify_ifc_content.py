import ifcopenshell
from collections import Counter

IFC_FILE_PATH = "C:\\Users\\Samuel\\Documents\\Repositorios\\chatbot-bim-neo4j\\data\\Building-Architecture.ifc"

try:
    model = ifcopenshell.open(IFC_FILE_PATH)
    print(f"Ficheiro '{IFC_FILE_PATH}' carregado com sucesso.\n")

    # Cria um contador para todos os tipos de 'IfcProduct'
    # IfcProduct é a classe base para a maioria dos objetos físicos num modelo BIM
    product_types = [element.is_a() for element in model.by_type("IfcProduct")]
    type_counts = Counter(product_types)

    print("--- Contagem de Tipos de Elementos (IfcProduct) no Ficheiro ---")
    if not type_counts:
        print("Nenhum elemento do tipo IfcProduct encontrado.")
    else:
        # Imprime os resultados de forma organizada
        for element_type, count in sorted(type_counts.items()):
            print(f"- {element_type}: {count}")

except Exception as e:
    print(f"Ocorreu um erro ao ler o ficheiro IFC: {e}")