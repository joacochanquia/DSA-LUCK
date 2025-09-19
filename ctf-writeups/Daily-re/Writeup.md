# Write-up: Legally Distinct Daily Game (Web + Reversing)

## Introducción
Este reto consistió en descubrir las palabras diarias que el juego **"Legally Distinct Daily Game"** usa para los días 72, 73 y 74, con el objetivo de obtener la flag en el formato:

![Página del reto](imagenes/Desafio.PNG)

## Descripción del reto
Se nos daba acceso a una página web con un juego estilo *Wordle* que mostraba únicamente la palabra del día actual, sin revelar las palabras de días anteriores ni posteriores.  
La pista del reto indicaba que no se podía hacer trampa fácilmente, por lo que debíamos investigar cómo se generaban las palabras de cada día.


![Página del reto](imagenes/Pagina.PNG)

## Proceso de resolución

### Investigación inicial
- Se consultaron listas públicas conocidas de Wordle y sus variantes.  
- Ninguna coincidía con las palabras esperadas para la flag.

### Análisis del archivo `words.wasm`
- Al inspeccionar el código fuente de la página con DevTools, se encontró un archivo llamado `words.wasm` que contenía la lógica del juego y el conjunto completo de palabras.  
- Se identificó una sección de datos que contenía las palabras codificadas.

![Archivo words.wasm](imagenes/words.PNG)

### Extracción de las palabras
- Se utilizó un script en Python (`Words.py`) para extraer las palabras del segmento de datos dentro del `.wasm`.  
- Se aplicó una expresión regular para filtrar todas las palabras de 5 letras.
  ```python
  data_blob = (
    r"\01\00\00\008482423c95bf2f4a165f0c08ad27a800\00might\00\00\02\00\00\0043dc252ca71e1d9b502bc2c44bd3fb3e\00joust\00\00\03\00\00\00eb38ca52bed68ffc6e771cb904a76281\00quaky\00\00\04\00\00\00dfd13e0a7f17da5496a22cf4423fbd7a\00unite\00\00\05\00\00\00de271fa1d0777a3aea3a926280e42158\00agile\00\00\06\00\00\00980920de164c7f279b2dc8e4ccd6fbf9\00valor\00\00\07\00\00\005dfd61c8ecae413bc851075388721e37\00xenon\00\00\08\00\00\002bd5e35921f7682406c59e06e0bd5a73\00latch\00\00\09\00\00\00a7d955cc7bbe8de8bb70f772da29e262\00image\00\00\0a\00\00\00508eb8634faba2eaaacda7194ff6ad10\00orbit\00\00\0b\00\00\00072f9d124ccaa8426d453b179123087c\00sleek\00\00\0c\00\00\00651a7234ff4100ed989795879163a5f6\00vowel\00\00\0d\00\00\009b37ddb0f7d92de5c73ecf4b1e0ab88b\00brisk\00\00\0e\00\00\0017aa8695a3d0cdac566de5e3f2e9d594\00whirl\00\00\0f\00\00\00afbbe4b3dd89ce9ff319649bfe90ab79\00grape\00\00\10\00\00\00337cab92d07605b1d1fc37d311b525a5\00elbow\00\00\11\00\00\0070e7726a9b8d5e65a6dbb19cf784ad5a\00zonal\00\00\12\00\00\00b3f61e6d07992d25a42114c7d50f5f69\00loyal\00\00\13\00\00\0067cb213109a49a3b9d3ca167c051dad9\00zesty\00\00\14\00\00\0037e55328fb18231f159ebb1d12b2c6a2\00choke\00\00\15\00\00\0068bf7179ac3257087966787f004543d5\00haste\00\00\16\00\00\00fc6521b9a1194a19de15ccd7e0975390\00xenon\00\00\17\00\00\00743fd28187df87b8e26e6c37ae50be1a\00relay\00\00\18\00\00\00c80f40e3c5250b243bd1ceceab2edf03\00abyss\00\00\19\00\00\008522b961b71c5b6bbde930cd62bf36cb\00march\00\00\1a\00\00\0013dcc16b15548672e0d308c1c2c67116\00apron\00\00\1b\00\00\00d0229677b1c1734fd39aa96e895979c1\00roast\00\00\1c\00\00\008cc8f9f16e05dfeddad7aa7b847dbd4f\00joint\00\00\1d\00\00\00102c63a00d6309b1a62f3552898bf5dc\00vivid\00\00\1e\00\00\00654ce3959aadb4aa0cea8ab1f09719d7\00drown\00\00\1f\00\00\009b50e0517ec8a9fe31a6712cb239fc69\00quack\00\00 \00\00\00a8b87cb7ca6c4cce8b6de91e55ff9c3e\00gloom\00\00!\00\00\006a1cc835e586a668e5de940eeb1fe364\00tango\00\00\22\00\00\0083bee0d3dce885bf1c51214c32f2f90a\00quest\00\00#\00\00\0045b7698a8e92ce91b506d64fecba314a\00nudge\00\00$\00\00\00f288bc4ee4dabb9ece63c60f9b9cb081\00inbox\00\00%\00\00\00e612ca2c10c3a2790551a3153b725c71\00zesty\00\00&\00\00\0010ebb501bc596fc0d68b77adc07885e5\00glide\00\00'\00\00\00a0ae1102ed936a10f3c0a08a4eeb1d06\00prank\00\00(\00\00\00d790b21bc90d2923cc3da0b07835f0a5\00xerox\00\00)\00\00\000b52b4ae038426e142173b550f6ff2d2\00brave\00\00*\00\00\0080e68391801c921249e41756b42b3694\00drive\00\00+\00\00\0001ccf3f1a516114b47e78b17c41d3068\00opera\00\00,\00\00\0003bc4a9cf8c632bbeef7bbeae2b80cb2\00trace\00\00-\00\00\00a1f6e432046a4d576491fb5977c04466\00rover\00\00.\00\00\00a774822c8ece8c62548df1e0fd338beb\00ultra\00\00/\00\00\00559886a46d4fc0334365207ffc10d366\00spoil\00\000\00\00\00dff54dc554b539b8a434bb5313e0a3ac\00hairy\00\001\00\00\003e0965bc9c65bc987e30db9e0e803505\00doubt\00\002\00\00\008b8f3419f95f982974bc3ea05897f089\00koala\00\003\00\00\00193436981ab2cd0c1c5fed476d1d2af8\00juice\00\004\00\00\00ef6b75ace2f1217dcc33a42911db7a6b\00raise\00\005\00\00\00e605d6861c75e572778ffb951cf231f7\00flair\00\006\00\00\00b7732452844d88e885de9bcccb5518b6\00quilt\00\007\00\00\006b8f71356e819af1a2065cb2b2927490\00pious\00\008\00\00\00e177fbd897d6043ac26550b45690f304\00inset\00\009\00\00\00042df3ad75c3a98ffaba61723a87a7d1\00uncle\00\00:\00\00\000a96f95856f4aa17f91da3ec76be0b8b\00obese\00\00;\00\00\001f7d1fcdbf614b306caacc615ed44c33\00barge\00\00<\00\00\00e68def0e199d4312a21bb63d2fe0b01d\00kiosk\00\00=\00\00\00a15dd9f89f1ce0521d8d40924864f97f\00yodel\00\00>\00\00\001e83cd89d9be464fda5eb4a265fa665c\00crane\00\00?\00\00\00cec5461ee8647e58534a7ddb9d7dd620\00knock\00\00@\00\00\00c32213f4f34d1529824936ceb3863beb\00plumb\00\00A\00\00\005df4440ca30ced69e48da69ac48b2eb2\00vague\00\00B\00\00\003d273ba1e7a4d2060921a0b828879720\00shove\00\00C\00\00\004d24345d562516215d8e5dad1638c27b\00wacky\00\00D\00\00\0048c649bc269ac8bb054bd6624ec47525\00slide\00\00E\00\00\00354810314ddeaa675974e2fdaeb558d3\00faint\00\00F\00\00\003ed04769ba8857297b3d5019bdfde899\00taunt\00\00G\00\00\00b0f88f4c8ef877ba8150f5d92d756c2c\00trawl\00\00H\00\00\00dc99b25df638f6bc0eb9cdd44811f2dd\00limbo\00\00I\00\00\001ed5047bb0ada6ded5ab08fdb84a8875\00urban\00\00J\00\00\008748afe7a3214eaafc7380bf19a680f8\00fiber\00\00K\00\00\00793ef7fbf6dff901a6606407cd5f0c8b\00prism\00\00L\00\00\00fc520bf146aeb77fdea602e500e9845d\00novel\00\00M\00\00\00ac1d6c3443cd2f849a9d18b851937839\00mirth\00\00N\00\00\006db5e56cec4d173744d5b458c0608c98\00tribe\00\00O\00\00\0032a9af7f43ac5a8037a047b5e07a4d5d\00drape\00\00P\00\00\000c24f57036a5fe8518ef366f6265f9a4\00charm\00\00Q\00\00\005aedfb770b7f3f2477051b22e281f548\00karma\00\00R\00\00\00e9273a3bb44af43be051a5539f4fb66b\00wrong\00\00S\00\00\002fb6b2b917bbaa44cc74b28f2e2916f8\00mound\00\00T\00\00\00f13d833cbfa67a79802051f44f48cd02\00youth\00\00U\00\00\000b17a8680c388a7caa02a4e296a34833\00noise\00\00V\00\00\008a810bfed10e6d76b5c18d633f0dfde1\00blaze\00\00W\00\00\006a3d227302a8f3ec34011b7f72845f1f\00slink\00\00X\00\00\00b69f00361af11e7ae4ce9cf9a12dd6d0\00liven\00\00Y\00\00\00cfd92e74f1db5f11afab3835199d0d76\00yacht\00\00Z\00\00\00b72f533a3a90b1b7cb7cc84420252318\00jolly\00\00[\00\00\0095ea1906cdc6fa71404e0dd1d5eb5975\00squad\00\00\5c\00\00\003c05527bcbb9f936cc2acd0666ef3e0a\00ozone\00\00]\00\00\006affd7f61fab8ddb3f18b4f499a665f1\00flops\00\00^\00\00\0003a85ea2dac0e104d8d1012514c8c667\00hasty\00\00_\00\00\00ac5cf869be0f98af893f3e57864f2449\00eager\00\00`\00\00\00e022eaa87c84c719d445d465bc1d8d6e\00gloat\00\00a\00\00\00e25903f490405fee417c76721a89bc39\00crave\00\00b\00\00\00752a1f7b05895cb302c86478fc63cf98\00notch\00\00c\00\00\00b20e698caa7d70d5351723c436f1aca9\00evoke\00\00d\00\00\005c5d906737c2edb0dc9c015ff4ca12c8\00hatch\00\00"
   
)

import re

# Busca palabras de longitud 5 entre delimitadores nulos
words = re.findall(r"\\00([a-z]{5})\\00", data_blob)
segment = words[71:75]  # indices 72, 73, 74 (Python zero-based)
print(segment)

  ```
- Finalmente, se obtuvieron las palabras correspondientes a los días solicitados:

| Día | Palabra |
|-----|---------|
| 72  | limbo   |
| 73  | urban   |
| 74  | fiber   |

![Salida del script de Python](imagenes/respuesta.png)

### Validación y flag
- Combinando las palabras obtenidas, la flag final es: K17{limbo, urban, fiber}

