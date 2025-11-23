[LittleLemon_API_Documentation.md](https://github.com/user-attachments/files/23697963/LittleLemon_API_Documentation.md)
# Documentation of the LittleLemon API

## 1. Objectives

### 1.1. Main Objective

To provide a comprehensive documentation of the LittleLemon API, detailing its endpoints, functionalities, and usage, to facilitate its use and maintenance.

### 1.2. Secondary Objectives

*   To document each of the API's endpoints, including its URL, the HTTP methods it supports, the expected request format, and the possible responses.
*   To describe the different user roles and their permissions within the API.
*   To provide a clear and concise guide for testing the API and its endpoints.

## 2. Introduction

The LittleLemon API is a web service designed to manage a restaurant's operations. It provides functionalities for managing users, menu items, categories, shopping carts, and orders. The API is built with Django and Django REST Framework, and it uses token-based authentication for security.

This document provides a detailed description of the API's endpoints and their usage. It is intended for developers who need to interact with the API, as well as for those responsible for its maintenance and future development.

## 3. Development (API Documentation)

This section details each of the API's endpoints.

### 3.1. User Management

#### 3.1.1. Managers

##### **Endpoint: `/api/groups/manager/users/`**

*   **Description:** This endpoint allows a manager to retrieve a list of all managers or to add a user to the "Manager" group.
*   **HTTP Methods:** `GET`, `POST`
*   **Permissions:** Only users belonging to the "Manager" group can access this endpoint.

**GET Request**

*   **Description:** Retrieves a list of all users in the "Manager" group.
*   **Success Response (200 OK):**
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
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Unautorized"
    }
    ```

**POST Request**

*   **Description:** Adds a user to the "Manager" group.
*   **Request Body:**
    ```json
    {
        "username": "new_manager_user"
    }
    ```
*   **Success Response (201 Created):**
    ```json
    {
        "message": "User Added to Manager group"
    }
    ```
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Unautorized"
    }
    ```
*   **Error Response (404 Not Found):** If the user specified in the request body does not exist.

**Tests Screenshot:**

*(Space for screenshot)*

---

##### **Endpoint: `/api/groups/manager/users/{userId}`**

*   **Description:** This endpoint allows a manager to remove a user from the "Manager" group.
*   **HTTP Method:** `DELETE`
*   **Permissions:** Only users belonging to the "Manager" group can access this endpoint.

**DELETE Request**

*   **Description:** Removes the user with the specified `userId` from the "Manager" group.
*   **Success Response (200 OK):**
    ```json
    {
        "message": "User removed from Managers Group"
    }
    ```
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Unautorized"
    }
    ```
*   **Error Response (404 Not Found):** If the user with the specified `userId` does not exist.

**Tests Screenshot:**

*(Space for screenshot)*

---

#### 3.1.2. Delivery Crew

##### **Endpoint: `/api/groups/delivery-crew/users/`**

*   **Description:** This endpoint allows a manager to retrieve a list of all delivery crew members or to add a user to the "Delivery crew" group.
*   **HTTP Methods:** `GET`, `POST`
*   **Permissions:** Only users belonging to the "Manager" group can access this endpoint.

**GET Request**

*   **Description:** Retrieves a list of all users in the "Delivery crew" group.
*   **Success Response (200 OK):**
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
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Unautorized"
    }
    ```

**POST Request**

*   **Description:** Adds a user to the "Delivery crew" group.
*   **Request Body:**
    ```json
    {
        "username": "new_delivery_user"
    }
    ```
*   **Success Response (201 Created):**
    ```json
    {
        "message": "User Added to Delivery crew group"
    }
    ```
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Unautorized"
    }
    ```
*   **Error Response (404 Not Found):** If the user specified in the request body does not exist.

**Tests Screenshot:**

*(Space for screenshot)*

---

##### **Endpoint: `/api/groups/delivery-crew/users/{userId}`**

*   **Description:** This endpoint allows a manager to remove a user from the "Delivery crew" group.
*   **HTTP Method:** `DELETE`
*   **Permissions:** Only users belonging to the "Manager" group can access this endpoint.

**DELETE Request**

*   **Description:** Removes the user with the specified `userId` from the "Delivery crew" group.
*   **Success Response (200 OK):**
    ```json
    {
        "message": "User removed from Delivery crew Group"
    }
    ```
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Unautorized"
    }
    ```
*   **Error Response (404 Not Found):** If the user with the specified `userId` does not exist.

**Tests Screenshot:**

*(Space for screenshot)*

---

### 3.2. Menu Items

##### **Endpoint: `/api/menu-items/`**

*   **Description:** This endpoint allows any user to retrieve a list of menu items. Managers can also create new menu items.
*   **HTTP Methods:** `GET`, `POST`
*   **Permissions:**
    *   `GET`: Authenticated or read-only access.
    *   `POST`: Only users belonging to the "Manager" group.

**GET Request**

*   **Description:** Retrieves a list of all menu items. It supports filtering, searching, and ordering.
*   **Query Parameters:**
    *   `search`: Search by title or category title.
    *   `category`: Filter by category ID.
    *   `featured`: Filter by featured status (`true` or `false`).
    *   `price__gte`: Filter by price greater than or equal to the specified value.
    *   `price__lte`: Filter by price less than or equal to the specified value.
    *   `ordering`: Order by `price`, `-price`, `tittle`, `-tittle`, `category`, `-category`, `featured`, `-featured`.
*   **Success Response (200 OK):**
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

**POST Request**

*   **Description:** Creates one or more new menu items.
*   **Request Body (single item):**
    ```json
    {
        "tittle": "Pizza",
        "price": "15.00",
        "featured": false,
        "category": 2
    }
    ```
*   **Request Body (multiple items):**
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
*   **Success Response (201 Created):**
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
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Unautorized"
    }
    ```

**Tests Screenshot:**

*(Space for screenshot)*

---

##### **Endpoint: `/api/menu-items/{pk}/`**

*   **Description:** This endpoint allows any authenticated user to retrieve a single menu item. Managers can also update or delete a menu item.
*   **HTTP Methods:** `GET`, `PUT`, `PATCH`, `DELETE`
*   **Permissions:**
    *   `GET`: Authenticated users.
    *   `PUT`, `PATCH`, `DELETE`: Only users belonging to the "Manager" group.

**GET Request**

*   **Description:** Retrieves a single menu item by its ID.
*   **Success Response (200 OK):**
    ```json
    {
        "id": 1,
        "tittle": "Bruschetta",
        "price": "10.00",
        "featured": true,
        "category": 1
    }
    ```

**PUT/PATCH Request**

*   **Description:** Updates a menu item. `PUT` requires all fields, while `PATCH` allows partial updates.
*   **Request Body:**
    ```json
    {
        "tittle": "New Tittle",
        "price": "12.50",
        "featured": true,
        "category": 1
    }
    ```
*   **Success Response (200 OK):**
    ```json
    {
        "message": "Item Updated"
    }
    ```
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Unautorized"
    }
    ```

**DELETE Request**

*   **Description:** Deletes a menu item.
*   **Success Response (200 OK):**
    ```json
    {
        "message": "Item Deleted"
    }
    ```
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Unautorized"
    }
    ```

**Tests Screenshot:**

*(Space for screenshot)*

---

### 3.3. Cart Management

##### **Endpoint: `/api/cart/menu-items/`**

*   **Description:** This endpoint allows an authenticated user (customer) to manage their shopping cart.
*   **HTTP Methods:** `GET`, `POST`, `DELETE`
*   **Permissions:** Only authenticated users (customers).

**GET Request**

*   **Description:** Retrieves the items in the user's shopping cart.
*   **Success Response (200 OK):**
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

**POST Request**

*   **Description:** Adds an item to the shopping cart or updates its quantity if it already exists.
*   **Request Body:**
    ```json
    {
        "menuitem": 1,
        "quantity": 3
    }
    ```
*   **Success Response (200 OK or 201 Created):**
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
*   **Error Response (400 Bad Request):**
    ```json
    {
        "message": "menuitem and quantity are required"
    }
    ```

**DELETE Request**

*   **Description:** Clears all items from the user's shopping cart.
*   **Success Response (200 OK):**
    ```json
    {
        "message": "Cart cleared"
    }
    ```

**Tests Screenshot:**

*(Space for screenshot)*

---

### 3.4. Order Management

##### **Endpoint: `/api/orders/`**

*   **Description:** This endpoint allows customers to create new orders and view their own orders. Managers can view all orders.
*   **HTTP Methods:** `GET`, `POST`
*   **Permissions:**
    *   `GET`: Authenticated users. Managers can see all orders, while customers can only see their own.
    *   `POST`: Only authenticated users (customers).

**GET Request**

*   **Description:** Retrieves a list of orders.
*   **Success Response (200 OK):**
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

**POST Request**

*   **Description:** Creates a new order from the items in the user's shopping cart. The cart is cleared after the order is created.
*   **Success Response (201 Created):**
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
*   **Error Response (400 Bad Request):**
    ```json
    {
        "message": "Cart is empty"
    }
    ```
*   **Error Response (403 Forbidden):** If a manager or delivery crew member tries to create an order.
    ```json
    {
        "message": "Only customer can create orders"
    }
    ```

**Tests Screenshot:**

*(Space for screenshot)*

---

##### **Endpoint: `/api/orders/{pk}/`**

*   **Description:** This endpoint allows users to view, update, or delete a single order, with permissions based on their role.
*   **HTTP Methods:** `GET`, `PUT`, `PATCH`, `DELETE`
*   **Permissions:**
    *   **Manager:** Can `GET`, `PATCH` (delivery crew and status), and `DELETE` any order.
    *   **Delivery Crew:** Can `GET` orders assigned to them and `PATCH` the status of those orders.
    *   **Customer:** Can `GET` their own orders and `PUT` or `PATCH` the items within their orders.

**GET Request**

*   **Description:** Retrieves a single order by its ID.
*   **Success Response (200 OK):**
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
*   **Error Response (403 Forbidden):** If a user tries to access an order that does not belong to them.

**PUT Request (Customer only)**

*   **Description:** Updates the items in an order.
*   **Request Body:**
    ```json
    {
        "items": [
            { "menuitem": 1, "quantity": 1 },
            { "menuitem": 2, "quantity": 2 }
        ]
    }
    ```
*   **Success Response (200 OK):**
    ```json
    {
        "message": "Order update successfully",
        "items_added": 2,
        "total_updated": "35.00"
    }
    ```

**PATCH Request**

*   **Manager:** Can update `delivery_crew` and `status`.
    *   **Request Body:** `{"delivery_crew": 2, "status": 1}`
    *   **Success Response:** `{"message": "Order updated successfully"}`
*   **Delivery Crew:** Can update `status`.
    *   **Request Body:** `{"status": 1}`
    *   **Success Response:** `{"message": "Order status has been updated successfully"}`
*   **Customer:** Can update the quantity of a single item or add a new item.
    *   **Request Body:** `{"menuitem": 1, "quantity": 5}`
    *   **Success Response:** `{"message": "Item Bruschetta has been updated successfully", "total_updated": "50.00"}`

**DELETE Request (Manager only)**

*   **Description:** Deletes an order.
*   **Success Response (200 OK):**
    ```json
    {
        "message": "The order has been deleted successfully"
    }
    ```

**Tests Screenshot:**

*(Space for screenshot)*

---

### 3.5. Category Management

##### **Endpoint: `/api/categories/`**

*   **Description:** This endpoint allows any authenticated user to retrieve a list of categories. Managers can also create new categories.
*   **HTTP Methods:** `GET`, `POST`
*   **Permissions:**
    *   `GET`: Authenticated users.
    *   `POST`: Only users belonging to the "Manager" group.

**GET Request**

*   **Description:** Retrieves a list of all categories.
*   **Success Response (200 OK):**
    ```json
    [
        {
            "id": 1,
            "tittle": "Starters",
            "slug": "starters"
        },
        ...
    ]
    ```

**POST Request**

*   **Description:** Creates a new category.
*   **Request Body:**
    ```json
    {
        "tittle": "Main Courses",
        "slug": "main-courses"
    }
    ```
*   **Success Response (201 Created):**
    ```json
    {
        "id": 2,
        "tittle": "Main Courses",
        "slug": "main-courses"
    }
    ```
*   **Error Response (400 Bad Request):**
    ```json
    {
        "message": "Tittle is required"
    }
    ```
*   **Error Response (403 Forbidden):**
    ```json
    {
        "message": "Only managers can create categories"
    }
    ```

**Tests Screenshot:**

*(Space for screenshot)*

## 4. Conclusions

The LittleLemon API offers a robust and secure set of endpoints for managing a restaurant's operations. The role-based access control is well-defined, ensuring that users can only access the resources and perform the actions that are appropriate for their role.

The API is well-structured and follows the principles of REST. The use of standard HTTP methods and status codes makes it easy to understand and interact with.

The documentation provides a comprehensive overview of the API's functionality. However, it is important to note that the API is still under development, and some features are implemented in two different ways (function-based and class-based views). This suggests an ongoing refactoring process, and it is recommended to complete this process to ensure consistency and maintainability.

Finally, the documentation includes placeholders for test screenshots. It is crucial to perform thorough testing of the API to ensure its correctness and robustness.
