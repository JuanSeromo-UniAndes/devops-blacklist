# Blacklist API - Documentación Oficial

## Información General
- **Base URL**: `http://localhost:5000` (local) / `https://your-aws-url.com` (producción)
- **Autenticación**: JWT Bearer Token
- **Content-Type**: `application/json`

---

## 🔗 Endpoints

### 1. Health Check
**Verificar estado de la API**

```http
GET /blacklist/ping
```

**Parámetros**: Ninguno

**Respuesta Exitosa (200)**:
```
pong
```

**Ejemplo de uso**:
```bash
curl http://localhost:5000/blacklist/ping
```

---

### 2. Agregar Email a Blacklist
**Agregar un email a la lista negra**

```http
POST /blacklist
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Parámetros del Body**:
| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| email | string | ✅ | Email válido a bloquear |
| app_uuid | string | ✅ | UUID de la aplicación |
| blocked_reason | string | ❌ | Razón del bloqueo |

**Ejemplo de Request**:
```json
{
  "email": "spammer@example.com",
  "app_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "blocked_reason": "Actividad de spam detectada"
}
```

**Respuesta Exitosa (201)**:
```json
{
  "message": "Email successfully added to blacklist"
}
```

**Respuestas de Error**:
- **400**: Email ya existe o datos inválidos
- **401**: Token faltante o inválido

**Ejemplo de uso**:
```bash
curl -X POST http://localhost:5000/blacklist \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","app_uuid":"550e8400-e29b-41d4-a716-446655440000","blocked_reason":"Test"}'
```

---

### 3. Verificar Email en Blacklist
**Consultar si un email está en la lista negra**

```http
GET /blacklist/{email}
Authorization: Bearer {jwt_token}
```

**Parámetros de URL**:
| Campo | Tipo | Descripción |
|-------|------|-------------|
| email | string | Email a verificar |

**Respuesta Exitosa (200) - Email Bloqueado**:
```json
{
  "existing": true,
  "blocked_reason": "Actividad de spam detectada"
}
```

**Respuesta Exitosa (200) - Email No Bloqueado**:
```json
{
  "existing": false
}
```

**Respuestas de Error**:
- **401**: Token faltante o inválido

**Ejemplo de uso**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/blacklist/test@example.com
```

---

## 🔐 Autenticación

### Generar Token JWT
```bash
python gen_token.py
```

### Usar Token en Requests
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📋 Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| 200 | Operación exitosa |
| 201 | Recurso creado exitosamente |
| 400 | Datos inválidos o email duplicado |
| 401 | No autorizado (token faltante) |
| 422 | Token JWT inválido |
| 500 | Error interno del servidor |

---

## 🧪 Casos de Prueba

### Escenario 1: Flujo Completo Exitoso
1. **Health Check**: `GET /blacklist/ping` → `pong`
2. **Agregar Email**: `POST /blacklist` → `201 Created`
3. **Verificar Email**: `GET /blacklist/{email}` → `{"existing": true}`

### Escenario 2: Validaciones
1. **Email Duplicado**: `POST /blacklist` (mismo email) → `400 Bad Request`
2. **Email Inválido**: `POST /blacklist` (formato incorrecto) → `400 Bad Request`
3. **UUID Inválido**: `POST /blacklist` (UUID malformado) → `400 Bad Request`

### Escenario 3: Seguridad
1. **Sin Token**: `GET /blacklist/{email}` → `401 Unauthorized`
2. **Token Inválido**: Con token malformado → `422 Unprocessable Entity`

---

## 📦 Colección de Postman

**Archivo**: `Blacklist_API.postman_collection.json`

**Variables requeridas**:
- `base_url`: URL base de la API
- `jwt_token`: Token JWT generado

**Importar en Postman**:
1. Abrir Postman
2. Import → Seleccionar archivo JSON
3. Configurar variables de entorno
4. Ejecutar pruebas

---

## 🚀 Despliegue

### Local
```bash
python app.py
# API disponible en http://localhost:5000
```

### AWS Elastic Beanstalk
```bash
eb init
eb create blacklist-env
eb deploy
# API disponible en https://blacklist-env.region.elasticbeanstalk.com
```

---

## 📞 Soporte

Para reportar problemas o solicitar funcionalidades, contactar al equipo de desarrollo.