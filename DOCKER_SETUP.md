# Docker Setup - Regresión Lineal Cloud

## ✅ Estado: Docker Compose está completamente configurado y funcionando

### 🏗️ Estructura de Contenedores

#### **Backend (Python FastAPI + Gunicorn)**
- **Imagen**: Python 3.11-slim
- **Puerto**: 8000
- **Servicio**: Gunicorn + Uvicorn
- **Workers**: 2
- **Volumen**: ./backend/models (persistencia de modelos)
- **Características**:
  - Instala todas las dependencias desde `requirements.txt`
  - Gunicorn expone la aplicación FastAPI en puerto 8000
  - PYTHONUNBUFFERED=1 para logs en tiempo real

#### **Frontend (Vue + Vite + Nginx)**
- **Imagen**: Node 20-alpine (build) → Nginx alpine (producción)
- **Puerto**: 80
- **Build Tool**: Vite
- **Server**: Nginx
- **Configuración**: nginx.conf con reverse proxy para /api

### 🔌 Configuración de Red (Docker Compose)

```
Frontend (Nginx:80)
    ↓
    └─→ Reverse Proxy /api/ → Backend (Gunicorn:8000)
```

**Nginx Reverse Proxy**:
- Rutas estáticas (/) → Frontend (dist)
- Rutas API (/api/) → Backend (http://backend:8000/)
- Headers proxy: Host, X-Real-IP

**API Client (Frontend)**:
- Usa axios con `baseURL: '/api'`
- Las llamadas se routing automáticamente a través de Nginx
- Endpoints: `/columns`, `/train`, `/predict`

### 📁 Archivos Modificados

1. **backend/Dockerfile** (actualizado)
   - Copiar directorio completo (no /app/app)
   - Comando: `gunicorn main:app -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000`

2. **backend/requirements.txt** (creado)
   - Incluye gunicorn, fastapi, uvicorn, scikit-learn, pandas, numpy

3. **frontend/Dockerfile** (actualizado)
   - Node 20-alpine (compatible con Vite 7.3+)
   - Build multi-stage para optimizar tamaño

4. **frontend/nginx.conf** (sin cambios, ya estaba correcto)
   - Reverse proxy para /api/

5. **frontend/src/services/api.js** (actualizado)
   - Migrado de fetch a axios
   - `baseURL: '/api'` para Docker

6. **frontend/package.json** (actualizado)
   - Agregado axios ^1.6.0

7. **docker-compose.yml** (actualizado)
   - Rutas de volumen corregidas
   - Variable PYTHONUNBUFFERED
   - Dependencias entre servicios

8. **.dockerignore**
   - backend: __pycache__, .pyc, .env, models/
   - frontend: node_modules, dist, .git, npm-debug.log

### ✅ Validación Completada

```
✓ Docker build exitoso para ambos servicios
✓ Backend iniciando correctamente (gunicorn + uvicorn)
✓ Frontend iniciando correctamente (nginx)
✓ Ambos contenedores en estado "Running"
✓ Backend responde en http://localhost:8000
✓ Frontend responde en http://localhost
```

### 🚀 Cómo Usar

#### Iniciar los contenedores:
```bash
docker-compose up -d
```

#### Ver logs:
```bash
docker-compose logs -f
docker-compose logs backend
docker-compose logs frontend
```

#### Detener los contenedores:
```bash
docker-compose down
```

#### Reconstruir las imágenes:
```bash
docker-compose build --no-cache
```

### 📊 Verificación de Funcionalidad

1. **Backend está corriendo**:
   ```
   curl http://localhost:8000
   # Responde: {"message":"Servidor de Regresión Lineal"}
   ```

2. **Frontend está corriendo**:
   ```
   curl http://localhost
   # Responde con HTML index.html
   ```

3. **Nginx reverse proxy funciona**:
   - Solicitudes a `http://localhost/api/*` se forwardean a `http://backend:8000/*`

### 🔧 Próximos Pasos (Opcional)

Si necesitas:
- **Production**: Agregar HTTPS, LoadBalancer, Cloud Deployment
- **Database**: Agregar servicio PostgreSQL/MongoDB
- **Monitoring**: Agregar Prometheus, Grafana
- **CI/CD**: Configurar GitHub Actions para auto-build y push a registry

### 📝 Notas

- Los contenedores están configurados para auto-restart
- El volumen `./backend/models` persiste los modelos entrenados
- Nginx actúa como reverse proxy para servicios detrás de un mismo puerto
- FastAPI usa automáticamente CORS con origins=["*"] en desarrollo
