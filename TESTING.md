# Testing Documentation

## Cobertura de Pruebas por Endpoint

### ✅ Endpoints Cubiertos

| Endpoint | Método | Pruebas | Descripción |
|----------|--------|---------|-------------|
| `/` | GET | 1 | Health check raíz |
| `/blacklist/ping` | GET | 1 | Health check API |
| `/blacklist` | POST | 7 | Agregar email a blacklist |
| `/blacklist/<email>` | GET | 3 | Consultar email en blacklist |

**Total: 4 endpoints, 13 pruebas unitarias**

---

## Detalle de Pruebas

### 1. GET / (Root)
- ✅ `test_root` - Verifica respuesta 200 y contenido "OK"

### 2. GET /blacklist/ping (Health Check)
- ✅ `test_health_check` - Verifica respuesta 200 y contenido "pong"

### 3. POST /blacklist (Agregar a Blacklist)
- ✅ `test_add_blacklist_success` - Email agregado exitosamente
- ✅ `test_add_blacklist_invalid_email` - Validación de formato email
- ✅ `test_add_blacklist_invalid_uuid` - Validación de formato UUID
- ✅ `test_add_blacklist_duplicate` - Prevención de duplicados (409)
- ✅ `test_add_blacklist_missing_fields` - Campos requeridos faltantes
- ✅ `test_add_blacklist_no_data` - Request sin datos
- ✅ `test_add_blacklist_with_ip` - Captura de IP del cliente
- ✅ `test_add_blacklist_exception` - Manejo de errores de BD (500)

### 4. GET /blacklist/<email> (Consultar Email)
- ✅ `test_get_blacklist_exists` - Email existe en blacklist (200)
- ✅ `test_get_blacklist_not_exists` - Email no existe (200)
- ✅ `test_get_blacklist_exception` - Manejo de errores de BD (500)

---

## Métricas de Coverage

**Coverage Actual: 90.54%** ✅ (Supera el 70% requerido)

| Archivo | Statements | Miss | Cover |
|---------|-----------|------|-------|
| models/blacklist.py | 21 | 5 | 76.19% |
| resources/__init__.py | 0 | 0 | 100.00% |
| resources/blacklist_resource.py | 39 | 2 | 94.87% |
| resources/get_blacklist_resource.py | 14 | 0 | 100.00% |
| **TOTAL** | **74** | **7** | **90.54%** |

---

## Ejecución de Pruebas

### Local
```bash
# Ejecutar todas las pruebas
python3 -m pytest tests/test_unit.py -v

# Con coverage (falla si < 70%)
python3 -m pytest tests/test_unit.py --cov=resources --cov=models/blacklist --cov-config=.coveragerc --cov-fail-under=70 -v

# Generar reporte HTML
python3 -m pytest tests/test_unit.py --cov=resources --cov=models/blacklist --cov-report=html
```

### Pipeline CI/CD
El pipeline `.github/workflows/unit-tests.yml` se ejecuta automáticamente en:
- Push a `main` o `develop`
- Pull requests a `main` o `develop`

**El pipeline falla si:**
- Alguna prueba no pasa
- El coverage es menor al 70%

---

## Validación de Requisitos

✅ **Al menos un escenario de prueba por endpoint:**
- `/` → 1 prueba
- `/blacklist/ping` → 1 prueba
- `POST /blacklist` → 7 pruebas
- `GET /blacklist/<email>` → 3 pruebas

✅ **Coverage >= 70%:** Actual 90.54%

✅ **Validación ante futuras modificaciones:**
- Pipeline automático en GitHub Actions
- Falla si coverage < 70%
- Falla si alguna prueba no pasa

---

## Tecnología

- **Framework:** pytest
- **Mocking:** unittest.mock
- **Coverage:** pytest-cov
- **CI/CD:** GitHub Actions
