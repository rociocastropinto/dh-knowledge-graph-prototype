import re
import folium
from rdflib import Graph, URIRef

CRM = "http://www.cidoc-crm.org/cidoc-crm/"
EX_PLACE = "http://example.org/flora-tristan/place/"
GEO = "http://www.opengis.net/ont/geosparql#"

GENDER_ICON_COLORS = {
    "Feminized": "pink",
    "Masculinized": "blue",
    "Mixed": "green",
}

def build_map(g: Graph) -> folium.Map:
    m = folium.Map(location=[-12.047, -77.030], zoom_start=14, tiles="CartoDB dark_matter")

    E53 = URIRef(f"{CRM}E53_Place")
    P168 = URIRef(f"{CRM}P168_place_is_defined_by")
    P3 = URIRef(f"{CRM}P3_has_note")
    P2 = URIRef(f"{CRM}P2_has_type")
    P67 = URIRef(f"{CRM}P67_refers_to")
    GENDER_SIG = URIRef(f"{EX_PLACE}genderSignificance")
    GEO_HAS_GEOM = URIRef(f"{GEO}hasGeometry")
    GEO_AS_WKT = URIRef(f"{GEO}asWKT")
    RDFS_LABEL = URIRef("http://www.w3.org/2000/01/rdf-schema#label")

    for place in g.subjects(URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), E53):
        label_val = g.value(place, RDFS_LABEL)
        label = str(label_val) if label_val else str(place)

        gender_val = g.value(place, GENDER_SIG)
        gender = str(gender_val) if gender_val else "Mixed"

        note_val = g.value(place, P3)
        note = str(note_val) if note_val else ""

        # Get emotion
        emotion_uri = g.value(place, P67)
        emotion = ""
        if emotion_uri:
            em_label = g.value(emotion_uri, RDFS_LABEL)
            emotion = str(em_label) if em_label else ""

        # Get categories
        cats = []
        for cat_uri in g.objects(place, P2):
            cat_str = str(cat_uri)
            if "feminist_category" in cat_str:
                cat_label = cat_str.split("/")[-1].replace("_", " ").title()
                cats.append(cat_label)

        # Get coordinates
        geo_feature = g.value(place, P168)
        if not geo_feature:
            continue
        geom = g.value(geo_feature, GEO_HAS_GEOM)
        if not geom:
            continue
        wkt_val = g.value(geom, GEO_AS_WKT)
        if not wkt_val:
            continue

        wkt = str(wkt_val)
        match = re.search(r"POINT\(([-\d.]+)\s+([-\d.]+)\)", wkt)
        if not match:
            continue
        lon, lat = float(match.group(1)), float(match.group(2))

        icon_color = GENDER_ICON_COLORS.get(gender, "gray")
        popup_html = f"""
        <div style='font-family:sans-serif; min-width:200px'>
          <b style='font-size:14px'>{label}</b><br>
          <span style='color:#888'>Gender significance:</span> <b>{gender}</b><br>
          <span style='color:#888'>Emotional register:</span> {emotion}<br>
          <span style='color:#888'>Categories:</span> {', '.join(cats)}<br><br>
          <i style='font-size:11px; color:#555'>{note}</i>
        </div>
        """
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=label,
            icon=folium.Icon(color=icon_color, icon="info-sign"),
        ).add_to(m)

    # Legend
    legend_html = """
    <div style='position:fixed; bottom:30px; left:30px; z-index:1000;
                background:#FAF9F6ee; padding:12px 16px; border-radius:8px;
                font-family:sans-serif; font-size:12px; color:#1a1a1a; border:1px solid #DDD8CE;
                box-shadow: 0 2px 8px rgba(0,0,0,0.12)'>
      <b>Gender Significance</b><br>
      <span style='color:#b5446e'>● Feminized</span><br>
      <span style='color:#3d6b99'>● Masculinized</span><br>
      <span style='color:#4a9e6e'>● Mixed</span>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    return m
