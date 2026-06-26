import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import pandas as pd
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from utils.sparql_runner import load_graph, run_query, QUERIES
from utils.graph_builder import build_pyvis_html
from utils.map_builder import build_map

TTL_PATH = os.path.join(os.path.dirname(__file__), "data", "flora_tristan_gazetteer.ttl")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Feminist RDF Gazetteer · Lima",
    page_icon="🗺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap');

  /* Base */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #FAF9F6;
    color: #1a1a1a;
  }
  h1, h2, h3 { font-family: 'EB Garamond', serif !important; color: #1a1a1a; }

  /* Main area background */
  .stApp { background-color: #FAF9F6; }
  [data-testid="stAppViewContainer"] { background-color: #FAF9F6; }
  [data-testid="stHeader"] { background-color: #FAF9F6; }
  section[data-testid="stSidebar"] > div { background-color: #F0EDE6; border-right: 1px solid #DDD8CE; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: #F0EDE6;
    border-bottom: 2px solid #DDD8CE;
    padding: 0 8px;
    border-radius: 6px 6px 0 0;
  }
  .stTabs [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 500;
    color: #6b6b6b;
    padding: 10px 22px;
    border-bottom: 3px solid transparent;
    background: transparent;
  }
  .stTabs [aria-selected="true"] {
    color: #b5446e !important;
    border-bottom: 3px solid #b5446e !important;
    background: transparent !important;
    font-weight: 600 !important;
  }
  .stTabs [data-baseweb="tab"]:hover { color: #b5446e !important; background: #e8e4dc !important; }

  /* Metric cards */
  .metric-card {
    background: #FFFFFF;
    border: 1px solid #DDD8CE;
    border-radius: 8px;
    padding: 16px 20px;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .metric-num { font-size: 32px; font-family: 'EB Garamond', serif; color: #b5446e; }
  .metric-label { font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

  /* Ontology blocks */
  .ontology-block {
    background: #FFFFFF;
    border-left: 3px solid #b5446e;
    border-radius: 0 6px 6px 0;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 13px;
    line-height: 1.7;
    color: #2a2a2a;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  .ontology-block code {
    background: #F0EDE6;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 12px;
    color: #5a3060;
    border: 1px solid #DDD8CE;
  }

  /* Sidebar text */
  .sidebar-desc {
    font-size: 12px;
    color: #5a5a5a;
    line-height: 1.6;
    margin-top: 8px;
  }

  /* SPARQL code box */
  .sparql-box {
    background: #F5F3EE;
    border: 1px solid #DDD8CE;
    border-radius: 6px;
    padding: 14px;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    color: #3a2a4a;
    white-space: pre-wrap;
    line-height: 1.6;
  }

  /* Selectbox and widgets */
  .stSelectbox > div > div {
    background: #FFFFFF;
    border: 1px solid #DDD8CE;
    color: #1a1a1a;
  }

  /* Buttons */
  .stButton > button {
    background: #b5446e;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 500;
  }
  .stButton > button:hover { background: #8f3458; }

  /* Dataframe */
  .stDataFrame { border: 1px solid #DDD8CE; border-radius: 6px; }

  /* Divider */
  hr { border-color: #DDD8CE; }

  /* Legend dot */
  .legend-dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }

  /* Success/info boxes */
  .stAlert { border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_resource
def get_graph():
    return load_graph(TTL_PATH)

g = get_graph()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗺 Feminist RDF Gazetteer")
    st.markdown("**Lima, Peru — 19th century**")
    st.markdown("""
    <div class='sidebar-desc'>
    A semantic knowledge graph encoding gendered, emotional, and socio-spatial 
    dimensions of 19th-century Lima from Flora Tristán's 
    <em>Peregrinations of a Pariah</em>.<br><br>
    Built with <strong>CIDOC CRM</strong>, <strong>RDFLib</strong>, 
    <strong>GeoSPARQL</strong>, and deployed as a proof-of-concept 
    methodology for feminist literary gazetteers.<br><br>
    <strong>Ontologies used:</strong><br>
    · CIDOC CRM (E53, E55, E89, E52, E41)<br>
    · GeoSPARQL (geo:Feature, geo:asWKT)<br>
    · Custom feminist spatial extensions
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**Repository**")
    st.markdown("[github.com/rociocastropinto/feminist-rdf-gazetteer-lima](https://github.com/rociocastropinto/feminist-rdf-gazetteer-lima)")


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# Feminist RDF Gazetteer")
st.markdown("#### Semantic Mapping of Gendered Space in Nineteenth-Century Lima")
st.markdown("*Flora Tristán · Peregrinations of a Pariah · CIDOC CRM · SPARQL · GeoSPARQL*")
st.divider()

# ── Metrics row ───────────────────────────────────────────────────────────────
from rdflib import URIRef as U
CRM_NS = "http://www.cidoc-crm.org/cidoc-crm/"
n_places = len(list(g.subjects(U("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), U(f"{CRM_NS}E53_Place"))))
n_triples = len(g)
n_cats = len(set(str(o) for s,p,o in g.triples((None, U(f"{CRM_NS}P2_has_type"), None))
               if "feminist_category" in str(o)))
n_emotions = len(set(str(s) for s,p,o in g.triples((None, U("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                                                      U(f"{CRM_NS}E89_Propositional_Object")))))

c1, c2, c3, c4 = st.columns(4)
for col, num, label in [
    (c1, n_places, "E53 Places"),
    (c2, n_triples, "RDF Triples"),
    (c3, n_cats, "Feminist Categories"),
    (c4, n_emotions, "Emotional Registers"),
]:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
          <div class='metric-num'>{num}</div>
          <div class='metric-label'>{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "SPARQL Explorer",
    "Knowledge Graph",
    "Spatial Map",
    "Data Model",
])

# ═══════════════════════════════════════════════════════════════
# TAB 1 · SPARQL EXPLORER
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Query the Knowledge Graph")
    st.markdown("""
    Select a pre-built SPARQL query below to interrogate the RDF dataset. 
    Each query demonstrates a different analytical axis: gender, spatial category, 
    emotional register, and intersectional combinations.
    """)

    query_name = st.selectbox("Select query", list(QUERIES.keys()))

    col_run, col_sparql = st.columns([1, 3])
    with col_run:
        show_sparql = st.checkbox("Show SPARQL", value=True)

    if show_sparql:
        st.markdown(f"<div class='sparql-box'>{QUERIES[query_name].strip()}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.spinner("Running query…"):
        df = run_query(g, query_name)

    if df.empty:
        st.info("No results returned for this query.")
    else:
        st.success(f"{len(df)} result(s) returned")
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Chart for suitable queries
        if "genderSignificance" in df.columns:
            st.markdown("#### Distribution by Gender Significance")
            gender_counts = df["genderSignificance"].value_counts().reset_index()
            gender_counts.columns = ["Gender", "Count"]
            fig = px.bar(
                gender_counts, x="Gender", y="Count", color="Gender",
                color_discrete_map={"Feminized": "#b5446e", "Masculinized": "#3d6b99", "Mixed": "#4a9e6e"},
                template="plotly_white",
            )
            fig.update_layout(showlegend=False, plot_bgcolor="#FAF9F6", paper_bgcolor="#FAF9F6",
                              font_color="#1a1a1a", height=280, margin=dict(t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

        if "category" in df.columns:
            st.markdown("#### Category Frequency")
            cat_counts = df["category"].value_counts().reset_index()
            cat_counts.columns = ["Category", "Count"]
            fig2 = px.bar(
                cat_counts, x="Count", y="Category", orientation="h",
                color="Count", color_continuous_scale=["#e8c4d0", "#b5446e"],
                template="plotly_white",
            )
            fig2.update_layout(showlegend=False, plot_bgcolor="#FAF9F6", paper_bgcolor="#FAF9F6",
                               font_color="#1a1a1a", height=300, margin=dict(t=20, b=20))
            st.plotly_chart(fig2, use_container_width=True)

        if "emotion" in df.columns:
            st.markdown("#### Emotional Registers")
            em_counts = df["emotion"].value_counts().reset_index()
            em_counts.columns = ["Emotion", "Count"]
            fig3 = px.pie(
                em_counts, names="Emotion", values="Count",
                color_discrete_sequence=["#b5446e","#3d6b99","#4a9e6e","#c87c2a","#7a5a9e","#888","#c4a020"],
                template="plotly_white",
            )
            fig3.update_layout(plot_bgcolor="#FAF9F6", paper_bgcolor="#FAF9F6",
                               font_color="#1a1a1a", height=320)
            st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2 · KNOWLEDGE GRAPH
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Interactive Knowledge Graph")
    st.markdown("""
    The graph encodes three layers of semantic structure: **places** (circles, coloured 
    by gender significance), **spatial categories** (diamonds), and **emotional registers** 
    (ellipses in gold). Edges represent CIDOC CRM properties. Hover over nodes to inspect 
    their annotations; drag to rearrange.
    """)

    col_l, col_r = st.columns([3, 1])
    with col_r:
        st.markdown("**Legend**")
        st.markdown("""
        <div style='font-size:12px; line-height:2; color:#2a2a2a'>
        <span class='legend-dot' style='background:#b5446e'></span>Place · Feminized<br>
        <span class='legend-dot' style='background:#3d6b99'></span>Place · Masculinized<br>
        <span class='legend-dot' style='background:#4a9e6e'></span>Place · Mixed<br>
        <span class='legend-dot' style='background:#aaa; border-radius:0'></span>Category (diamond)<br>
        <span class='legend-dot' style='background:#c4a020'></span>Emotional register
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("""
        <div style='font-size:11px; color:#555; line-height:1.6'>
        <b>CRM properties shown:</b><br>
        crm:P2_has_type<br>
        crm:P67_refers_to<br>
        ex:genderSignificance
        </div>
        """, unsafe_allow_html=True)

    with col_l:
        with st.spinner("Rendering graph…"):
            html = build_pyvis_html(g)
        components.html(html, height=560, scrolling=False)


# ═══════════════════════════════════════════════════════════════
# TAB 3 · MAP
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### Spatial Distribution of Gendered Places")
    st.markdown("""
    Each marker represents a place from Tristán's narrative, geo-referenced to 
    19th-century Lima. Marker colour encodes **gender significance** as annotated 
    in the RDF dataset. Click any marker to view the full semantic record — 
    spatial categories, emotional register, and interpretive note.
    """)

    from streamlit_folium import st_folium
    fmap = build_map(g)
    st_folium(fmap, width="100%", height=520, returned_objects=[])

    st.markdown("""
    <div style='font-size:12px; color:#666; margin-top:8px'>
    Coordinates sourced from GeoSPARQL <code>geo:asWKT</code> literals in the RDF dataset. 
    FT_1 (Casa de la tía) omitted from map — no geo-coordinates available in the source text.
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 4 · DATA MODEL
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### Ontology & Data Model")
    st.markdown("""
    This project models gendered historical places using **CIDOC CRM** as the canonical 
    reference ontology, extended with custom feminist spatial properties and aligned with 
    **GeoSPARQL** for geospatial representation. The design follows the principle that 
    a well-designed conceptual model should be derivable into both an 
    **RDF/OWL triple store** and a **normalised relational schema** — 
    a key requirement for projects requiring dual-database interoperability.
    """)

    st.markdown("#### Core Classes")

    classes = [
        ("crm:E53_Place", "The primary entity. Each place in the gazetteer is an instance of E53, encoding the physical and conceptual location referenced in Tristán's narrative."),
        ("crm:E55_Type", "Used for both spatial category (GENDERED_SPACE, RELIGIOUS_SPACE, etc.) and place type (church, port, government_building). Allows polyhierarchical classification without redundant class proliferation."),
        ("crm:E89_Propositional_Object", "Encodes the emotional register attributed to each place. This is the CRM's mechanism for representing subjective or propositional content attached to an entity."),
        ("crm:E52_Time_Span", "Temporal anchoring for each place's attestation in the source (1830–1838, Tristán's Lima period)."),
        ("crm:E41_Appellation", "Formal name label, enabling multilingual and variant naming without altering the place entity itself."),
        ("geo:Feature / geo:Geometry", "GeoSPARQL classes for point coordinates, stored as WKT literals. Enables spatial querying and map rendering independent of the semantic layer."),
    ]

    for cls, desc in classes:
        st.markdown(f"""
        <div class='ontology-block'>
        <code>{cls}</code><br>{desc}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Key Properties")

    props = [
        ("crm:P2_has_type", "Links a place to its E55_Type instances. A single place can carry multiple types simultaneously — this polyvalence is the core mechanism for intersectional spatial analysis."),
        ("ex:genderSignificance", "Custom property extending CRM. Values: Feminized / Masculinized / Mixed. Intentionally kept as a datatype property (not a class) to remain compatible with relational column semantics."),
        ("crm:P67_refers_to", "Connects the place to its E89 emotional register. Chosen over a simple annotation property to preserve CRM's event-referencing logic and enable reasoning over propositional content."),
        ("crm:P168_place_is_defined_by", "Links to the geo:Feature, decoupling semantic identity from geometric representation — places retain their identity even if coordinates change or are disputed."),
        ("crm:P3_has_note", "Interpretive annotation in natural language. In a relational projection, this maps to a TEXT column; in RDF, it remains a literal with language tag."),
    ]

    for prop, desc in props:
        st.markdown(f"""
        <div class='ontology-block'>
        <code>{prop}</code><br>{desc}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Dual-Database Design Rationale")
    st.markdown("""
    A central challenge in semantic DH projects is that a model designed exclusively 
    for graph traversal often becomes hostile to relational query patterns — and vice versa. 
    This design resolves that tension through three decisions:

    1. **Flat typing over deep hierarchies.** All categories are E55_Type instances rather 
       than subclasses of E53, making them representable as rows in a `place_type` lookup 
       table without loss of semantics.

    2. **Datatype properties for scalar attributes.** `genderSignificance` and `hasText` 
       are datatype properties (string literals), not object properties pointing to 
       controlled-vocabulary URIs. This means they project directly to relational columns 
       without join overhead.

    3. **Geometry decoupled from identity.** The `crm:P168 → geo:Feature → geo:Geometry` 
       chain means coordinates can be stored in a PostGIS geometry column in a relational 
       system while the same entities remain dereferenceable as LOD URIs in the graph.
    """)

    st.markdown("#### Alignment with Standards")
    st.markdown("""
    | Standard | Usage in this project |
    |---|---|
    | CIDOC CRM 7.1.2 | Core entity and property framework |
    | GeoSPARQL 1.0 | Geometry representation and spatial predicates |
    | Linked Places Format (LP-TSV) | Source data format before RDF conversion |
    | W3C RDF 1.1 / Turtle | Serialisation format |
    | MIT License | Open data release |
    """)
