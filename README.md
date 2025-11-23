[LittleLemon_API_Documentation_ES.md](https://github.com/user-attachments/files/23697985/LittleLemon_API_Documentation_ES.md)
# Documentación de la API de LittleLemon

## 1. Objetivos

### 1.1. Objetivo Principal

Proporcionar una documentación completa de la API de LittleLemon, detallando sus endpoints, funcionalidades y uso, para facilitar su utilización y mantenimiento.

### 1.2. Objetivos Secundarios

*   Documentar cada uno de los endpoints de la API, incluyendo su URL, los métodos HTTP que soporta, el formato de solicitud esperado y las posibles respuestas.
*   Describir los diferentes roles de usuario y sus permisos dentro de la API.
*   Proporcionar una guía clara y concisa para probar la API y sus endpoints.

## 2. Introducción

La API de LittleLemon es un servicio web diseñado para gestionar las operaciones de un restaurante. Proporciona funcionalidades para gestionar usuarios, elementos del menú, categorías, carritos de compras y pedidos. La API está construida con Django y Django REST Framework, y utiliza autenticación basada en tokens para la seguridad.

Este documento proporciona una descripción detallada de los endpoints de la API y su uso. Está destinado a los desarrolladores que necesitan interactuar con la API, así como a los responsables de su mantenimiento y futuro desarrollo.

## 3. Desarrollo (Documentación de la API)

Esta sección detalla cada uno de los endpoints de la API.

### 3.1. Gestión de Usuarios

#### 3.1.1. Gerentes

##### **Endpoint: `/api/groups/manager/users/`**

*   **Descripción:** Este endpoint permite a un gerente recuperar una lista de todos los gerentes o agregar un usuario al grupo "Manager".
*   **Métodos HTTP:** `GET`, `POST`
*   **Permisos:** Solo los usuarios que pertenecen al grupo "Manager" pueden acceder a este endpoint.

**Solicitud GET**

*   **Descripción:** Recupera una lista de todos los usuarios en el grupo "Manager".
*   **Respuesta Exitosa (200 OK):**
    ```json
    [
        {
            "id": 1,
            "username": "manager_user",
            "email": "manager@example.com"
        },
        ...
    ]
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "No autorizado"
    }
    ```

**Solicitud POST**

*   **Descripción:** Agrega un usuario al grupo "Manager".
*   **Cuerpo de la Solicitud:**
    ```json
    {
        "username": "new_manager_user"
    }
    ```
*   **Respuesta Exitosa (201 Creado):**
    ```json
    {
        "message": "Usuario agregado al grupo de Gerentes"
    }
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "No autorizado"
    }
    ```
*   **Respuesta de Error (404 No Encontrado):** Si el usuario especificado en el cuerpo de la solicitud no existe.

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

---

##### **Endpoint: `/api/groups/manager/users/{userId}`**

*   **Descripción:** Este endpoint permite a un gerente eliminar un usuario del grupo "Manager".
*   **Método HTTP:** `DELETE`
*   **Permisos:** Solo los usuarios que pertenecen al grupo "Manager" pueden acceder a este endpoint.

**Solicitud DELETE**

*   **Descripción:** Elimina al usuario con el `userId` especificado del grupo "Manager".
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "message": "Usuario eliminado del grupo de Gerentes"
    }
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "No autorizado"
    }
    ```
*   **Respuesta de Error (404 No Encontrado):** Si el usuario con el `userId` especificado no existe.

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

---

#### 3.1.2. Personal de Entrega

##### **Endpoint: `/api/groups/delivery-crew/users/`**

*   **Descripción:** Este endpoint permite a un gerente recuperar una lista de todo el personal de entrega o agregar un usuario al grupo "Delivery crew".
*   **Métodos HTTP:** `GET`, `POST`
*   **Permisos:** Solo los usuarios que pertenecen al grupo "Manager" pueden acceder a este endpoint.

**Solicitud GET**

*   **Descripción:** Recupera una lista de todos los usuarios en el grupo "Delivery crew".
*   **Respuesta Exitosa (200 OK):**
    ```json
    [
        {
            "id": 2,
            "username": "delivery_user",
            "email": "delivery@example.com"
        },
        ...
    ]
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "No autorizado"
    }
    ```

**Solicitud POST**

*   **Descripción:** Agrega un usuario al grupo "Delivery crew".
*   **Cuerpo de la Solicitud:**
    ```json
    {
        "username": "new_delivery_user"
    }
    ```
*   **Respuesta Exitosa (201 Creado):**
    ```json
    {
        "message": "Usuario agregado al grupo de Personal de Entrega"
    }
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "No autorizado"
    }
    ```
*   **Respuesta de Error (404 No Encontrado):** Si el usuario especificado en el cuerpo de la solicitud no existe.

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

---

##### **Endpoint: `/api/groups/delivery-crew/users/{userId}`**

*   **Descripción:** Este endpoint permite a un gerente eliminar un usuario del grupo "Delivery crew".
*   **Método HTTP:** `DELETE`
*   **Permisos:** Solo los usuarios que pertenecen al grupo "Manager" pueden acceder a este endpoint.

**Solicitud DELETE**

*   **Descripción:** Elimina al usuario con el `userId` especificado del grupo "Delivery crew".
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "message": "Usuario eliminado del grupo de Personal de Entrega"
    }
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "No autorizado"
    }
    ```
*   **Respuesta de Error (404 No Encontrado):** Si el usuario con el `userId` especificado no existe.

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

---

### 3.2. Elementos del Menú

##### **Endpoint: `/api/menu-items/`**

*   **Descripción:** Este endpoint permite a cualquier usuario recuperar una lista de elementos del menú. Los gerentes también pueden crear nuevos elementos del menú.
*   **Métodos HTTP:** `GET`, `POST`
*   **Permisos:**
    *   `GET`: Acceso autenticado o de solo lectura.
    *   `POST`: Solo usuarios que pertenecen al grupo "Manager".

**Solicitud GET**

*   **Descripción:** Recupera una lista de todos los elementos del menú. Soporta filtrado, búsqueda y ordenamiento.
*   **Parámetros de Consulta:**
    *   `search`: Búsqueda por título o título de categoría.
    *   `category`: Filtrar por ID de categoría.
    *   `featured`: Filtrar por estado de destacado (`true` o `false`).
    *   `price__gte`: Filtrar por precio mayor or igual al valor especificado.
    *   `price__lte`: Filtrar por precio menor or igual al valor especificado.
    *   `ordering`: Ordenar por `price`, `-price`, `tittle`, `-tittle`, `category`, `-category`, `featured`, `-featured`.
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "tittle": "Bruschetta",
                "price": "10.00",
                "featured": true,
                "category": 1
            }
        ]
    }
    ```

**Solicitud POST**

*   **Descripción:** Crea uno o más elementos nuevos en el menú.
*   **Cuerpo de la Solicitud (un solo elemento):**
    ```json
    {
        "tittle": "Pizza",
        "price": "15.00",
        "featured": false,
        "category": 2
    }
    ```
*   **Cuerpo de la Solicitud (múltiples elementos):**
    ```json
    [
        {
            "tittle": "Pizza",
            "price": "15.00",
            "featured": false,
            "category": 2
        },
        {
            "tittle": "Pasta",
            "price": "12.00",
            "featured": true,
            "category": 2
        }
    ]
    ```
*   **Respuesta Exitosa (201 Creado):**
    ```json
    [
        {
            "id": 2,
            "tittle": "Pizza",
            "price": "15.00",
            "featured": false,
            "category": 2
        }
    ]
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "No autorizado"
    }
    ```

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

---

##### **Endpoint: `/api/menu-items/{pk}/`**

*   **Descripción:** Este endpoint permite a cualquier usuario autenticado recuperar un solo elemento del menú. Los gerentes también pueden actualizar o eliminar un elemento del menú.
*   **Métodos HTTP:** `GET`, `PUT`, `PATCH`, `DELETE`
*   **Permisos:**
    *   `GET`: Usuarios autenticados.
    *   `PUT`, `PATCH`, `DELETE`: Solo usuarios que pertenecen al grupo "Manager".

**Solicitud GET**

*   **Descripción:** Recupera un solo elemento del menú por su ID.
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "id": 1,
        "tittle": "Bruschetta",
        "price": "10.00",
        "featured": true,
        "category": 1
    }
    ```

**Solicitud PUT/PATCH**

*   **Descripción:** Actualiza un elemento del menú. `PUT` requiere todos los campos, mientras que `PATCH` permite actualizaciones parciales.
*   **Cuerpo de la Solicitud:**
    ```json
    {
        "tittle": "Nuevo Título",
        "price": "12.50",
        "featured": true,
        "category": 1
    }
    ```
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "message": "Elemento Actualizado"
    }
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "No autorizado"
    }
    ```

**Solicitud DELETE**

*   **Descripción:** Elimina un elemento del menú.
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "message": "Elemento Eliminado"
    }
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "No autorizado"
    }
    ```

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

---

### 3.3. Gestión del Carrito

##### **Endpoint: `/api/cart/menu-items/`**

*   **Descripción:** Este endpoint permite a un usuario autenticado (cliente) gestionar su carrito de compras.
*   **Métodos HTTP:** `GET`, `POST`, `DELETE`
*   **Permisos:** Solo usuarios autenticados (clientes).

**Solicitud GET**

*   **Descripción:** Recupera los elementos en el carrito de compras del usuario.
*   **Respuesta Exitosa (200 OK):**
    ```json
    [
        {
            "id": 1,
            "menuitem": 1,
            "menuitem_tittle": "Bruschetta",
            "quantity": 2,
            "unit_price": "10.00",
            "price": "20.00"
        }
    ]
    ```

**Solicitud POST**

*   **Descripción:** Agrega un elemento al carrito de compras o actualiza su cantidad si ya existe.
*   **Cuerpo de la Solicitud:**
    ```json
    {
        "menuitem": 1,
        "quantity": 3
    }
    ```
*   **Respuesta Exitosa (200 OK o 201 Creado):**
    ```json
    {
        "id": 1,
        "menuitem": 1,
        "menuitem_tittle": "Bruschetta",
        "quantity": 3,
        "unit_price": "10.00",
        "price": "30.00"
    }
    ```
*   **Respuesta de Error (400 Solicitud Incorrecta):**
    ```json
    {
        "message": "menuitem y quantity son requeridos"
    }
    ```

**Solicitud DELETE**

*   **Descripción:** Elimina todos los elementos del carrito de compras del usuario.
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "message": "Carrito vaciado"
    }
    ```

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

---

### 3.4. Gestión de Pedidos

##### **Endpoint: `/api/orders/`**

*   **Descripción:** Este endpoint permite a los clientes crear nuevos pedidos y ver sus propios pedidos. Los gerentes pueden ver todos los pedidos.
*   **Métodos HTTP:** `GET`, `POST`
*   **Permisos:**
    *   `GET`: Usuarios autenticados. Los gerentes pueden ver todos los pedidos, mientras que los clientes solo pueden ver los suyos.
    *   `POST`: Solo usuarios autenticados (clientes).

**Solicitud GET**

*   **Descripción:** Recupera una lista de pedidos.
*   **Respuesta Exitosa (200 OK):**
    ```json
    [
        {
            "id": 1,
            "user": 1,
            "delivery_crew": null,
            "status": 0,
            "total": "20.00",
            "date": "2025-11-23",
            "items": [
                {
                    "id": 1,
                    "menuitem": 1,
                    "menuitem_tittle": "Bruschetta",
                    "quantity": 2,
                    "unit_price": "10.00",
                    "price": "20.00"
                }
            ]
        }
    ]
    ```

**Solicitud POST**

*   **Descripción:** Crea un nuevo pedido a partir de los elementos en el carrito de compras del usuario. El carrito se vacía después de crear el pedido.
*   **Respuesta Exitosa (201 Creado):**
    ```json
    {
        "id": 2,
        "user": 1,
        "delivery_crew": null,
        "status": 0,
        "total": "30.00",
        "date": "2025-11-23",
        "items": [
            {
                "id": 2,
                "menuitem": 1,
                "menuitem_tittle": "Bruschetta",
                "quantity": 3,
                "unit_price": "10.00",
                "price": "30.00"
            }
        ]
    }
    ```
*   **Respuesta de Error (400 Solicitud Incorrecta):**
    ```json
    {
        "message": "El carrito está vacío"
    }
    ```
*   **Respuesta de Error (403 Prohibido):** Si un gerente o un miembro del personal de entrega intenta crear un pedido.
    ```json
    {
        "message": "Solo los clientes pueden crear pedidos"
    }
    ```

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

---

##### **Endpoint: `/api/orders/{pk}/`**

*   **Descripción:** Este endpoint permite a los usuarios ver, actualizar o eliminar un solo pedido, con permisos basados en su rol.
*   **Métodos HTTP:** `GET`, `PUT`, `PATCH`, `DELETE`
*   **Permisos:**
    *   **Gerente:** Puede `GET`, `PATCH` (personal de entrega y estado), and `DELETE` cualquier pedido.
    *   **Personal de Entrega:** Puede `GET` los pedidos que se le han asignado y `PATCH` el estado de esos pedidos.
    *   **Cliente:** Puede `GET` sus propios pedidos y `PUT` o `PATCH` los elementos dentro de sus pedidos.

**Solicitud GET**

*   **Descripción:** Recupera un solo pedido por su ID.
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "id": 1,
        "user": 1,
        "username": "customer_user",
        "delivery_crew": null,
        "status": 0,
        "total": "20.00",
        "date": "2025-11-23",
        "items": [
            {
                "id": 1,
                "menuitem": 1,
                "menuitem_tittle": "Bruschetta",
                "quantity": 2,
                "unit_price": "10.00",
                "price": "20.00"
            }
        ]
    }
    ```
*   **Respuesta de Error (403 Prohibido):** Si un usuario intenta acceder a un pedido que no le pertenece.

**Solicitud PUT (solo Cliente)**

*   **Descripción:** Actualiza los elementos en un pedido.
*   **Cuerpo de la Solicitud:**
    ```json
    {
        "items": [
            { "menuitem": 1, "quantity": 1 },
            { "menuitem": 2, "quantity": 2 }
        ]
    }
    ```
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "message": "Pedido actualizado exitosamente",
        "items_added": 2,
        "total_updated": "35.00"
    }
    ```

**Solicitud PATCH**

*   **Gerente:** Puede actualizar `delivery_crew` y `status`.
    *   **Cuerpo de la Solicitud:** `{"delivery_crew": 2, "status": 1}`
    *   **Respuesta Exitosa:** `{"message": "Pedido actualizado exitosamente"}`
*   **Personal de Entrega:** Puede actualizar `status`.
    *   **Cuerpo de la Solicitud:** `{"status": 1}`
    *   **Respuesta Exitosa:** `{"message": "El estado del pedido ha sido actualizado exitosamente"}`
*   **Cliente:** Puede actualizar la cantidad de un solo elemento o agregar un nuevo elemento.
    *   **Cuerpo de la Solicitud:** `{"menuitem": 1, "quantity": 5}`
    *   **Respuesta Exitosa:** `{"message": "El elemento Bruschetta ha sido actualizado exitosamente", "total_updated": "50.00"}`

**Solicitud DELETE (solo Gerente)**

*   **Descripción:** Elimina un pedido.
*   **Respuesta Exitosa (200 OK):**
    ```json
    {
        "message": "El pedido ha sido eliminado exitosamente"
    }
    ```

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

---

### 3.5. Gestión de Categorías

##### **Endpoint: `/api/categories/`**

*   **Descripción:** Este endpoint permite a cualquier usuario autenticado recuperar una lista de categorías. Los gerentes también pueden crear nuevas categorías.
*   **Métodos HTTP:** `GET`, `POST`
*   **Permisos:**
    *   `GET`: Usuarios autenticados.
    *   `POST`: Solo usuarios que pertenecen al grupo "Manager".

**Solicitud GET**

*   **Descripción:** Recupera una lista de todas las categorías.
*   **Respuesta Exitosa (200 OK):**
    ```json
    [
        {
            "id": 1,
            "tittle": "Entrantes",
            "slug": "entrantes"
        },
        ...
    ]
    ```

**Solicitud POST**

*   **Descripción:** Crea una nueva categoría.
*   **Cuerpo de la Solicitud:**
    ```json
    {
        "tittle": "Platos Principales",
        "slug": "platos-principales"
    }
    ```
*   **Respuesta Exitosa (201 Creado):**
    ```json
    {
        "id": 2,
        "tittle": "Platos Principales",
        "slug": "platos-principales"
    }
    ```
*   **Respuesta de Error (400 Solicitud Incorrecta):**
    ```json
    {
        "message": "El título es requerido"
    }
    ```
*   **Respuesta de Error (403 Prohibido):**
    ```json
    {
        "message": "Solo los gerentes pueden crear categorías"
    }
    ```

**Captura de Pantalla de las Pruebas:**

*(Espacio para captura de pantalla)*

## 4. Conclusiones

La API de LittleLemon ofrece un conjunto de endpoints robusto y seguro para gestionar las operaciones de un restaurante. El control de acceso basado en roles está bien definido, asegurando que los usuarios solo puedan acceder a los recursos y realizar las acciones apropiadas para su rol.

La API está bien estructurada y sigue los principios de REST. El uso de métodos y códigos de estado HTTP estándar facilita su comprensión e interacción.

La documentación proporciona una visión general completa de la funcionalidad de la API. Sin embargo, es importante tener en cuenta que la API todavía está en desarrollo, y algunas características se implementan de dos maneras diferentes (vistas basadas en funciones y vistas basadas en clases). Esto sugiere un proceso de refactorización en curso, y se recomienda completar este proceso para garantizar la consistencia y la mantenibilidad.

Finalmente, la documentación incluye marcadores de posición para capturas de pantalla de las pruebas. Es crucial realizar pruebas exhaustivas de la API para garantizar su corrección y robustez.
