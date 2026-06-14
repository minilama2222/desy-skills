#!/usr/bin/env python3
"""Linter v6 — translate() con match de frase multi-palabra + tokens."""
import json, re, unicodedata
from pathlib import Path

# Catalog path resolved relative to this script so the linter stays portable
# (works regardless of where the skill is installed in the filesystem).
CATALOG = json.load(open(Path(__file__).parent / 'catalog.json'))
COMPONENT_SYNONYMS = {'link': 'links-list', 'c-link': 'links-list', 'radio': 'radios', 'checkbox': 'checkboxes'}

# Traducciones: keys pueden ser multi-palabra. Ordenar por longitud descendente para matchear frases largas primero.
TRANSLATIONS = {
    'por defecto': 'default',
    'primario': 'primary',
    'alerta': 'alert',
    'éxito': 'success',
    'exito': 'success',
    'advertencia': 'warning',
    'información': 'info',
    'informacion': 'info',
    'transparente': 'transparent',
    'deshabilitado': 'disabled',
    'activo': 'active',
    'pequeño': 'small',
    'pequeno': 'small',
    'mediano': 'medium',
    'grande': 'large',
    'habilitado': 'enabled',
    'enlace': 'link',
    'icono': 'icon',
    'placeholder': 'placeholder',
    'error': 'error',
    'pista': 'hint',
    'múltiples': 'multi',
    'multiples': 'multi',
    'actual': 'current',
    'submenú': 'submenu',
    'submenu': 'submenu',
    'niveles': 'level',
    'nivel': 'level',
}

CSS_CLASS_PATTERN = re.compile(r'^(c-|ds-|\.c-)')
COMPOSITION_PATTERN = re.compile(r'^(con |y |con un |con una |sin |en )')

def normalize(s):
    s = s.lower().strip()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r'\s+', ' ', s)
    return s

def translate(s):
    """Traduce español→inglés. Frases multi-palabra primero, luego tokens individuales."""
    s = normalize(s)
    # Ordenar keys por longitud descendente
    keys_sorted = sorted(TRANSLATIONS.keys(), key=lambda k: -len(k.split()))
    for k in keys_sorted:
        # Reemplazar la frase con su equivalente
        s = re.sub(r'\b' + re.escape(k) + r'\b', TRANSLATIONS[k], s)
    return s

def lint(comp, var):
    if CSS_CLASS_PATTERN.match(var):
        return ('CSS_CLASS', f"'{var}' parece CLASE CSS, no variante")
    comp_canonical = COMPONENT_SYNONYMS.get(comp, comp)
    if comp_canonical not in CATALOG:
        return ('UNKNOWN', f"componente '{comp}' no existe")
    variantes = [e['name'] for e in CATALOG[comp_canonical]['examples']]
    
    # Normalizar y traducir
    var_norm = normalize(var)
    var_en = translate(var)
    
    # Match exacto (con y sin normalización, con y sin traducción)
    for v in variantes:
        v_n = normalize(v)
        if var_norm == v_n or var_en == v_n or normalize(var_en) == v_n:
            return ('OK', f"match exacto con '{v}' (normalizado)")
        # Substring en cualquiera de las formas
        for candidate in [var_norm, var_en]:
            if candidate in v_n:
                return ('OK', f"match substring con '{v}' (candidato: '{candidate}')")
    
    # ¿Es composición CSS? (patrón "con X" descriptivo)
    if COMPOSITION_PATTERN.match(normalize(var)):
        return ('COMPOSITION', f"'{var}' es patrón CSS descriptivo (no variante oficial). Probablemente modificadores sobre 'por defecto'.")
    
    # ¿Hay tokens en común con alguna variante?
    var_tokens = set(normalize(var_en).split())
    for v in variantes:
        v_tokens = set(normalize(v).split())
        if var_tokens.issubset(v_tokens) and len(var_tokens) >= 2:
            return ('OK', f"tokens matchean variante '{v}' (input: {var_tokens})")
    
    return ('WARNING', f"no matchea; primer variante: '{variantes[0]}'")

if __name__ == "__main__":
    tests = [
        ("acceso-cargando", [
            ("header-mini", "con logo"),
            ("notification", "éxito"),
            ("spinner", "por defecto"),
            ("link", "c-link"),
            ("links-list", "con múltiples links"),
            ("footer", "con los logos a la izquierda"),
        ]),
        ("404", [
            ("header-advanced", "con 3 niveles"),
            ("link", "c-link"),
            ("searchbar", "con un botón"),
            ("footer", "con los logos a la izquierda"),
        ]),
        ("accesibilidad", [
            ("header-mini", "por defecto"),
            ("link", "c-link"),
            ("links-list", "por defecto"),
        ]),
    ]
    counts = {'OK': 0, 'COMPOSITION': 0, 'CSS_CLASS': 0, 'WARNING': 0, 'UNKNOWN': 0}
    icon = {'OK': '✅', 'COMPOSITION': '🟡', 'CSS_CLASS': '🟣', 'WARNING': '⚠️', 'UNKNOWN': '❌'}
    
    print("="*75)
    print("LINTER DE VARIANTES v6 — normalización español↔inglés + rechazo de clases CSS")
    print("="*75)
    
    for mockup, idents in tests:
        print(f"\n--- {mockup} ---")
        for comp, var in idents:
            status, msg = lint(comp, var)
            counts[status] = counts.get(status, 0) + 1
            print(f"  {icon[status]} {comp}/{var:35s} → {msg}")
    
    total = sum(counts.values())
    print(f"\n{'='*75}")
    print(f"Resumen: {total} identificaciones")
    for status, n in counts.items():
        if n > 0:
            pct = 100 * n / total
            print(f"  {icon[status]} {status:13s}: {n:3d}  ({pct:5.1f}%)")
    quality = counts.get('OK', 0) + counts.get('COMPOSITION', 0) + counts.get('CSS_CLASS', 0)
    real_problems = counts.get('WARNING', 0) + counts.get('UNKNOWN', 0)
    print(f"\n  Reconocimientos CORRECTOS: {quality}/{total} ({100*quality/total:.0f}%)")
    print(f"  Warnings para revisión:    {real_problems}/{total} ({100*real_problems/total:.0f}%)")
