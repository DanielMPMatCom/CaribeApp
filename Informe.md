### Introducción

El problema de la distribución de pullovers en el contexto de un evento deportivo universitario involucra diversas restricciones y objetivos que lo convierten en un desafío complejo de optimización. Existen múltiples enfoques para abordar problemas de esta naturaleza, entre los cuales destacan la Programación Lineal Entera Mixta (MILP), los Algoritmos Genéticos (GA), el Simulated Annealing (SA), y los Algoritmos de Búsqueda Local como el *hill climbing* y *tabu search*. Este informe tiene como objetivo comparar estos métodos, argumentando por qué MILP representa una solución más robusta y adecuada para el problema en cuestión. El problema a resolver consiste en distribuir un número limitado de pullovers entre varias facultades, de modo que se respeten diversas restricciones, como la cantidad disponible de colores, la cantidad de atletas inscritos en cada facultad, y la asignación equitativa basada en rankings y preferencias de color. Además, se busca maximizar el cumplimiento de restricciones de prioridad y minimizar las diferencias entre las razones de asignación de pullovers y atletas inscritos.

### Algoritmos Heurísticos y de Búsqueda Local

Los algoritmos heurísticos como los Algoritmos Genéticos (GA) y Simulated Annealing (SA), así como los métodos de búsqueda local como *hill climbing* y *tabu search*, son técnicas populares para resolver problemas de optimización complejos, especialmente cuando el espacio de soluciones es grande y la solución óptima no puede ser calculada de manera eficiente. Estas técnicas tienen la ventaja de ser más rápidas y menos exigentes en términos de recursos computacionales en comparación con MILP, especialmente en problemas de gran escala.

Sin embargo, estos métodos presentan varias limitaciones significativas cuando se comparan con MILP en el contexto del problema en cuestión:

1. Soluciones Aproximadas y No Óptimas: Los algoritmos heurísticos y de búsqueda local, por su naturaleza, tienden a encontrar soluciones aproximadas que no garantizan la optimalidad. En un problema donde cumplir con todas las restricciones es crítico, la capacidad de encontrar la solución óptima es esencial, y MILP garantiza esto siempre que el problema sea resoluble en tiempo razonable.

2. Dificultad para Manejar Múltiples Restricciones Complejas: Aunque los algoritmos heurísticos pueden ser adaptados para manejar múltiples restricciones, la combinación de restricciones estrictas y prioritarias, como en este problema, es difícil de implementar de manera eficiente. Por ejemplo, en GA o SA, diseñar una función de aptitud que maneje adecuadamente todas las restricciones y prioridades puede ser complejo y a menudo requiere afinaciones finas específicas para cada problema, lo cual reduce la generalidad del método.

3. Control Limitado sobre la Prioridad de Restricciones: En MILP, es posible definir de manera precisa la prioridad entre las restricciones utilizando técnicas como el método de *weighted sum* o *lexicographic optimization*. Por otro lado, en métodos como GA o SA, la priorización de restricciones puede no ser tan directa y puede depender de penalizaciones en la función objetivo, lo que introduce un elemento de incertidumbre en la calidad de las soluciones obtenidas.

4. Riesgo de Estancamiento en Óptimos Locales: Los métodos de búsqueda local como *hill climbing* y *tabu search* son susceptibles a quedar atrapados en óptimos locales, especialmente en problemas de alta complejidad como el presente. Aunque existen técnicas para mitigar este riesgo, como la diversificación en *tabu search* o el uso de operadores de mutación en GA, estas no garantizan la escapatoria de un óptimo local y pueden requerir tiempos de ejecución significativamente mayores para lograr soluciones de calidad.

### Programación Lineal Entera Mixta (MILP)

MILP es un enfoque de optimización exacto que permite modelar problemas con restricciones lineales y variables de decisión enteras. La fortaleza de MILP radica en su capacidad para encontrar soluciones óptimas garantizadas, siempre y cuando el problema sea formulado adecuadamente y los recursos computacionales lo permitan. La naturaleza combinatoria del problema de distribución de pullovers, que involucra múltiples restricciones y variables discretas, hace que MILP sea especialmente apropiado, ya que puede manejar la complejidad del problema y proporcionar soluciones óptimas que satisfacen todas las restricciones impuestas.

Además, MILP permite la incorporación explícita de prioridades entre restricciones, lo que es crucial en este caso, dado que algunas restricciones son innegociables mientras que otras pueden ser relajadas si es necesario. Este control granular sobre las restricciones es difícil de replicar en enfoques heurísticos.

### Metodología
#### Datos de Entrada
El algoritmo recibe los siguientes datos de entrada:

1. Facultades: Lista de facultades participantes.

2. Atletas: Diccionario que mapea cada facultad con la cantidad de atletas inscritos.

3. Ranking: Diccionario que asigna un ranking a cada facultad.

4. Pullovers Disponibles: Diccionario con la cantidad total de pullovers disponibles por color.

5. Pullovers para Árbitros y Profesores: Cantidad fija de pullovers destinados a árbitros y profesores.

6. Pullovers para AAAC: Cantidad fija de pullovers destinados al comité organizador (AAAC).

7. Preferencias: Diccionario opcional que indica la preferencia de color de cada facultad.

#### Pasos del Algoritmo
1. Asignación a Árbitros, Profesores y AAAC:

    * El algoritmo selecciona aleatoriamente un color para los árbitros, profesores y AAAC.
    
    * Se distribuye una cantidad fija de pullovers a estos grupos, reduciendo el total disponible para las facultades.

2. Asignación Inicial para Facultades con Menos de 10 Atletas:

    * Las facultades con menos de 10 atletas reciben sus pullovers de forma directa, asignándoles un color (preferido o aleatorio) y reduciendo el total disponible.

3. Optimización Principal:

    * Se modela un problema de optimización lineal para asignar los pullovers restantes a las facultades con más de 10 atletas.

    * Variables de Decisión:
        
        𝑥𝑖 : Cantidad de pullovers asignados a la facultad 𝑖.

        𝑦𝑖𝑗 : Variable binaria que indica si la facultad 𝑖 recibe el color 𝑗.

        𝑧𝑖𝑗 : Cantidad de pullovers asignados a la facultad 𝑖 del color 𝑗.

        𝑝𝑟𝑜𝑝𝑜𝑟𝑐𝑖𝑜𝑛𝑒𝑠 𝑖 : Proporción de pullovers asignados respecto al número de atletas de la facultad 𝑖.

        𝑑𝑖𝑓𝑒𝑟𝑒𝑛𝑐𝑖𝑎 𝑖 : Diferencia absoluta entre la proporción asignada y la media.

    * Restricciones:

        La suma total de pullovers asignados debe ser igual al total disponible.
        
        Cada facultad recibe exactamente un color.
        
        Ninguna facultad recibe más pullovers de los que hay disponibles de un color.
        
        La proporción de pullovers asignados a cada facultad debe acercarse lo más posible a la media.
        
        Función Objetivo:
        
        Minimizar la suma de las diferencias absolutas entre la proporción de pullovers asignados y la media.

4. Resolución:

    * El problema de optimización se resuelve utilizando el solver PuLP con un límite de tiempo para garantizar la eficiencia en la solución.

5. Salida:

    * El algoritmo imprime la cantidad de pullovers asignados a cada facultad, junto con el color asignado. También proporciona un resumen de la distribución total por color.
    
#### Resultados

El algoritmo asigna los pullovers de forma que las facultades con más atletas reciben una cantidad proporcionalmente mayor, respetando las preferencias de color cuando es posible. El uso de un modelo de optimización asegura que la distribución sea lo más equitativa posible, minimizando la diferencia en relación con el número de atletas.