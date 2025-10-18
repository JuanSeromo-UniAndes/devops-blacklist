# Publicar Documentación de la API

## Opciones para Publicar la Documentación

### 1. GitHub Pages (Recomendado)
```bash
# 1. Subir proyecto a GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/blacklist-api.git
git push -u origin main

# 2. Habilitar GitHub Pages
# - Ir a Settings > Pages
# - Source: Deploy from branch
# - Branch: main / (root)
# - La documentación estará en: https://tu-usuario.github.io/blacklist-api/
```

### 2. Postman Public Documentation
```bash
# 1. En Postman, seleccionar la colección
# 2. Click en "..." > "Publish Docs"
# 3. Configurar y publicar
# 4. Obtienes URL pública como: https://documenter.getpostman.com/view/xxx/xxx
```

### 3. GitBook (Alternativa)
```bash
# 1. Crear cuenta en GitBook.com
# 2. Importar desde GitHub
# 3. Sincronizar automáticamente
# 4. URL pública: https://tu-espacio.gitbook.io/blacklist-api/
```

## URLs de Documentación

### Para el Informe de Arquitectura:

**Documentación Local**:
- README: `./README.md`
- API Docs: `./API_DOCUMENTATION.md`
- Postman Collection: `./Blacklist_API.postman_collection.json`

**URLs Públicas** (actualizar después de publicar):
- GitHub Pages: `https://tu-usuario.github.io/blacklist-api/`
- Postman Docs: `https://documenter.getpostman.com/view/xxx/xxx`
- API Endpoint: `https://blacklist-env.region.elasticbeanstalk.com`

## Pasos Siguientes

1. ✅ Documentación creada
2. ✅ Colección de Postman lista
3. ⏳ Subir a GitHub
4. ⏳ Publicar documentación
5. ⏳ Obtener URL pública
6. ⏳ Agregar URL al informe de arquitectura