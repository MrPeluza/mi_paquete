# Reporte de Seguridad: OpenClaw & Ollama (LLM Local)

**Equipo auditor:** Manuel Rivera
**Fecha:** 27 de abril de 2026 
**Versión de OpenClaw auditada:** v2026.5.4 

### Especificaciones de hardware del entorno de prueba:
* **CPU:** Intel i5 12400f 
* **RAM:** 32GB DDR5 5600MHz
* **GPU:** RTX 4070Ti (12GB VRAM) 
* **Almacenamiento:** SSD 1TB 

---

## 1. Resumen ejecutivo
Se realizó una auditoría de seguridad a la instalación y ejecución de **OpenClaw** y **Ollama** dentro de contenedores Docker en un entorno Windows 10/11 utilizando el subsistema de Linux para Windows (WSL2). El análisis se enfocó en la configuración de parámetros de red, persistencia de datos, gestión de permisos y seguridad del acceso en entornos locales.

Se concluye que la arquitectura presentada es **segura para entornos locales**, siempre que se apliquen estrictamente las configuraciones detalladas en la guía técnica adjunta.

---

## 2. Alcance de la auditoría
### Elementos auditados:
* **Dockerización:** Revisión del archivo `docker-compose.yml`.
* **Permisos:** Configuración de volúmenes y contenedores en el host.
* **Red:** Aislamiento de puertos y redireccionamiento en bucle local (*loopback*).
* **Tráfico:** Enlace entre contenedores y comprobación de flujo solicitud-respuesta.

### Elementos fuera de alcance:
* Código fuente de OpenClaw.
* Binarios raíz de Ollama.

---

## 3. Arquitectura auditada

| Configuración | Descripción | Flujo de Datos (Stack) |
| :--- | :--- | :--- |
| **Configuración A** | Instalación inicial orientada a despliegue rápido con tokens locales. | Windows Explorer → CMD → Docker Engine → OpenClaw-Server → Imágenes de OpenClaw & Ollama. |
| **Configuración B** | Integración avanzada con persistencia y autenticación externa. | WSL 2 (Ubuntu) → Docker Compose → OpenClaw → Archivo `.env` (API Key de OpenRouter). |

---

## 4. Hallazgos y mitigaciones

### 4.1 Exposición del contenedor Ollama
* **Severidad:** **ALTA**.
* **Observación:** En la configuración inicial, Ollama requería una dirección "abierta" expuesta en un puerto específico para conectarse con OpenClaw.
* **Evidencia:** Uso de la dirección `0.0.0.0` en el campo `vars` del archivo `openclaw.json`, lo que permitía solicitudes de terceros dentro de la misma red local.
* **Estado:** **Resuelto.** Se actualizó el `docker-compose.yml` para que Ollama escuche en `0.0.0.0` solo dentro de la red interna de Docker, aislándolo en el bucle local `127.0.0.1`. Ahora OpenClaw se conecta mediante el nombre del servicio: `http://ollama-server:11434`.

### 4.2 Error de conexión entre OpenClaw y Ollama
* **Severidad:** **ALTA**.
* **Observación:** Las actualizaciones recientes de OpenClaw tienden a corromper datos configurados previamente, provocando que el sistema no reconozca a Ollama como proveedor de IA.
* **Evidencia:** Logs de Docker muestran que, tras actualizaciones, OpenClaw ignora la configuración de `docker-compose.yml` y utiliza proveedores preestablecidos.
* **Estado:** **Investigación en curso.** Se ha mitigado eliminando archivos `.md` en la carpeta `.openclaw/workspace` y borrando manualmente el contenedor para recrear la imagen.

### 4.3 Autorización del contenedor Ollama a nivel ROOT
* **Severidad:** **BAJA**.
* **Observación:** Ollama requiere privilegios de superusuario para acceder a los drivers y núcleos de la GPU.
* **Evidencia:** Verificación de permisos en WSL2 confirma que `ollama-server` opera con privilegios de root.
* **Estado:** **Mitigado.** El contenedor está aislado en una red de bucle local. Si un atacante traspasa la barrera, quedaría confinado al contenedor de Ollama sin posibilidad de escalar hacia el host.

---

## 5. Riesgos residuales
El riesgo derivado de los permisos root en Ollama se considera mínimo debido al aislamiento de red. El sistema permite detectar solicitudes sospechosas en los logs y eliminar el contenedor de forma inmediata para mitigar cualquier amenaza detectada.

---

## 6. Recomendaciones de seguridad
1. **Monitoreo de logs:** Revisar periódicamente los registros de Ollama y OpenClaw para identificar solicitudes inusuales en estado de reposo.
2. **Auditoría de puertos:** Utilizar el comando `netstat -ano | findstr :"PUERTO"` para verificar qué servicios están escuchando activamente.
3. **Cifrado:** Implementar cifrado en los volúmenes del área de trabajo para proteger los datos persistentes.
4. **Privilegio mínimo:** Aplicar estrictamente el principio de mínimo privilegio detallado en el manual de instalación.

---

## 7. Conclusión
El ecosistema **OpenClaw & Ollama** queda **APROBADO** bajo la **Configuración A**. El cumplimiento de la seguridad depende estrictamente de seguir la guía de configuración establecida. Se advierte que no existe aún una solución definitiva para prevenir la corrupción de la carpeta `.openclaw` tras actualizaciones del software.
