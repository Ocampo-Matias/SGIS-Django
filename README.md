# SGIS - Sistema de Gestión de Incidentes de Seguridad

SGIS es una aplicación web monolítica desarrollada con el framework **Django (Python)** diseñada para registrar, clasificar y realizar el seguimiento de incidentes de seguridad de la información. Este proyecto fue desarrollado como parte de mi formación académica para demostrar habilidades prácticas en el diseño de bases de datos relacionales, el control de acceso basado en roles (RBAC) y la implementación de lógica de negocio del lado del servidor.

---

## 📋 Descripción del Proyecto

El sistema centraliza la gestión de incidentes (como phishing, malware, filtraciones de datos o ataques DDoS) permitiendo a un equipo de seguridad asignarlos, actualizar sus estados de resolución y añadir comentarios colaborativos.

El núcleo técnico de este proyecto radica en la delimitación estricta de permisos según el rol asignado al usuario en el sistema.

---

## 🛠️ Tecnologías Utilizadas

*   **Framework Principal:** Django 5.0.7 (Python)
*   **Base de Datos:** PostgreSQL (Soporta fallback local y configuración automatizada para despliegue en la nube vía `dj-database-url`)
*   **Gestión de Formularios:** Django ModelForms y `django-widget-tweaks` para mejorar la integración de estilos.
*   **Servidor y Despliegue:** Preparado para despliegue en entornos como Render/Heroku mediante `gunicorn`/`uvicorn` y manejo optimizado de archivos estáticos con `WhiteNoise`.
*   **Interfaz de Usuario:** HTML5, plantillas integradas de Django y Bootstrap 4.

---

## ⚙️ Arquitectura y Diseño de Datos

El proyecto cuenta con tres entidades principales en su modelo de base de datos relacional:

1.  **CustomUser:** Extiende el modelo `AbstractUser` de Django para incorporar un campo de control de roles (`upper_level`, `medium_level`, `low_level`).
2.  **Incidents:** Almacena la información de cada incidente (tipo, descripción, prioridad, estado actual, historial y el usuario asignado).
3.  **Comment:** Mantiene la relación muchos a uno con los incidentes para el registro cronológico de anotaciones y actualizaciones del equipo técnico.

---

## 🔑 Funcionalidades Principales y Control de Acceso (RBAC)

La plataforma implementa un control de acceso basado en tres niveles de privilegios:

*   **Nivel Alto (`upper_level`):** Equivale al rol de Administrador. Puede gestionar usuarios (crear, listar, asignar roles y eliminar cuentas) y posee control total sobre la creación y edición de cualquier incidente.
*   **Nivel Medio (`medium_level`):** Equivale al rol de Analista de Seguridad. Puede registrar nuevos incidentes, autoasignarse incidentes o actualizar los estados de los casos asignados.
*   **Nivel Bajo (`low_level`):** Equivale al rol de Observador / Reportador. Tiene permisos para visualizar incidentes asignados y añadir comentarios para enriquecer la bitácora de análisis, pero no puede alterar la prioridad o los parámetros clave del incidente.

### Flujo del Ciclo de Vida del Incidente
El estado de los incidentes progresa a través de la siguiente máquina de estados sencilla:
`Nuevo (New)` ➡️ `En Progreso (In Progress)` ➡️ `Resuelto (Resolved)` ➡️ `Cerrado (Closed)`

*   Una vez que un incidente pasa a estado **Cerrado**, sus campos quedan bloqueados para su edición y pasa a ser de solo lectura para evitar alteraciones históricas, permitiendo únicamente su eliminación por parte de los administradores.

---

## 🖼️ Capturas de Pantalla (Placeholders)

> En esta sección se incluirán capturas de pantalla reales una vez completado el despliegue del proyecto.

| Vista Principal (Dashboard) | Gestión de Incidentes |
| :--- | :--- |
| `![Dashboard Placeholder](https://via.placeholder.com/600x400?text=Dashboard+SGIS)` | `![Incidentes Placeholder](https://via.placeholder.com/600x400?text=Lista+de+Incidentes)` |

---

## 🚀 Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local de desarrollo:

### Prerrequisitos
*   Python 3.10 o superior instalado.
*   Servidor PostgreSQL local o remoto.

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/SGIS-Django.git
cd SGIS-Django
```

### Paso 2: Crear y activar un entorno virtual
En Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
En Linux / macOS:
```bash
python -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar la base de datos
El proyecto utiliza `dj-database-url` para configurar la conexión. Por defecto, en desarrollo busca una base de datos local en `postgresql://postgres:postgres@localhost:5432/mysite`.

Puedes ajustar esto en la configuración o exportar una variable de entorno `DATABASE_URL` con tus credenciales:
```bash
# Ejemplo en Linux/macOS
export DATABASE_URL="postgresql://usuario:contraseña@localhost:5432/nombre_bd"

# Ejemplo en Windows (PowerShell)
$env:DATABASE_URL="postgresql://usuario:contraseña@localhost:5432/nombre_bd"
```

### Paso 5: Ejecutar migraciones y recolectar archivos estáticos
```bash
python manage.py migrate
python manage.py collectstatic --no-input
```

### Paso 6: Crear un usuario administrador (Superusuario)
Necesario para acceder al módulo de administración y al rol `upper_level`.
```bash
python manage.py createsuperuser
```
*(Durante la creación, asegúrate de asignarle el rol correspondiente a través de la consola de administración o ajustando el campo `role` en la base de datos).*

### Paso 7: Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```
La aplicación estará disponible en `http://127.0.0.1:8000/`.

---

## 💡 Aprendizajes Obtenidos

*   **Extensión de Modelos de Usuario en Django:** Comprendí la importancia práctica de heredar de `AbstractUser` al inicio del desarrollo del proyecto en lugar de usar el modelo predeterminado, facilitando la adición de campos personalizados sin comprometer la compatibilidad del ecosistema de autenticación de Django.
*   **Implementación de Middlewares y Decoradores Personalizados:** Desarrollé decoradores de funciones en Python para centralizar las comprobaciones de autorización por rol (`role_required`), evitando duplicar la lógica de validación en múltiples vistas.
*   **Gestión del Ciclo de Vida del Dato:** Diseñé lógica de validación del lado del servidor para garantizar que las transiciones de estado de un incidente (por ejemplo, de "Resuelto" a "Cerrado") sigan un flujo lógico coherente y cumplan con las restricciones de edición requeridas.

---

## 🚀 Posibles Mejoras Futuras

*   **Corrección de Seguridad en Decoradores:** Refactorizar el decorador `role_required` para instanciar correctamente la clase de respuesta (`return HttpResponseForbidden()`), previniendo posibles inconsistencias en el manejo de peticiones no autorizadas.
*   **Agregar Cobertura de Pruebas Unitarias:** Implementar casos de prueba automáticos en `tests.py` usando `django.test.TestCase` para verificar los flujos de creación de incidentes, edición por rol y autenticación.
*   **Módulo de Historial / Audit Log:** Sustituir el campo de texto simple `history_incident` por una tabla relacional independiente que registre automáticamente quién modificó cada campo y en qué fecha, permitiendo una trazabilidad real para auditorías.
*   **Implementación de API REST:** Migrar las vistas monolíticas actuales hacia endpoints estructurados utilizando Django Rest Framework (DRF) para facilitar una futura integración con interfaces tipo Single Page Applications (SPA).
