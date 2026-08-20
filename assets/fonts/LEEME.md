# Tipografías Zunox

| Rol | Familia | Pesos | Uso |
|---|---|---|---|
| Display | **Sora** | 600 / 700 | Titulares, bajada del logo, cifras destacadas |
| Texto | **Manrope** | 400 / 500 / 700 | Párrafos, interfaz, documentos |

Ambas son **variables** y llevan licencia **SIL Open Font License 1.1**: puedes
usarlas en web, impresión, productos y clientes sin pagar nada. Ver `OFL.txt`.

## Autoalojarlas (recomendado: no depende de Google)

```css
@font-face{
  font-family:"Sora"; src:url("/fonts/Sora-Variable.ttf") format("truetype-variations");
  font-weight:100 800; font-display:swap;
}
@font-face{
  font-family:"Manrope"; src:url("/fonts/Manrope-Variable.ttf") format("truetype-variations");
  font-weight:200 800; font-display:swap;
}
```

Para producción, convierte a **WOFF2** (pesa ~70 % menos):
`pip install fonttools brotli && fonttools ttLib.woff2 compress Sora-Variable.ttf`

## Escala tipográfica

| Nivel | Tamaño | Familia / peso | Interlineado | Tracking |
|---|---|---|---|---|
| Display | 56–72 px | Sora 700 | 1.05 | −0.02em |
| H1 | 40 px | Sora 600 | 1.10 | −0.02em |
| H2 | 30 px | Sora 600 | 1.20 | −0.015em |
| H3 | 22 px | Sora 600 | 1.30 | −0.01em |
| Cuerpo | 16–17 px | Manrope 400 | 1.65 | 0 |
| Cuerpo pequeño | 14 px | Manrope 400 | 1.60 | 0 |
| Etiqueta | 11.5 px | Sora 500 mayúsculas | 1.4 | +0.14em |
| Bajada del logo | — | Sora 400 mayúsculas | — | ajustado al ancho de ZUNOX |

**El logo no usa estas fuentes.** Las cinco letras de ZUNOX son curvas
dibujadas a medida: nunca escribas «ZUNOX» con Sora y lo llames logo.
