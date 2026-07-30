# KitchenOS Database Schema

## Overview

KitchenOS uses Django ORM with SQLite as the database backend. The database is designed to manage cloud kitchen operations including kitchens, menu items, inventory, orders, and third-party integrations.

---

# Entity Relationship Overview

```
Kitchen
   │
   ├──────────────┐
   │              │
   ▼              ▼
MenuItem      Inventory

Order

Integration
```

---

# Kitchen

Stores information about each cloud kitchen.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField | Kitchen name |
| location | CharField | Kitchen location |
| manager | CharField | Kitchen manager |
| capacity | IntegerField | Daily production capacity |
| status | CharField | Operational status |

### Purpose

The Kitchen model acts as the central entity for managing multiple cloud kitchen locations.

---

# MenuItem

Stores menu information available for customers.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField | Menu item name |
| category | CharField | Food category |
| price | DecimalField | Selling price |
| available | BooleanField | Availability status |

### Purpose

Allows administrators to manage available food items, pricing, and categories.

---

# Inventory

Tracks ingredient inventory.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| ingredient | CharField | Ingredient name |
| quantity | IntegerField | Current stock |
| unit | CharField | Unit of measurement |
| reorder_level | IntegerField | Minimum stock level |

### Purpose

Helps monitor inventory levels and identify low-stock ingredients.

---

# Order

Stores customer order information.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| customer_name | CharField | Customer name |
| menu_item | CharField | Ordered item |
| quantity | IntegerField | Quantity ordered |
| total_amount | DecimalField | Total order value |
| status | CharField | Order status |

### Purpose

Tracks the lifecycle of customer orders from placement through completion.

---

# Integration

Stores third-party platform integration status.

| Field | Type | Description |
|-------|------|-------------|
| id | AutoField | Primary Key |
| name | CharField | Integration name |
| provider | CharField | Service provider |
| category | CharField | Integration category |
| description | TextField | Description |
| connected | BooleanField | Connection status |
| updated_at | DateTimeField | Last updated timestamp |

### Purpose

Allows administrators to enable or disable external service integrations and track their current connection status.

---

# Relationships

Current application relationships:

```
Kitchen
   │
   ├──── Menu Items
   │
   └──── Inventory
```

The remaining entities operate independently within the current version of the application and are managed through their respective modules.

---

# Data Access Layer

KitchenOS uses Django ORM for all database operations.

Typical workflow:

```
View
   │
   ▼
Model
   │
   ▼
Django ORM
   │
   ▼
SQLite Database
```

Benefits include:

- Database abstraction
- SQL injection protection
- Simplified CRUD operations
- Migration management

---

# Database Migrations

Schema changes are managed using Django migrations.

Common commands:

```bash
python manage.py makemigrations
python manage.py migrate
```

Current migrations include:

- 0001_initial
- 0002_integration

---

# Future Database Enhancements

Potential improvements include:

- PostgreSQL migration
- Foreign key relationships between orders and menu items
- Customer entity
- Supplier management
- Audit logs
- Payment transaction records
- Multi-location inventory support
- User and role management

