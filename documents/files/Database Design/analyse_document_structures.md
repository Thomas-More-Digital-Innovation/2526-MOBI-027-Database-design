# Document structures Analyse

## 1. file met nodes in en property type van de node, relaties worden als array bewaard als property

#### Voordelen
- **Simpel model:** alles staat in één collectie, makkelijk te importeren/exporteren.
- **Makkelijk op te zetten:** geen complexe schema's, gewoon 1 JSON per node.
- **Flexibiliteit:** je kan nieuwe types en realties toevoegen zonder schema migrations.
- **Goed voor prototyping:** vooral handig als je snel iets met een wabapp wil testen.

#### Nadelen
**Queries worden complex:**
- Je moet veel joins in de applicatielaag doen (want Mongo heeft geen echte joins).
- Relaties op meerdere hops zijn traag en lastig.

**Redundantie of inconsistentie:**
- Als je een relatie in Node A opslaat, moet je dit eigenlijk ook in Node B spiegelen, zorgt voor kans op inconsistentie.

**Performance issues bij groei:**
- Zodra er veel relaties zijn, worden arrays groot, updates en queries worden trager.

**Geen echte graph-functionaliteit meer:**
- Traversals die in een graph DB zijn kunnen hier niet.

#### Impact op je webapp
- **Goed voor simpele views:** Als je bv. een profielpagina toont met directe relaties kan dit prima werken.
- **Lastig bij complexe queries:** Als je later features wil zoasl "suggesties", moet je dit zelf in code oplossen, wat performace-killers kunnen worden.
- **API wordt zwaar:** Je webapp moet vaak meerdere quereis doen en zelf data samenvoegen, i.p.v. dat de database dit efficiënt doet.

## 2. Document maken per type node, realties bewaren als array in property van de record

#### Voordelen
- **Betere organisatie:** data is opgesplitst per type, waardoor documenten per collectie homogener zijn.
- **Efficiënter zoeken:** queries per node-type zijn sneller
- **Minder "type"-property nodig:** je weet al uit de collectie wat voor node het is, scheelt data & queries.
- **Makkelijker schema's opstellen:** bv. validatie per collectie.
- **Goed voor API-structuur:** in je webapp kan je endpoints netjes mappen op collecties.

#### Nadelen
**Relaties blijven arrays**
- Je hebt nog steeds duplicatie en kans op inconsistenties (Node 1 zegt dat hij verbonden is met Node B, maar Node B heeft dat niet correct gespiegeld)

**Cross-collection queries lastig**
- Als je een query wil zoals "geef alle parts van exo X inclusief joints", moet je meerdere queries doen en data zelf samenvoegen.

**Traversals blijven moeilijk**
- Diepere graph queries (2 of meer hops) zijn lastig zonder extra logica in je applicatie.

**Moeilijker bij dynamische realties**
- als realties heel gevarieerd zijn (veel soorten edges), kan het beheer ingewikkeld worden.


#### Impact op je webapp
- **API-structuur wordt duidleijker:** /exoskeletons/:id, /parts/:id, /joints/:id
- **Goede fit voor CRUD:** makkelijk afzonderlijk zecords ophalen of aanpassen.
- **Maar relationele queries worden bottleneck:** UI die samengestelde data nodig heeft wordt trager en vraagt extra code.

## 3. Nodes en verschillende relaties in apparte collecties bewaren

#### Voordelen
- **Duidelijke semantiek:** elke collectie vertegenwoordigt één type realtie, waardoor het heel leesbaar is en logisch aanvoelt.
- **Queries per relatie-type zijn snel:** als je bv. alle *HAS_AIM* relaties nodig hebt, zit je meteen in de juiste collectie zonder filtering.
- **Indexering eenvoudig:** je kan makkelijk indexen op *from* en *to* binnen die specifieke collectie.
- **Schaalbaarder dan arrays:** relaties staan los van nodes, dus geen eneorme arrays die steeds groter worden.
- **Past bij een webapp die endpoints per relatie-type wil:** bijvoorbeeld */belongs_to*, */has_aim*


#### Nadelen
**Fragmentatie**
- Realties zijn verspreid over meerdree collecties, wat queries lastiger maakt als je "alle rielaties van een nod" wil. Je moet dan door alle realtie-collecties heen zoeken.

**Extra complexiteit**
- Je backend moet snappen in welke collectie gezocht moet worden voor welk type relatie.

**Moielijke voor generieke traversals**
- "geef alle nodes die 3 stappen verwijderd zijn van node X", dan zal je zelf over meerdere collecties heen moeten traversen.

**Minder flexibel bij nieuwe relatie-types**
- voor elke relatie moet je een **nieuwe collectie** aanmaken, wat kan leiden tot veel collecties als je model groeit.

#### Impact op je webapp
- **Goed als de UI relationele data vaak per type opvraagt**
- **Minder geschikt als de UI heel generiek moet zijn:** Dan moet je API alle relatie-collecties combineren en dat kan performance-kosten geven.
- **Complexere API-design:** of je maakt generieke endpoints (*/relations?from=exo_1*) die onderliggend alle collecties doorzoeken, of je maakt endpoints per relatie-type (*/belongs_to*, */has_aim*)

## 4. Nodes in verschillende collecties en relaties in 1 collectie

#### Voordelen
- **Duidelijke scheiding:** nodes en realties apart houdt het model strak en vergelijkbaar met een echte graph DB.
- **Geen duplicatie:** je hoeft relaties niet in beide nodes bij te houden, want je hebt een aparte tabel/collectie.
- **Relaties kunnen properties hebben:** handig voor bv. gewicht van een joint, timestamp, sterkte van connectie.
- **Flexibel:** makkelijk nieuwe soorten relaties toevoegen zonder nodes te veranderen.
- **Schaalbaarder:** dan arrays in nodes, omdat realties onafhankelijk zijn.

#### Nadelen
**Meer queries nodig**
- om een node met zijn relaties te halen, moet je vaak eerst de node ophalen, daarna alle edges, daarna de target nodes.

**Geen native joins in document-databases**
- Dus je moet dit in je applicatie-logica doen (of via aggregation pipelines, wat soms ingewikkeld is).

**Performance**
- bij veel hops (traversals) kan dit zwaar worden, omdat je elke stap zelf moet oplossen in code of aggregaties.

**Complexer te bouwen API**
- Je moet endpoints maken die nodes en realties apart afhandelen

#### Impact op je webapp
- **Betere uitbreidbaarheid:** relaties kunnen makkelijk verrijkt worden en API's worden consistenter (*/nodes*, */realtions*).
- **Past goed bij graph-achtige features:** (aanbevelingen, connecties, visualisaties).
- **Extra logica nodig in backend:** je API moet queries optimaliseren, bv. door caching of pre-joined responses, want een naëve aanpak kan traag worden.
- **Makkelijk om later te switchen naar een echte graph DB:** als de nood aan performance/traversals groeit.