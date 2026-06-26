from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDFS
import re

CRM = "http://www.cidoc-crm.org/cidoc-crm/"
EX_PLACE = "http://example.org/flora-tristan/place/"
CATEGORY = "http://example.org/flora-tristan/feminist_category/"
PLACETYPE = "http://example.org/flora-tristan/place_type/"

GENDER_COLORS = {
    "Feminized": "#b5446e",
    "Masculinized": "#3d6b99",
    "Mixed": "#4a9e6e",
}

CATEGORY_COLORS = {
    "RELIGIOUS_SPACE": "#c9a96e",
    "POLITICAL_SPACE": "#6e8ec9",
    "GENDERED_SPACE": "#c96e9a",
    "PUBLIC_CIVIC_SPACE": "#6ec9a9",
    "ECONOMIC_SPACE": "#c9c06e",
    "CULTURAL_SPACE": "#a06ec9",
    "SYMBOLIC_SPACE": "#c9896e",
    "CARCERAL_SPACE": "#888888",
}

def _short(uri: str) -> str:
    for ns in [EX_PLACE, CATEGORY, PLACETYPE, CRM]:
        if uri.startswith(ns):
            return uri[len(ns):]
    return uri.split("/")[-1].split("#")[-1]

def build_network_data(g: Graph) -> dict:
    """Return nodes + edges dicts for rendering with pyvis."""
    nodes = {}
    edges = []

    E53 = URIRef(f"{CRM}E53_Place")
    E55 = URIRef(f"{CRM}E55_Type")
    E89 = URIRef(f"{CRM}E89_Propositional_Object")
    P2 = URIRef(f"{CRM}P2_has_type")
    P67 = URIRef(f"{CRM}P67_refers_to")
    GENDER_SIG = URIRef(f"{EX_PLACE}genderSignificance")

    for place in g.subjects(URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), E53):
        label_val = g.value(place, RDFS.label)
        label = str(label_val) if label_val else _short(str(place))
        gender = str(g.value(place, GENDER_SIG)) if g.value(place, GENDER_SIG) else "Mixed"
        note_val = g.value(place, URIRef(f"{CRM}P3_has_note"))
        note = str(note_val) if note_val else ""
        color = GENDER_COLORS.get(gender, "#aaaaaa")
        place_id = str(place)
        nodes[place_id] = {
            "id": place_id,
            "label": label,
            "title": f"<b>{label}</b><br>Gender: {gender}<br><i>{note[:120]}...</i>" if len(note) > 120 else f"<b>{label}</b><br>Gender: {gender}<br><i>{note}</i>",
            "color": color,
            "size": 28,
            "group": "place",
            "gender": gender,
        }

        # Category nodes + edges
        for cat_uri in g.objects(place, P2):
            cat_str = str(cat_uri)
            if CATEGORY in cat_str:
                cat_label = _short(cat_str).replace("_", " ").title()
                cat_color = CATEGORY_COLORS.get(_short(cat_str), "#dddddd")
                if cat_str not in nodes:
                    nodes[cat_str] = {
                        "id": cat_str,
                        "label": cat_label,
                        "title": f"Category: {cat_label}",
                        "color": cat_color,
                        "size": 18,
                        "group": "category",
                        "shape": "diamond",
                    }
                edges.append({"from": place_id, "to": cat_str, "label": "hasType", "color": "#cccccc"})

        # Emotion nodes + edges
        emotion_uri = g.value(place, P67)
        if emotion_uri:
            emotion_label_val = g.value(emotion_uri, RDFS.label)
            emotion_label = str(emotion_label_val) if emotion_label_val else _short(str(emotion_uri))
            em_str = str(emotion_uri)
            if em_str not in nodes:
                nodes[em_str] = {
                    "id": em_str,
                    "label": emotion_label,
                    "title": f"Emotional register: {emotion_label}",
                    "color": "#c4a020",
                    "size": 14,
                    "group": "emotion",
                    "shape": "ellipse",
                }
            edges.append({"from": place_id, "to": em_str, "label": "emotionalRegister", "color": "#c4a02066"})

    return {"nodes": list(nodes.values()), "edges": edges}


def build_pyvis_html(g: Graph) -> str:
    from pyvis.network import Network
    net = Network(height="520px", width="100%", bgcolor="#FAF9F6", font_color="#1a1a1a", directed=False)
    net.set_options("""{
      "physics": {"stabilization": {"iterations": 120}},
      "interaction": {"hover": true, "tooltipDelay": 100},
      "edges": {"smooth": {"type": "dynamic"}, "font": {"size": 9, "color": "#aaaaaa"}},
      "nodes": {"font": {"size": 13}}
    }""")
    data = build_network_data(g)
    for n in data["nodes"]:
        net.add_node(
            n["id"], label=n["label"], title=n["title"],
            color=n["color"], size=n["size"],
            shape=n.get("shape", "dot"),
        )
    for e in data["edges"]:
        net.add_edge(e["from"], e["to"], title=e["label"], color=e.get("color", "#aaaaaa"))
    return net.generate_html()
