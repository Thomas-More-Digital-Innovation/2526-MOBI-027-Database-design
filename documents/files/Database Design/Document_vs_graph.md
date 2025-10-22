# Vergelijking Document Database (zoals MongoDb) vs Graph Database (zoals Neo4j)

## 1. Structuur en data model

| Kenmerk   | Document Database | Graph Database       |
|--------------|--------|----------------|
| **Data model**| JSON/BSON-documenten met geneste eigenschappen en arrays.| Nodes en edges; realties zijn first-class citizens|
| **Schema**| Schemaloos of flexibel schema → makkelijk toevoegen van nieuwe node types of properties| Schema kan flexibel zijn, maar veel relationele traversals en types moeten worden gedefinieerd|
| **Relaties**| Relaties via arrays van references of embedded documents      | Relaties expliciet, direct verbonden met nodes.        |
| **Voorbeeld projectdata**          | een **Exo** node met array van relaties naar **Dof, Aim, Part**      | **Exo** node met edges naar **Dof, Aim, Part** via **HAS_AIM, ASSISTS_IN**|

## 2. Query mogelijkheden
| Kenmerk   | Document Database | Graph Database       |
|--------------|--------|----------------|
| **Filtering/search**| Zeer krachtig via MongoDB queries en aggregations | Filtering kan, maar vaak via pattern matching|
| **Traversals**| Beperkt efficiënt bij multi-hop relaties (>2 stappen), maar 1-2 hop queries zijn snel| Zeer efficiënt voor multi-hop queries (vb: "vind alle Exos die via Dof een SKN beïnvloeden") |
| **Aggregaties/dashboards**| Aggreagtion pipelines uitstekend voor statistieken en overzichten      | Aggregaties mogelijk maar minder intuïtief, gericht op netwerkstructuren |

## 3. Webfrontend integratie
| Kenmerk   | Document Database | Graph Database       |
|--------------|--------|----------------|
| **JSON-native**| Perfect: direct bruikbaar in React/Vue/Angular apps| JSON is mogelijk via drivers, maar vaak extra mapping nodig|
| **API**| REST / GraphQL makkelijk → JSON documenten. | REST / GraphQL mogelijk, maar meer complexiteit bij realties en traversals |
| **Visualisatie(graph-view)**| Kan via frontend libraries zoals D3.js of Cytoscape.js, realties worden array-based gevisualiseerd      | Graph-view direct natuurlijk, nodes en edges kunnen 1-op-1 weergegeven worden |

## 4. Schaalbaarheid en onderhoud
| Kenmerk   | Document Database | Graph Database       |
|--------------|--------|----------------|
| **Schaling**| Horizontaal sharden, cloud-native (MongoDB Atlas, AWS DocumentDB).| Schalen is lastiger, clustering bestaat maar complexer. |
| **Onderhoud**| Goed ondersteund, eenvoudig backups, flexibiliteit voor updates | Onderhoud vereist kennis van graph operations; bulk updates lastiger |
| **Data import**| Bulk import eenvoudig uit Excel/CSV → JSON → MongoDB     | Bulk import mogelijk. maar mapping van relaties complexer |

## 5. Flexibiliteit en uitbreidbaarheid
| Kenmerk   | Document Database | Graph Database       |
|--------------|--------|----------------|
| **Nieuwe nodes types**| Makkelijk toevoegen, geen schema migraties nodig| Kan, maar vaak extra configuratie en edge-definities vereist |
| **Nieuwe properties**| Schemaloos → direct toevoegen aan documenten | Schema moet soms aangepast worden; kan minder dynamisch zijn |
| **Nieuwe relaties**| Voeg nieuwe entry in **relations** array toe.     | Edge definities toevoegen; meer setup |

## 6. Kosten en projectimpact
| Kenmerk   | Document Database | Graph Database       |
|--------------|--------|----------------|
| **Setup en hosting**| Cloud-hosting eenvoudig (MongoDB Atlas, DocumentDB), goedkoper en minder complex | Hosting kan duurder, clustering complexer |
| **Development tijd**| Sneller prototypen, eenvuodig iteratief uitbreiden | Meer tijd nodig voor queries, schema-definities en traversals |
| **Frontend integratie**| JSON-compatibel → sneller ontwikkelen    | Extra mapping van graph queries naar JSON nodig |


## 7. Conclusie: Waarom Document Based (MongoDB) de beste keuze lijkt.
**1. Flexibiliteit:** Nieuwe nodes en eigenschappen kunnen zonder schema-migraties toegevoegd worden <br>
**2. Webcompatibiliteit:** JSON-native, direct bruikbaar voor frontend, filtering, dashboards en graph-visulisaties via D3.js, Cytoscape.js ...<br>
**3. Eenvoudige data-import:** Bulk import van Excel → JSON → MongoDB, makkelijker dan mapping naar Neo4j<br>
**4. Traversals zijn beperkt:** Projectqueries vereisen meestal 1-2 hop-relaties: MongoDB kan dit prima aan.<br>
**5. Schaalbaarheid en hosting:** MongoDB Atlas/ DocumentDB → makkelijk, cloud-ready, goedkoper dan Neo4j<br>
**6. Aggregaties en dashboards:** MongoDB Aggregation Pipeline is krachtig voor statistieken zonder extra tools.<br>
**7. Onderhoud en ontwikkeling:** Schemaloos → makkelijk uitbreiden, minder complex dan Neo4j bij updates<br>


## 8. Voorbeeld
```
{
  "_id": "Exo1",
  "type": "Exo",
  "properties": {
    "name": "Finger curl exercise",
    "difficulty": "medium"
  },
  "relations": [
    {
      "type": "ASSISTS_IN",
      "endNode": "Dof1",
      "amount": "+1",
      "notes": "Supports flexion movements"
    },
    {
      "type": "DOESNT_GO_WITH",
      "endNode": "SKN1",
      "amount": "1",
      "reason": "Skin irritation risk"
    },
    {
      "type": "HAS_AIM",
      "endNode": "vinger",
      "priority": "high"
    }
  ]
}

```

