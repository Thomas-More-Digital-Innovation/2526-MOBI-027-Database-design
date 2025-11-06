# Keuze van de technologieën: Spring Boot en Angular

## Backend: Spring Boot

Voor de backend van dit project is gekozen voor **Spring Boot**, een volwassen en veelzijdig Java-framework, vanwege de volgende technische redenen:

1. **Modulaire en schaalbare architectuur**  
   Spring Boot maakt gebruik van een componentgebaseerde architectuur en dependency injection via Spring Framework. Dit zorgt voor een duidelijke scheiding van verantwoordelijkheden en maakt het eenvoudig om verschillende lagen (controller, service, repository) te organiseren. Dit is bijzonder nuttig voor een project dat meerdere databronnen en complexe datamodellen combineert.

2. **Uitgebreide ondersteuning voor databases**  
   Spring Boot biedt directe ondersteuning voor zowel relationele databases (via Spring Data JPA) als document-gebaseerde databases zoals MongoDB (via Spring Data MongoDB). Dit maakt het geschikt voor dit project waarin gegevens uit Excel-bestanden worden geconverteerd naar een document-gebaseerde structuur in MongoDB, waarbij de flexibiliteit van schema-loze opslag essentieel is.

3. **REST API faciliteiten**  
   Spring Boot vereenvoudigt het opzetten van RESTful webservices. Controllers en repository-lagen kunnen in enkele lijnen code een volledig functionele API leveren. Dit is belangrijk voor de communicatie tussen de backend en de Angular frontend, inclusief filtering, zoekfuncties en data-aggregaties.

4. **Configuratie en extensie**  
   Spring Boot biedt uitgebreide configuratiemogelijkheden en ondersteuning voor externe configuratiebestanden, waardoor het makkelijk is om de applicatie aan te passen aan verschillende omgevingen (ontwikkel-, test- en productieomgeving). Daarnaast zijn er tal van uitbreidingen beschikbaar, zoals integratie met security, batchverwerking, en data-conversie van en naar Excel/JSON.

5. **Community en documentatie**  
   Spring Boot is een van de meest gebruikte Java-frameworks wereldwijd. Het heeft een zeer uitgebreide documentatie en actieve community, wat handig is bij het implementeren van geavanceerde functionaliteit zoals aggregaties en complexe queries op MongoDB.

---

## Frontend: Angular

Voor de frontend is gekozen voor **Angular**, een krachtig TypeScript-gebaseerd frontend-framework, vanwege de volgende technische overwegingen:

1. **Component-gebaseerde structuur**  
   Angular gebruikt een duidelijke componenthiërarchie, waarbij elke UI-component zelfstandig en herbruikbaar is. Dit maakt het mogelijk om complexe UI-elementen, zoals zoek- en filterfunctionaliteiten, grafische visualisaties (graph-view) en dashboards, overzichtelijk te organiseren en te onderhouden.

2. **Two-way data binding en reactieve forms**  
   Angular biedt sterke ondersteuning voor reactieve forms en two-way data binding. Dit vergemakkelijkt het dynamisch updaten van de UI op basis van gebruikersinput of data uit de backend. Voor een project waarin gebruikers filters kunnen instellen en de resultaten direct in een grafische weergave of tabel zien, is dit essentieel.

3. **Integratie met grafische libraries**  
   Angular kan eenvoudig geïntegreerd worden met JavaScript-visualisatielibraries zoals D3.js, Cytoscape.js of ngx-graph. Hierdoor kunnen complexe netwerkstructuren (zoals exoskeleton ↔ joint relaties) visueel en interactief worden weergegeven zonder dat de kernarchitectuur wordt beïnvloed.

4. **TypeScript en onderhoudbaarheid**  
   Angular is volledig gebaseerd op TypeScript, wat sterke typecontrole biedt en fouten tijdens compile-time detecteert. Dit verhoogt de betrouwbaarheid en onderhoudbaarheid van de code, vooral bij projecten met veel datavelden en complexe datamodellen.

5. **Routing en state management**  
   Angular biedt ingebouwde routing en mogelijkheden voor state management, waardoor de navigatie tussen verschillende pagina’s (zoals filterpagina, graph-view en dashboard) gestructureerd en performant verloopt.

---

## Conclusie

De combinatie van **Spring Boot** voor de backend en **Angular** voor de frontend biedt een technisch solide fundament voor het project:

- Spring Boot levert een modulair, uitbreidbaar en database-agnostisch backend platform.  
- Angular biedt een component-gebaseerde, interactieve frontend die goed integreert met complexe visualisaties en dynamische data.  

Samen vormen ze een technologie-stack die geschikt is voor het structureren, presenteren en interactief ontsluiten van complexe datasets zoals die van het Jobtakels-project.
