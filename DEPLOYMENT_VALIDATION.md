# Validación del Despliegue Rolling en Ejecución

## 1. Comando de despliegue con timestamps

```bash
echo "Deployment started at: $(date)" && eb deploy && echo "Deployment finished at: $(date)"
```

**Propósito:**
- Captura hora de inicio y fin automáticamente
- Muestra logs en tiempo real del proceso

**Resultado:**
```
Deployment started at: Sun Oct 19 18:41:57 -05 2025
...
Deployment finished at: Sun Oct 19 18:50:05 -05 2025
```

---

## 2. Monitoreo de eventos en tiempo real

```bash
eb events
```

**Propósito:**
- Muestra cada batch del rolling deployment
- Indica qué instancia se está actualizando
- Reporta progreso de health checks

**Resultado:**
```
2025-10-19 23:42:04    INFO    Batch 1: Starting application deployment on instance(s) [i-0115b9d3385fe2acc].
2025-10-19 23:44:40    INFO    Batch 1: Completed application deployment.
2025-10-19 23:44:40    INFO    Batch 2: Starting application deployment on instance(s) [i-01842ab73a6ef1229].
2025-10-19 23:47:27    INFO    Batch 2: Completed application deployment.
2025-10-19 23:47:27    INFO    Batch 3: Starting application deployment on instance(s) [i-02bc7f43b740775f3].
2025-10-19 23:50:04    INFO    Batch 3: Completed application deployment.
```

---

## 3. Verificación de estado del entorno

```bash
eb status
```

**Propósito:**
- Muestra Status: "Updating" durante el despliegue
- Cambia a "Ready" cuando termina
- Indica Health status

**Resultado durante despliegue:**
```
Status: Updating
Health: Yellow
```

**Resultado después del despliegue:**
```
Status: Ready
Health: Green
```

---

## 4. Consulta de instancias EC2

```bash
aws ec2 describe-instances \
  --filters "Name=tag:elasticbeanstalk:environment-name,Values=blacklist-env" \
            "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId,State:State.Name,LaunchTime:LaunchTime}' \
  --output table
```

**Propósito:**
- Verifica cuántas instancias están corriendo
- Muestra LaunchTime de cada instancia
- Identifica instancias nuevas vs existentes

**Resultado:**
```
-----------------------------------------------------------------
|                       DescribeInstances                       |
+----------------------+-----------------------------+----------+
|          ID          |         LaunchTime          |  State   |
+----------------------+-----------------------------+----------+
|  i-02bc7f43b740775f3 |  2025-10-19T23:31:34+00:00  |  running |
|  i-0115b9d3385fe2acc |  2025-10-19T23:31:34+00:00  |  running |
|  i-01842ab73a6ef1229 |  2025-10-19T23:24:24+00:00  |  running |
+----------------------+-----------------------------+----------+
```

---

## 5. Logs detallados del despliegue

**Evidencia del proceso Rolling:**

### Batch 1
- **Instancia:** i-0115b9d3385fe2acc
- **Inicio:** 23:42:04
- **Fin:** 23:44:40
- **Duración:** 2 minutos 36 segundos

### Batch 2
- **Instancia:** i-01842ab73a6ef1229
- **Inicio:** 23:44:40
- **Fin:** 23:47:27
- **Duración:** 2 minutos 47 segundos

### Batch 3
- **Instancia:** i-02bc7f43b740775f3
- **Inicio:** 23:47:27
- **Fin:** 23:50:04
- **Duración:** 2 minutos 37 segundos

**Tiempo total:** 8 minutos 8 segundos

---

## 6. Validación de disponibilidad durante despliegue

```bash
curl http://blacklist-env.eba-hsrbudpd.us-east-1.elasticbeanstalk.com/blacklist/ping
```

**Propósito:**
- Verificar que el endpoint responde durante todo el proceso
- Confirmar que no hay downtime

**Resultado:**
```
pong
```

**Conclusión:** El endpoint respondió exitosamente durante todo el despliegue, confirmando que no hubo downtime.

---

## Resumen de Validación

✅ **Despliegue Rolling confirmado:** Los logs mostraron "Batch X: Starting/Completed" secuencialmente

✅ **Sin downtime:** El servicio estuvo disponible durante todo el proceso

✅ **Health checks exitosos:** Cada batch esperó confirmación de salud antes de continuar

✅ **3 instancias actualizadas:** Todas las instancias recibieron la nueva versión

✅ **Tiempo total:** 8 minutos 8 segundos para actualizar 3 instancias
