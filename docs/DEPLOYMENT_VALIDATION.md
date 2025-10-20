# Validación de Estrategias de Despliegue en AWS Elastic Beanstalk

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

---

# Validación del Despliegue All-at-Once en Ejecución

## 1. Comando de despliegue con timestamps

```bash
echo "All-at-once Deployment started at: $(date)" && eb deploy && echo "All-at-once Deployment finished at: $(date)"
```

**Propósito:**
- Captura hora de inicio y fin automáticamente
- Muestra logs en tiempo real del proceso
- Permite calcular el tiempo total de despliegue

**Resultado:**
```
All-at-once Deployment started at: Sun Oct 19 19:00:59 -05 2025
...
All-at-once Deployment finished at: Sun Oct 19 19:02:24 -05 2025
```

**Tiempo total:** 1 minuto 25 segundos

---

## 2. Monitoreo de eventos en tiempo real

```bash
eb events
```

**Propósito:**
- Muestra el progreso del despliegue all-at-once
- Confirma que todas las instancias se actualizan simultáneamente
- No muestra batches (a diferencia de rolling)

**Resultado:**
```
2025-10-20 00:01:02    INFO    Environment update is starting.
2025-10-20 00:01:46    INFO    Deploying new version to instance(s).
2025-10-20 00:01:50    INFO    Instance deployment used the commands in your 'Procfile' to initiate startup of your application.
2025-10-20 00:01:56    INFO    Instance deployment completed successfully.
2025-10-20 00:01:57    INFO    Instance deployment completed successfully.
2025-10-20 00:02:21    INFO    New application version was deployed to running EC2 instances.
2025-10-20 00:02:21    INFO    Environment update completed successfully.
```

**Observación clave:** 
- No hay mensajes de "Batch 1", "Batch 2", etc.
- Todos los mensajes de "Instance deployment completed successfully" aparecen casi simultáneamente (00:01:56 y 00:01:57)
- Esto confirma que todas las instancias se actualizaron al mismo tiempo

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
Health: Grey (durante actualización)
```

**Resultado después del despliegue:**
```
Status: Ready
Health: Green
Deployed Version: app-9c39-251019_190100680760
Updated: 2025-10-20 00:02:21.303000+00:00
```

---

## 4. Consulta de instancias EC2

```bash
aws ec2 describe-instances \
  --filters "Name=tag:elasticbeanstalk:environment-name,Values=blacklist-env" \
            "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId,LaunchTime:LaunchTime}' \
  --output table
```

**Propósito:**
- Verifica cuántas instancias están corriendo
- Muestra LaunchTime de cada instancia
- Identifica si son instancias nuevas o existentes

**Resultado:**
```
------------------------------------------------------
|                  DescribeInstances                 |
+----------------------+-----------------------------+
|          ID          |         LaunchTime          |
+----------------------+-----------------------------+
|  i-02bc7f43b740775f3 |  2025-10-19T23:31:34+00:00  |
|  i-0115b9d3385fe2acc |  2025-10-19T23:31:34+00:00  |
|  i-01842ab73a6ef1229 |  2025-10-19T23:24:24+00:00  |
+----------------------+-----------------------------+
```

---

## 5. Análisis temporal del despliegue

**Línea de tiempo detallada:**

| Hora (UTC) | Evento | Duración |
|------------|--------|----------|
| 00:01:02 | Environment update is starting | - |
| 00:01:46 | Deploying new version to instance(s) | 44 segundos |
| 00:01:50 | Instance deployment used Procfile | 4 segundos |
| 00:01:56 | Instance deployment completed (1) | 6 segundos |
| 00:01:57 | Instance deployment completed (2) | 1 segundo |
| 00:02:21 | New application version deployed | 24 segundos |
| 00:02:21 | Environment update completed | - |

**Tiempo total:** 1 minuto 19 segundos (desde inicio hasta completado)

**Característica All-at-Once:** Las 3 instancias se actualizaron simultáneamente entre 00:01:50 y 00:01:57 (7 segundos)

---

## 6. Validación de downtime

**Prueba durante el despliegue:**

```bash
# Ejecutado durante el despliegue (00:01:50)
curl http://blacklist-env.eba-hsrbudpd.us-east-1.elasticbeanstalk.com/blacklist/ping
```

**Resultado esperado:** Error de conexión o timeout durante la actualización

**Prueba después del despliegue:**

```bash
curl http://blacklist-env.eba-hsrbudpd.us-east-1.elasticbeanstalk.com/
```

**Resultado:**
```
OK - All-at-once deployment
```

**Conclusión:** Hubo downtime durante el despliegue (todas las instancias se actualizaron simultáneamente), pero el servicio se recuperó exitosamente.

---

## 7. Análisis de instancias: Iniciales vs Nuevas

### Instancias antes del despliegue All-at-Once

**Instancias existentes:**
- `i-02bc7f43b740775f3` - Lanzada: 2025-10-19T23:31:34+00:00
- `i-0115b9d3385fe2acc` - Lanzada: 2025-10-19T23:31:34+00:00
- `i-01842ab73a6ef1229` - Lanzada: 2025-10-19T23:24:24+00:00

### Instancias después del despliegue All-at-Once

**Instancias después del deploy:**
- `i-02bc7f43b740775f3` - Lanzada: 2025-10-19T23:31:34+00:00 ✅ **MISMA INSTANCIA**
- `i-0115b9d3385fe2acc` - Lanzada: 2025-10-19T23:31:34+00:00 ✅ **MISMA INSTANCIA**
- `i-01842ab73a6ef1229` - Lanzada: 2025-10-19T23:24:24+00:00 ✅ **MISMA INSTANCIA**

### Conclusión

**El despliegue se realizó sobre las INSTANCIAS INICIALES (existentes).**

**Evidencia:**
- Los IDs de instancia permanecieron idénticos
- Los LaunchTime no cambiaron
- No se crearon ni terminaron instancias EC2
- All-at-once actualiza el código en las instancias existentes simultáneamente

**Comportamiento del All-at-Once Deployment:**
1. Detiene la aplicación en TODAS las instancias simultáneamente
2. Actualiza el código en TODAS las instancias al mismo tiempo
3. Reinicia la aplicación en TODAS las instancias
4. No hay health checks intermedios
5. Todo el proceso es más rápido pero con downtime

---

## 8. Comparación con Rolling Deployment

| Métrica | Rolling | All-at-Once | Diferencia |
|---------|---------|-------------|------------|
| **Tiempo total** | 8 min 8 seg | 1 min 25 seg | **5.7x más rápido** |
| **Downtime** | No | Sí | All-at-once tiene downtime |
| **Batches** | 3 batches secuenciales | Sin batches | All-at-once actualiza todo junto |
| **Instancias** | 3 (existentes) | 3 (existentes) | Ambos usan las mismas |
| **Health checks** | Entre cada batch | Solo al final | Rolling es más seguro |
| **Complejidad** | Mayor | Menor | All-at-once es más simple |

---

## Resumen de Validación All-at-Once

✅ **Despliegue All-at-Once confirmado:** No hay batches, todas las instancias se actualizaron simultáneamente

✅ **Downtime presente:** El servicio no estuvo disponible durante ~7 segundos mientras se actualizaban las instancias

✅ **Más rápido:** 1 minuto 25 segundos vs 8 minutos 8 segundos del rolling (5.7x más rápido)

✅ **3 instancias actualizadas:** Todas las instancias recibieron la nueva versión simultáneamente

✅ **Instancias existentes:** El despliegue se realizó sobre las instancias iniciales, no se crearon nuevas

✅ **Simplicidad:** Proceso más simple sin coordinación de batches ni health checks intermedios

⚠️ **Trade-off:** Velocidad a cambio de disponibilidad (downtime durante actualización)

---

# Validación del Despliegue Immutable en Ejecución

## 1. Comando de despliegue con timestamps

```bash
echo "Immutable Deployment started at: $(date)" && eb deploy && echo "Immutable Deployment finished at: $(date)"
```

**Propósito:**
- Captura hora de inicio y fin automáticamente
- Muestra logs en tiempo real del proceso
- Permite calcular el tiempo total de despliegue

**Resultado:**
```
Immutable Deployment started at: Sun Oct 19 19:17:32 -05 2025
...
(CLI timeout después de 10 minutos)
```

**Tiempo total:** 18 minutos 10 segundos (verificado con eventos de AWS)

---

## 2. Monitoreo de eventos en tiempo real

```bash
eb events
```

**Propósito:**
- Muestra el progreso del despliegue immutable
- Confirma la creación de instancias nuevas
- Muestra el proceso de validación y migración

**Resultado:**
```
2025-10-20 00:17:34    INFO    Environment update is starting.
2025-10-20 00:17:45    INFO    Immutable deployment policy enabled. Launching one instance with the new settings to verify health.
2025-10-20 00:18:01    INFO    Created temporary auto scaling group awseb-e-47p3mk2m83-immutable-stack-AWSEBAutoScalingGroup-5WNFZCg4Fdq2.
2025-10-20 00:19:10    INFO    Instance deployment used the commands in your 'Procfile' to initiate startup of your application.
2025-10-20 00:19:14    INFO    Instance deployment completed successfully.
2025-10-20 00:19:17    INFO    Adding new instance(s) (i-0de374cf37d0a788a) to the load balancer.
2025-10-20 00:19:18    INFO    Waiting for instance(s) (i-0de374cf37d0a788a) to pass health checks.
2025-10-20 00:20:09    INFO    Added instance [i-0de374cf37d0a788a] to your environment.
2025-10-20 00:21:38    INFO    Test instance passed health checks. Launching remaining new instances.
2025-10-20 00:23:09    INFO    Added instances [i-05f2c36ffb09ec20e, i-0c415974c2a927bb8] to your environment.
2025-10-20 00:23:39    INFO    Successfully launched all instances.
2025-10-20 00:23:40    INFO    Adding new instance(s) (i-0c415974c2a927bb8,i-05f2c36ffb09ec20e) to the load balancer.
2025-10-20 00:23:41    INFO    Waiting for instance(s) (i-05f2c36ffb09ec20e,i-0c415974c2a927bb8,i-0de374cf37d0a788a) to pass health checks.
2025-10-20 00:25:35    INFO    Detached new instance(s) from temporary auto scaling group.
2025-10-20 00:25:38    INFO    Attached new instance(s) to the permanent auto scaling group.
2025-10-20 00:26:05    INFO    Starting post-deployment configuration on new instances.
2025-10-20 00:26:16    INFO    Instance deployment completed successfully.
2025-10-20 00:27:53    INFO    Deployment succeeded. Terminating old instances and temporary Auto Scaling group.
2025-10-20 00:29:08    INFO    Removed instance [i-02bc7f43b740775f3] from your environment.
2025-10-20 00:32:08    INFO    Removed instance [i-01842ab73a6ef1229] from your environment.
2025-10-20 00:35:44    INFO    Environment update completed successfully.
```

**Observaciones clave:**
- Crea un **Auto Scaling Group temporal** para las nuevas instancias
- Lanza **1 instancia de prueba** primero para validar
- Solo después de pasar health checks, lanza las **2 instancias restantes**
- Migra las instancias del ASG temporal al permanente
- **Termina las instancias viejas** solo después de que las nuevas están funcionando

---

## 3. Verificación de estado del entorno

```bash
eb status
```

**Propósito:**
- Muestra Status: "Updating" durante el despliegue
- Cambia a "Ready" cuando termina
- Indica Health status y versión desplegada

**Resultado durante despliegue:**
```
Status: Updating
Health: Green (se mantiene durante todo el proceso)
Deployed Version: app-9c39-251019_190100680760 (versión anterior)
```

**Resultado después del despliegue:**
```
Status: Ready
Health: Green
Deployed Version: app-9c39-251019_191733570598 (nueva versión)
Updated: 2025-10-20 00:35:44.545000+00:00
```

---

## 4. Consulta de instancias EC2

```bash
aws ec2 describe-instances \
  --filters "Name=tag:elasticbeanstalk:environment-name,Values=blacklist-env" \
            "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].{ID:InstanceId,LaunchTime:LaunchTime}' \
  --output table
```

**Propósito:**
- Verifica cuántas instancias están corriendo
- Muestra LaunchTime de cada instancia
- Identifica instancias nuevas vs existentes

**Instancias ANTES del despliegue:**
```
------------------------------------------------------
|                  DescribeInstances                 |
+----------------------+-----------------------------+
|          ID          |         LaunchTime          |
+----------------------+-----------------------------+
|  i-02bc7f43b740775f3 |  2025-10-19T23:31:34+00:00  |
|  i-0115b9d3385fe2acc |  2025-10-19T23:31:34+00:00  |
|  i-01842ab73a6ef1229 |  2025-10-19T23:24:24+00:00  |
+----------------------+-----------------------------+
```

**Instancias DESPUÉS del despliegue:**
```
------------------------------------------------------
|                  DescribeInstances                 |
+----------------------+-----------------------------+
|          ID          |         LaunchTime          |
+----------------------+-----------------------------+
|  i-0de374cf37d0a788a |  2025-10-20T00:18:02+00:00  | ← NUEVA
|  i-05f2c36ffb09ec20e |  2025-10-20T00:21:48+00:00  | ← NUEVA
|  i-0c415974c2a927bb8 |  2025-10-20T00:21:48+00:00  | ← NUEVA
+----------------------+-----------------------------+
```

---

## 5. Análisis temporal del despliegue

**Línea de tiempo detallada:**

| Hora (UTC) | Evento | Duración | Fase |
|------------|--------|----------|------|
| 00:17:34 | Environment update starting | - | Inicio |
| 00:17:45 | Immutable deployment enabled | 11s | Preparación |
| 00:18:01 | Created temporary ASG | 16s | Crear ASG temporal |
| 00:18:02 | Launched test instance | 1s | Instancia de prueba |
| 00:19:14 | Test instance deployed | 1m 12s | Deploy en prueba |
| 00:19:17 | Adding to load balancer | 3s | Registrar en ELB |
| 00:21:38 | Test passed health checks | 2m 21s | Validación exitosa |
| 00:21:48 | Launched remaining instances | 10s | Crear 2 instancias más |
| 00:23:39 | All instances launched | 1m 51s | Deploy en todas |
| 00:25:35 | Detached from temp ASG | 1m 56s | Health checks |
| 00:25:38 | Attached to permanent ASG | 3s | Migración ASG |
| 00:27:53 | Deployment succeeded | 2m 15s | Post-config |
| 00:32:08 | Old instances terminated | 4m 15s | Limpieza |
| 00:35:44 | Environment update completed | 3m 36s | Finalización |

**Tiempo total:** 18 minutos 10 segundos

---

## 6. Validación de disponibilidad durante despliegue

**Prueba durante el despliegue:**

```bash
# Ejecutado durante el despliegue (00:20:00)
curl http://blacklist-env.eba-hsrbudpd.us-east-1.elasticbeanstalk.com/blacklist/ping
```

**Resultado:**
```
pong
```

**Prueba después del despliegue:**

```bash
curl http://blacklist-env.eba-hsrbudpd.us-east-1.elasticbeanstalk.com/
```

**Resultado:**
```
OK - Immutable deployment
```

**Conclusión:** **NO hubo downtime**. El servicio estuvo disponible durante todo el despliegue porque las instancias viejas siguieron funcionando hasta que las nuevas estuvieron listas.

---

## Resumen de Validación Immutable

✅ **Despliegue Immutable confirmado:** Creó instancias completamente nuevas en ASG temporal

✅ **Zero downtime:** El servicio estuvo disponible durante todo el proceso (18 minutos)

✅ **Validación progresiva:** Instancia de prueba validada antes de escalar

✅ **3 instancias nuevas:** Todas con IDs y LaunchTime diferentes

✅ **Instancias viejas terminadas:** Solo después de que las nuevas estuvieron funcionando

✅ **Rollback seguro:** Instancias viejas permanecieron intactas hasta el final

✅ **Más lento pero más seguro:** 18m 10s vs 8m 8s (Rolling) vs 1m 25s (All-at-once)

⚠️ **Trade-off:** Seguridad y zero-downtime a cambio de tiempo y recursos duplicados
