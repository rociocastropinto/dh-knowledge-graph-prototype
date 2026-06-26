# Feminist RDF Gazetteer · Lima

**A semantic knowledge graph encoding gendered, emotional, and socio-spatial dimensions of nineteenth-century Lima**

> Based on Flora Tristán's *Peregrinations of a Pariah* (1838) · CIDOC CRM · GeoSPARQL · SPARQL · Streamlit

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url-here.streamlit.app)

---

## Overview

This project develops a feminist literary gazetteer modelling 13 places from Chapter 8 of Flora Tristán's *Peregrinations of a Pariah* (1838). It investigates how Linked Places data, CIDOC CRM, and RDF can be used to represent the gendered, symbolic, and emotional spatial experiences recorded in Tristán's narrative of republican Lima — and how that model can remain interoperable across both graph and relational database contexts.

The interactive prototype demonstrates:

- **SPARQL query interface** — 5 pre-built analytical queries with result visualisations
- **Interactive knowledge graph** — force-directed network of places, categories, and emotional registers
- **Geospatial map** — GeoSPARQL coordinates rendered in Folium, colour-coded by gender significance
- **Data model documentation** — inline ontology rationale and dual-database design decisions

---

## Research Context

In early nineteenth-century Peru, independence from Spain reorganised colonial patriarchy under a republican regime without dissolving it. Flora Tristán — of French and Peruvian parentage — travelled to Lima in 1833–1834 in search of family recognition, and her resulting memoir *Peregrinations of a Pariah* (1838) is the first female-authored account of Peru's republican transformation. As Muchotrigo (2019) argues, the text records *invisible geographies*: how gender regulated access to space, how exclusion was built into everyday life, and how resistance was exercised through movement and presence.

This project encodes those geographies as linked data. Thirteen places are identified from Chapter 8, all within or adjacent to Lima's Plaza Mayor — a district that concentrated political authority, religious institutions, and social hierarchies. Each place is structured not simply as a coordinate, but as a semantic entity encoding place type, gender significance, emotional register, and narrative citation.

### Research Question

How can Linked Places data, CIDOC CRM, and RDF be applied to *Peregrinations of a Pariah* to reveal the gendered and symbolic spatial experiences of women in nineteenth-century republican Lima?

---

## Methodology

The workflow proceeds in four stages:

**1. Text and Map Data Extraction**  
Close reading of Chapter 8 with manual spatial reference extraction. Each reference is recorded as a compound site carrying narrative, gendered, and affective meaning — not merely a toponym. Ambiguities in the text were resolved through secondary sources including Gootenberg (1991) and UNESCO World Heritage Centre historical cartography.

**2. Gazetteer Construction in LP-TSV**  
Extracted entities are organised in Linked Places TSV (LP-TSV) format, where each row encodes a place with identifiers, geometry, and interpretive metadata. Following Grunewald and Mostern (2024), the gazetteer harmonises data fidelity with narrative meaning by adding fields for place type, gender significance, and emotional embodiment. The dataset was also uploaded to the World Historical Gazetteer (WHG) platform, demonstrating interoperability with existing digital infrastructure.

**3. Semantic Modelling with CIDOC CRM and RDF**  
The gazetteer is converted to RDF using Python's `rdflib` and mapped to CIDOC CRM. Places are instantiated as `E53_Place`; feminist spatial categories (GENDERED_SPACE, POLITICAL_SPACE, etc.) as `E55_Type` linked via `P2_has_type`; emotional resonance as `E89_Propositional_Object` linked via `P67_refers_to`; geometry via GeoSPARQL's `geo:hasGeometry` and `geo:asWKT`.

**4. SPARQL Query Validation**  
The RDF graph is serialised as Turtle (`.ttl`) and validated with SPARQL queries demonstrating that the model can answer research questions about gendered and symbolic space — that is, that it functions as a semantic device, not merely a structured list.

---

## Feminist Spatial Categories

| Category | Function Type | Feminist Criteria |
|---|---|---|
| GENDERED_SPACE | Private / Domestic | Female-coded spaces of confinement or care; gained meaning in women's lives |
| POLITICAL_SPACE | Institutional / Public | Sites of patriarchal authority, often male-dominated |
| ECONOMIC_SPACE | Civic / Commercial | Gendered access to economic roles and modes of trade |
| SYMBOLIC_SPACE | Narrative / Symbolic | Ideologically laden zones of gender, identity, and agency |
| RELIGIOUS_SPACE | Sacred / Institutional | Spiritual authority with gendered clerical hierarchy or female-specific devotions |
| CARCERAL_SPACE | Enforced / Punitive | Spatial regimes of control, often gendered (incarceration of women vs men) |
| PUBLIC_CIVIC_SPACE | Mixed / Public | Stages of social performance where class and gender lines are negotiated |
| CULTURAL_SPACE | Cultural / Performance | Spaces of artistic and social display |

---

## Ontology Design

The model uses **CIDOC CRM 7.1.2** as its canonical framework, extended with custom feminist spatial properties and aligned with **GeoSPARQL 1.0**:

| Class | Role |
|---|---|
| `crm:E53_Place` | Core entity for each attested place |
| `crm:E55_Type` | Spatial and feminist categories |
| `crm:E89_Propositional_Object` | Emotional registers (Awe, Repugnance, Intimacy, Formality…) |
| `crm:E52_Time_Span` | Temporal attestation of each place |
| `crm:E41_Appellation` | Formal name label, enabling variant naming |
| `geo:Feature / geo:Geometry` | GeoSPARQL geometry with WKT point literals |

Custom extension properties:
- `ex:genderSignificance` — Feminized / Masculinized / Mixed (datatype property for relational compatibility)
- `ex:hasText` — textual label for propositional objects

### Dual-Database Design Rationale

A model designed exclusively for graph traversal is often hostile to relational query patterns. This design resolves the tension through three decisions:

1. **Flat typing over deep hierarchies** — all categories are `E55_Type` instances, projectable as lookup table rows in a relational schema without loss of semantic expressiveness
2. **Datatype properties for scalar attributes** — `genderSignificance` is a string literal, not an object property, mapping directly to a relational column without join overhead
3. **Geometry decoupled from identity** — the `crm:P168 → geo:Feature → geo:Geometry` chain allows coordinates to be stored in a PostGIS column while entities remain dereferenceable as LOD URIs

---

## First Outcomes

Three concrete outputs were produced:

1. **LP-TSV gazetteer uploaded to World Historical Gazetteer** — demonstrating interoperability and that feminist annotation survives standardisation into global infrastructure
2. **RDF dataset with SPARQL validation** — 345 triples; queries confirm the model correctly retrieves interpretive categories (e.g. all RELIGIOUS_SPACE places; all places with emotional registers)
3. **Network graph of spatial categories, gender, and emotion** — force-directed visualisation showing that POLITICAL_SPACE is the most centrally connected node, and that Mixed Gender places function as negotiated stages of class and gender performance

---

## Repository Structure

```
feminist-rdf-gazetteer-lima/
├── app.py                          # Streamlit application
├── requirements.txt
├── data/
│   └── flora_tristan_gazetteer.ttl # RDF/Turtle dataset (345 triples)
├── utils/
│   ├── sparql_runner.py            # Query engine + pre-built SPARQL queries
│   ├── graph_builder.py            # Pyvis interactive network builder
│   └── map_builder.py              # Folium geospatial map builder
```

---

## Running Locally

```bash
git clone https://github.com/rociocastropinto/feminist-rdf-gazetteer-lima.git
cd feminist-rdf-gazetteer-lima
pip install -r requirements.txt
streamlit run app.py
```

---

## Technologies

- Python · RDFLib · SPARQL
- CIDOC CRM 7.1.2 · GeoSPARQL 1.0 · Linked Places Format (LP-TSV)
- Streamlit · Plotly · Pyvis · Folium
- NetworkX (network analysis) · Apache Jena (SPARQL validation)

---

## References

- CIDOC (2021). *CIDOC CRM Conceptual Reference Model*. http://www.cidoc-crm.org/
- Grunewald, S. and Mostern, R. (2024). Working with Named Places. *Programming Historian*, 13.
- Massey, D. (1994). *Space, Place, and Gender*. University of Minnesota Press.
- Moreira, D. and Rocha, D. (2025). Gazetteer Literário de Machado de Assis. *Encontros Bibli*, 30.
- Muchotrigo, E. C. (2019). La construcción de la identidad de 'paria'. *Metáfora*, 10.
- Oberhauser, A. M. et al. (2017). *Feminist Spaces: Gender and Geography in a Global Context*. Routledge.
- W3C (2014). RDF 1.1 Concepts and Abstract Syntax. https://www.w3.org/TR/rdf11-concepts/
- Wright, M. W. (2010). Geography and gender: Feminism and a feeling of justice. *Progress in Human Geography*, 34(6).

---

## Author

**Rocío Alejandra Castro Pinto**  
M.A. Digital Humanities · Georg-August-Universität Göttingen  
[github.com/rociocastropinto](https://github.com/rociocastropinto)

---

## License

Data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) · Code: MIT
