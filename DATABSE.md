# Corrected Database Schema — E-Commerce System

This document outlines the corrected relational database schema. 
*   **Decimal Types:** All monetary fields (price, total, subtotal) MUST use `Decimal` (Django: `DecimalField`) to avoid floating-point errors.
*   **Foreign Keys:** All relationships are explicitly defined with FK constraints.

---

## Entities & Structure

### 1. Kliente (Client)
| Column | Type | Constraints |
| :--- | :--- | :--- |
| id | Integer | PK |
| name | String | NOT NULL |
| email | String | NOT NULL, UNIQUE |
| password | String | NOT NULL |

### 2. Kategoria (Category)
| Column | Type | Constraints |
| :--- | :--- | :--- |
| id | Integer | PK |
| name | String | NOT NULL |
| description | Text | |

### 3. Produtu (Product)
| Column | Type | Constraints |
| :--- | :--- | :--- |
| id | Integer | PK |
| name | String | NOT NULL |
| description | Text | |
| price | Decimal | NOT NULL |
| stock | Integer | NOT NULL |
| kategoria_id | Integer | FK -> Kategoria(id), NOT NULL |

### 4. Pedidu (Order)
| Column | Type | Constraints |
| :--- | :--- | :--- |
| id | Integer | PK |
| status | String | NOT NULL |
| total | Decimal | NOT NULL |
| created_at | DateTime | NOT NULL |
| kliente_id | Integer | FK -> Kliente(id), NOT NULL |

### 5. DetalloPedidu (Order Detail)
| Column | Type | Constraints |
| :--- | :--- | :--- |
| id | Integer | PK |
| quantity | Integer | NOT NULL |
| subtotal | Decimal | NOT NULL |
| pedidu_id | Integer | FK -> Pedidu(id), NOT NULL |
| produtu_id | Integer | FK -> Produtu(id), NOT NULL |

### 6. Pagamentu (Payment)
| Column | Type | Constraints |
| :--- | :--- | :--- |
| id | Integer | PK |
| method | String | NOT NULL |
| total | Decimal | NOT NULL |
| status | String | NOT NULL |
| created_at | DateTime | NOT NULL |
| pedidu_id | Integer | FK -> Pedidu(id), UNIQUE, NOT NULL |

### 7. Notifikasaun (Notification)
| Column | Type | Constraints |
| :--- | :--- | :--- |
| id | Integer | PK |
| message | Text | NOT NULL |
| type | String | NOT NULL |
| created_at | DateTime | NOT NULL |
| kliente_id | Integer | FK -> Kliente(id), NOT NULL |
| pedidu_id | Integer | FK -> Pedidu(id), NULLABLE |

---

## Relationship Summary
*   **Kliente** 1:N **Pedidu**
*   **Kliente** 1:N **Notifikasaun**
*   **Kategoria** 1:N **Produtu**
*   **Produtu** 1:N **DetalloPedidu**
*   **Pedidu** 1:N **DetalloPedidu**
*   **Pedidu** 1:1 **Pagamentu**
*   **Pedidu** 1:N **Notifikasaun**
