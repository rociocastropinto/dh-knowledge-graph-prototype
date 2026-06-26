from rdflib import Graph
import pandas as pd

_graph = None

def load_graph(ttl_path: str) -> Graph:
    global _graph
    if _graph is None:
        _graph = Graph()
        _graph.parse(ttl_path, format="turtle")
    return _graph

QUERIES = {
    "All places with gender significance": """
        PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ex: <http://example.org/flora-tristan/place/>

        SELECT ?label ?genderSignificance ?note
        WHERE {
            ?place a crm:E53_Place ;
                   rdfs:label ?label ;
                   ex:genderSignificance ?genderSignificance .
            OPTIONAL { ?place crm:P3_has_note ?note . }
        }
        ORDER BY ?genderSignificance ?label
    """,

    "Places by spatial category": """
        PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX category: <http://example.org/flora-tristan/feminist_category/>

        SELECT ?label ?category
        WHERE {
            ?place a crm:E53_Place ;
                   rdfs:label ?label ;
                   crm:P2_has_type ?typeURI .
            ?typeURI rdfs:label ?category .
            FILTER(STRSTARTS(STR(?typeURI), "http://example.org/flora-tristan/feminist_category/"))
        }
        ORDER BY ?label
    """,

    "Emotional register per place": """
        PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ex: <http://example.org/flora-tristan/place/>

        SELECT ?label ?emotion ?genderSignificance
        WHERE {
            ?place a crm:E53_Place ;
                   rdfs:label ?label ;
                   ex:genderSignificance ?genderSignificance ;
                   crm:P67_refers_to ?emotionObj .
            ?emotionObj rdfs:label ?emotion .
        }
        ORDER BY ?label
    """,

    "Masculinized political spaces": """
        PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ex: <http://example.org/flora-tristan/place/>
        PREFIX category: <http://example.org/flora-tristan/feminist_category/>

        SELECT ?label ?note
        WHERE {
            ?place a crm:E53_Place ;
                   rdfs:label ?label ;
                   ex:genderSignificance "Masculinized"@en ;
                   crm:P2_has_type category:POLITICAL_SPACE .
            OPTIONAL { ?place crm:P3_has_note ?note . }
        }
    """,

    "Religious spaces and their gendering": """
        PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ex: <http://example.org/flora-tristan/place/>
        PREFIX category: <http://example.org/flora-tristan/feminist_category/>

        SELECT ?label ?genderSignificance ?emotion
        WHERE {
            ?place a crm:E53_Place ;
                   rdfs:label ?label ;
                   ex:genderSignificance ?genderSignificance ;
                   crm:P2_has_type category:RELIGIOUS_SPACE ;
                   crm:P67_refers_to ?emotionObj .
            ?emotionObj rdfs:label ?emotion .
        }
        ORDER BY ?genderSignificance
    """,
}

def run_query(graph: Graph, query_name: str) -> pd.DataFrame:
    query = QUERIES[query_name]
    results = graph.query(query)
    cols = [str(v) for v in results.vars]
    rows = []
    for row in results:
        rows.append([str(v) if v is not None else "" for v in row])
    return pd.DataFrame(rows, columns=cols)
