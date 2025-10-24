# *MOBI - 027* Database Design  

## Notities eerste meeting (23/10/2025)  

### Uitgelegd waarom eventueel export Neo4J niet handig is
Ik heb zelf ondervonden dat bij het gebruik van de data die geëxporteerd is uit Neo4J nogal lastig is om deze te importeren naar MySQL, naar MongoDB is dit eenvoudiger gelukt. Ook heb ik gemerkt dat deze structuur nogal zeer uitgebreid is zo staat er bijvoorbeeld bij de relaties telkens de volledige start node en eind node opgegeven wat voor heel veel dubbele gegevens zorgt die gefiltert moeten worden bij het importeren.

Ook zal dit voor later exporteren naar excel met deze structuur lastiger gaan om dan terug te importeren.

Daarom heb ik uitgelegd dat ik denk dat het voor hun beter is om de csv bestanden die ze nu gebruiken te gaan hergebruiken met een lichtelijke aanpassing, relaties duidelijk scheiden zodat deze voor import eenvoudiger zijn. 


### Uitgelegde alternatieve oplossing
Het is mogelijk op een eenvoudige manier om de geëxporteerde JSON van Neo4J te importeren naar MongoDB, als er dan vanuit MongoDB de gegevens geëxporteerd worden, is de JSON al veel overzichtelijker en simpelder en kan deze in tegenstelling tot de JSON van Neo4J eenvoudig in een excel tabel omgezet worden wat dan ook weer voor meer duidelijkheid zorgt voor personen met minder kennis over JSON.

### Volgende stappen
- Document opstellen met duidelijke verschillen tussen export van MongoDB en SQL
- Documenteren hoe Excel, JSON en CSV null worden voorgesteld
- Stappenplan, Hoe excel invullen → Hoe importeren → Hoe exporteren terug