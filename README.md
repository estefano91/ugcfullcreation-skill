# ugcfullcreation — Tu estudio de contenido con IA

Describes lo que quieres. Te genera las imágenes, el vídeo, el caption y lo publica en Instagram.

Sin diseño. Sin fotógrafos. Sin agencias.

---

## Cómo funciona

Escribes `/ugcfullcreation` en Claude Code y eliges qué quieres hacer. Hay cinco modos, cada uno para una situación distinta.

---

## Modo A — Wizard paso a paso (el más habitual)

El modo por defecto. Te hace preguntas una a una: qué actriz, qué formato, qué concepto, qué estilo. Tú contestas en lenguaje normal y al final genera todo.

**Cuándo usarlo:** cuando quieres crear algo nuevo desde cero.

**Ejemplo:**

Escribes `/ugcfullcreation` y el sistema te pregunta:
- ¿Qué actriz? → Luna
- ¿Qué formato? → Carrusel de 6 slides
- ¿Cuál es el concepto? → Terraza de verano, ropa de lino blanco, mezcla de cuerpo entero y primeros planos, luz dorada de tarde

Resultado: 6 imágenes recortadas al formato de Instagram + caption + hashtags, en una carpeta lista para publicar.

---

## Modo B — Generar desde un archivo JSON

Si ya tienes una campaña definida en un JSON (de una sesión anterior o de otra herramienta), lo lanzas directamente sin pasar por el wizard.

**Cuándo usarlo:** cuando ya tienes el plan de la campaña guardado y solo quieres ejecutarlo.

**Ejemplo:**

> "genera este archivo: campaigns/luna-linen-park/campaign.json"

El sistema muestra un resumen de lo que va a generar (actriz, formato, número de imágenes, coste estimado), le dices que sí, y genera.

---

## Modo C — Repetir una campaña con otra actriz

Tomas cualquier campaña ya generada y la vuelves a generar con la cara de otra actriz. El escenario, el outfit, la cámara, todo queda igual. Solo cambia la identidad.

**Cuándo usarlo:** cuando un concepto funciona y quieres el mismo contenido con Mia, Rowan u otra actriz.

**Ejemplo:**

> "usa el mismo JSON de la sesión de lino de Luna pero con Mia"

El sistema detecta la campaña, muestra qué va a cambiar (solo la actriz y sus fotos de referencia), confirmas, y genera las mismas imágenes con la cara de Mia.

También funciona con cualquier JSON de prompt externo — no tiene que ser tuyo:

> "coge este JSON de Pinterest que describe una sesión editorial y aplícalo a Rowan"

---

## Modo D — Calendario automático (genera solo cada día)

Configuras un calendario una vez con lo que quieres publicar cada día. Cada mañana, a la hora que elijas, tu Mac genera ese contenido de forma automática, sin que hagas nada. Te llega una notificación cuando está listo.

**Cuándo usarlo:** cuando ya tienes el contenido planificado y quieres que se genere solo.

**Cómo es un día típico:**

- **07:33** — tu Mac genera el contenido de hoy en segundo plano
- **08:00** — notificación en el escritorio: *"6 imágenes listas para el carrusel de Luna. Publicación a las 09:00."*
- **08:45** — abres la carpeta y miras las imágenes
- **09:00** — ejecutas un comando y se publica en Instagram

Tiempo real: menos de 5 minutos al día.

**Ejemplo de entrada en el calendario:**

| Fecha | Actriz | Formato | Concepto |
|---|---|---|---|
| 2026-05-10 | Luna | Carrusel 6 slides | Piscina, bikini blanco, luz de mediodía, mezcla poses |
| 2026-05-11 | Mia | Reel 5s | Terraza restaurante, vestido terracota, pelo al viento |
| 2026-05-12 | Luna + Mia | Carrusel 5 slides | Tarde de compras, ropa casual, ciudad |

---

## Modo R — Desde imágenes de Pinterest

Guardas imágenes de Pinterest (o de cualquier fuente) en la carpeta de referencias de una actriz. El sistema lee cada imagen visualmente, extrae el escenario y el estilo, y genera esa misma escena con la cara de tu actriz.

**Cuándo usarlo:** cuando encuentras referencias visuales que te gustan y quieres recrearlas con tus actrices.

**Ejemplo:**

Tienes 5 imágenes guardadas de un estilo editorial de café parisino. Escribes:

> "/ugcfullcreation from-pinterest luna"

El sistema analiza cada imagen, describe lo que ve (escenario, outfit, cámara, luz), te muestra el plan antes de generar, confirmas, y genera las 5 escenas con la cara de Luna.

---

## Tus actrices

Cada actriz es una identidad que el sistema mantiene consistente en todas las imágenes. Con una sola foto de referencia la cara se mantiene estable en 5–6 imágenes seguidas. Con más fotos, aún más consistente.

Para añadir una actriz nueva solo necesitas una foto de cara clara. El sistema extrae la identidad solo.

Ejemplos de actrices configuradas:

- **Luna** — 21 años, rubia, piel clara con pecas, ojos marrones. Contenido lifestyle y moda.
- **Mia** — 23 años, mediterránea, pelo oscuro ondulado, piel dorada. Moda atrevida y belleza.
- **Rowan** — 22 años, pelirroja, piel muy clara, ojos verde-gris. Editorial y tonos de otoño.

### Carpetas de cada actriz

```
actors/{actriz}/
  ├── hero_shots/       ← fotos de referencia de cara (2–4 máx.)
  ├── references/       ← refs adicionales si las hay
  ├── pinterest/        ← imágenes de inspiración para Modo R
  ├── motion_refs/      ← vídeos de referencia de movimiento/cámara (.mp4 .mov)
  └── actor_card.json   ← identidad de la actriz (generada automáticamente)
```

La carpeta `motion_refs/` es la que usa el sistema cuando generas un reel con vídeo de referencia (Modo video-to-video). Pon ahí los vídeos de TikTok, Reels o cualquier clip que quieras usar como guía de movimiento. El sistema los detecta automáticamente — no hace falta indicar la ruta a mano.

---

## Formatos disponibles

| Formato | Para qué sirve |
|---|---|
| **Carrusel** | Sesiones de moda, storytelling, educación de producto |
| **Post único** | Hero shot editorial, revelación de producto |
| **Reel ambiental** | Piscina, café, exterior con movimiento de ambiente |
| **Reel retrato** | Primer plano, belleza, contacto visual directo |
| **Reel POV** | Contenido viral tipo "POV: you found her" |
| **Reel con texto** | Overlay con frase, quote, llamada a la acción |
| **Reel con control de cámara** | Movimiento de cámara preciso: zoom, paneo, tilt, travelling |
| **Story** | Momento íntimo, prueba de look, lifestyle casual |

---

## Control de cámara en reels

Los reels generados con Kling ahora admiten movimientos de cámara deterministas — no "muévete con naturalidad" sino un zoom, paneo o tilt concreto, igual en cada generación.

Se especifica en el script con un nombre de preset y el sistema lo convierte en parámetros de API:

| Preset | Efecto |
|---|---|
| `zoom_in` / `zoom_out` | Acercamiento o alejamiento suave de la actriz |
| `zoom_in_slow` / `zoom_out_slow` | Versión lenta, ideal para finales de clip |
| `pan_left` / `pan_right` | La cámara gira horizontalmente |
| `tilt_up` / `tilt_down` | La cámara se inclina hacia arriba o hacia abajo |
| `truck_left` / `truck_right` | La cámara se desplaza lateralmente |
| `pedestal_up` / `pedestal_down` | La cámara sube o baja (crane up / down) |
| `roll_cw` / `roll_ccw` | Rotación del encuadre (efecto Dutch tilt) |

También acepta valores personalizados si quieres ajustar la velocidad — el rango es de 1 (muy lento) a 10 (máximo).

**Ejemplo de uso:**

> "haz un reel de Luna en la terraza con un zoom lento de entrada"

El sistema genera primero el fotograma estático y luego anima con `zoom_in_slow`. El movimiento de cámara y el movimiento de la actriz son independientes — puedes combinar un zoom lento con una actriz que se ríe o se mueve el pelo.

**Cuándo usar control de cámara vs reel normal:**

- Reel normal → la actriz se mueve, la cámara "flota" de forma natural
- Control de cámara → necesitas un movimiento de cámara específico y repetible (revelación, push dramático, travelling de producto)

---

## Lo que el sistema hace solo, sin que tengas que pedirlo

Hay una serie de cosas técnicas que la skill maneja automáticamente en cada generación. No hace falta que las sepas ni que las pidas — pasan siempre, por defecto. Aquí van explicadas simple:

**🎨 Realismo automático**
Cada imagen y vídeo lleva "toques de realismo" incluidos en el prompt: textura de piel real, pelo que no está perfectamente peinado, ropa con caída y peso natural, luz ligeramente desigual, un detalle imperfecto de fondo. Es lo que hace que una foto se vea como una foto de verdad y no como un render de IA. Esto se aplica siempre, incluso en generaciones rápidas.

**🚫 Evita que Instagram/las IAs bloqueen el contenido**
Algunos proveedores de IA (sobre todo GPT Image) tienen un filtro de contenido muy sensible con bikinis, ropa ajustada o ciertas poses combinadas con fotos de referencia reales. El sistema ya sabe qué combinaciones bloquean y cuáles no — lo ha ido aprendiendo generación a generación — y elige el proveedor y la redacción del prompt que tiene más probabilidad de pasar limpio a la primera. Si algo se bloquea igualmente, el sistema reintenta con un ajuste (cambia el ángulo, la palabra usada para la prenda, o cambia de proveedor) en vez de simplemente fallar.

**📸 Identidad estable, incluso con prompts cortos**
Para que la cara de tu actriz no cambie entre fotos, el sistema usa muy pocas fotos de referencia (1-2, no más) y prompts cortos y sencillos — cuantos más detalles de identidad metas en el texto (medidas exactas, colores en hexadecimal...), peor funciona, porque compite con la propia foto de referencia. La cara la lleva la foto, no el texto.

**🎥 Cámara fija en los vídeos**
Por defecto, los vídeos ahora se generan con cámara fija (como un trípode) en vez de "seguir" el movimiento de la persona — esto evita que la cara se deforme o pixele cuando hay movimiento rápido. Si necesitas que la cámara sí se mueva (zoom, paneo…), se puede pedir explícitamente.

**🧠 Aprende y no se le olvida**
Cada vez que una generación se bloquea o pasa de forma sorprendente, el sistema lo anota en su base de conocimiento interna (parte del código de la skill, guardado en GitHub). Eso significa que estas reglas no dependen de esta conversación — la próxima vez que uses `/ugcfullcreation`, en un chat nuevo, semanas después, el sistema ya sabe todo esto y lo aplica solo.

---

## Cuánto cuesta

Son costes de generación pagados directamente a los proveedores de IA. La skill en sí es gratuita.

| Tipo de contenido | Coste aproximado |
|---|---|
| 1 imagen (slide de carrusel) | $0.07 – $0.15 |
| Carrusel completo de 6 imágenes | $0.40 – $0.70 |
| 1 Reel (imagen + vídeo de 5s) | $0.90 – $1.00 |
| 1 mes de contenido diario (24 posts) | $15 – $25 |

---

## Cómo empezar

1. Instala [Claude Code](https://claude.ai/code)
2. Descarga la skill en tu carpeta de skills de Claude
3. Abre Claude Code en tu carpeta de proyecto y escribe `/ugcfullcreation`

La primera vez te hace unas preguntas de configuración (qué cuenta de Instagram, qué tipo de contenido, qué presupuesto). Después ya no vuelve a preguntarte.

---

## Preguntas frecuentes

**¿Tengo que escribir prompts?**
No. Describes el concepto en lenguaje normal y la skill lo convierte internamente en lo que necesita.

**¿Puedo usar mis propias actrices?**
Sí. Cualquier persona con al menos una foto de cara clara sirve como actriz.

**¿Puedo gestionar varias cuentas de Instagram?**
Sí. Puedes tener tantas cuentas y actrices como quieras, cada una con su propio calendario y configuración.

**¿Publica solo o tengo que aprobar?**
Por defecto genera el contenido y espera tu aprobación antes de publicar. También se puede configurar para publicar automáticamente.

**¿Funciona si mi Mac está en reposo?**
No. El Mac tiene que estar encendido. Con la tapa cerrada y enchufado va bien.
