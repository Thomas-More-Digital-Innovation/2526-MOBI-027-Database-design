# *MOBI - 027* Database Design  

## Notities eerste meeting (22/09/2025)  

### Data-import en context  

De gegevens die nodig zijn voor dit project zijn momenteel beschikbaar in verschillende Excel-bestanden. Deze bestanden worden met behulp van specifieke commando’s geïmporteerd in de Neo4j graph database. Hierdoor kan bestaande data efficiënt hergebruikt worden en hoeft er geen complexe migratie vanuit andere systemen plaats te vinden.  

#### Mobilab & Care  
Mobilab & Care is een onderzoeksgroep van de Thomas More University of Applied Sciences, actief binnen het expertisecentrum *Care and Well-being*. Hun doel is de levenskwaliteit van mensen met zorg- of ondersteuningsnoden te verbeteren. Dit bereiken zij door innovatief onderzoek in zowel fysieke, psychologische als sociale domeinen.  

De onderzoeksgroep focust sterk op preventie, revalidatie en blijvende ondersteuning, met als ambitie om volledige maatschappelijke inclusie voor iedereen mogelijk te maken. Daarnaast ontwikkelen zij toepassingen voor de zorgsector in Vlaanderen, vaak in nauwe samenwerking met partners uit het werkveld.  

#### Historiek: Sense to eXion-project  
Enkele jaren geleden bouwden DI-studenten voor Mobilab & Care een graph database in het kader van het *Sense to eXion*-project. Dit project onderzocht hulpmiddelen zoals risicotools, sensoren en exoskeletten die de bewegingen van werknemers ondersteunen of meten.  

De verzamelde data werd opgeslagen in een Neo4j graph database, en er werd een front-end ontwikkeld waarmee queries uitgevoerd konden worden. Enkele voorbeeldvragen die het systeem kon beantwoorden waren:  

- *“Ik produceer exoskeletten van het volgende type, welke toepassingen zijn hiervoor relevant?”*  
- *“In mijn bedrijf worden veel dozen gedragen. Hoe kan ik met een exoskelet het risico op fysieke klachten bij mijn werknemers verminderen?”*  

Hoewel de database bestond en ook de bijbehorende Excel-bestanden en website werden voorbereid, is het platform nooit officieel live gegaan.  

#### Nieuwe fase: Jobtakels  
Het *Sense to eXion*-project is inmiddels afgerond, maar met het nieuwe project **Jobtakels** wil men voortbouwen op de bestaande graph database. Hierbij worden de eerdere beslissingen opnieuw geëvalueerd: is Neo4j nog steeds de beste keuze, en hoe kan de database uitgebreid worden met nieuwe data en functionaliteiten?  

Daarom wordt dit project gestart met een herziening van de bestaande architectuur, de beschikbare data, en de mogelijkheden die Neo4j biedt om de database toekomstbestendig te maken.  

#### Voorlopig pad voor heropstart  
De eerste stap bestaat uit:  
1. Het verzamelen en ordenen van de beschikbare Excel-bestanden.  
2. Het opzetten van een importproces naar Neo4j met herbruikbare commando’s.  
3. Het in kaart brengen van de huidige structuur en hoe deze aansluit bij de noden van het nieuwe project.  
4. Het verifiëren of Neo4j de juiste keuze blijft, of dat alternatieven overwogen moeten worden.  
5. Relaties moeten snel en eenvoudig duidelijk zijn voor iedereen.

### Waarom een Graph Database  
Een graph database maakt het mogelijk om relaties op een intuïtieve en visuele manier in kaart te brengen. In plaats van losse tabellen met complexe koppelingen (zoals in een relationele database), worden de gegevens opgeslagen als knopen (nodes) en verbindingen (edges). Hierdoor kan eenvoudig worden weergegeven welk exoskelet geschikt is voor een bepaald gebied of regio.  

Daarnaast maakt een graph database het mogelijk om verder te gaan dan eenvoudige koppelingen. Zo kan er bijvoorbeeld een netwerk worden opgebouwd waarin exoskeletten, regio’s, typen ondergrond, en zelfs specifieke gebruikersproblemen met elkaar in verband staan. Dit geeft niet alleen inzicht in welke oplossing waar toepasbaar is, maar ook in *waarom* die toepassing logisch is.  

Een belangrijke meerwaarde is dat relaties in een graph database altijd een “eerste klas” onderdeel van de data zijn, en dus niet verstopt zitten in ingewikkelde query’s of join-tabellen. Dit maakt het eenvoudiger om:  
- snel nieuwe verbanden en patronen te ontdekken,  
- data uit te breiden met extra knopen of relaties zonder het bestaande model te breken,  
- queries uit te voeren die meerdere lagen van relaties doorzoeken (bijvoorbeeld: *welke exoskeletten zijn toepasbaar bij personen die last hebben van hun schouder als ze hun handen hoger in de lucht moeten steken*).  

Bovendien is een graph database schaalbaar en flexibel. Naarmate de dataset groeit, kan er zonder grote herstructureringen nieuwe informatie worden toegevoegd. Dit is belangrijk omdat de context rond exoskeletten en hun toepassingen waarschijnlijk in de toekomst zal veranderen of complexer zal worden.  

Kortom: een graph database is gekozen omdat deze niet alleen de relaties tussen exoskeletten en regio’s inzichtelijk maakt, maar ook ruimte biedt voor uitbreiding richting gebruikersdata, probleemtypen, en andere factoren die relevant zijn voor het vinden van de beste oplossingen.  

### Belangrijkste aandachtspunten  
1. Gegevens (bijvoorbeeld uit Excel of handmatig ingevoerd) moeten eenvoudig toegevoegd kunnen worden.  
2. De opgeslagen gegevens moeten gemakkelijk uitleesbaar en filterbaar zijn, zonder dat hiervoor veel tussenstappen nodig zijn.  
3. Gebruikers mogen de gegevens enkel raadplegen; bewerken is niet toegestaan.  
4. Het moet mogelijk zijn om eenvoudig queries uit te voeren op de database.

### Planning
Deze week ga ik mijzelf bezig houden met onderzoeken van alle verschillende opties database, de voor en nadelen hiervan opzoeken om dat met effectieve simpele voorbeeld data al een logisch te analyseren of de voor en nadelen die ik eerder heb gevonden van toepassing zijn of niet. Ze gingen mij nog excel sturen en eenvoudige voorbeeld geven die ik kan importerne in Neo4 om de effectieve data te kunnen bekijken en analyseren.

