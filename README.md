# TicketA - Event Ticketing Platform

![TicketA Screenshot](https://via.placeholder.com/1200x600?text=TicketA+Platform+Showcase)

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

Ticketa is a full-featured event management and ticketing platform built with Django that enables:
- **Event organizers** to create, manage, and promote events
- **Attendees** to discover, purchase tickets for, and save events
- **Administrators** to oversee platform operations

The platform combines the robustness of Django's backend with the modern interactivity of Alpine.js and the sleek design of Tailwind CSS.

## Key Features

### 🎟️ Core Functionality
- User authentication system (registration, login, password reset)
- Event creation wizard with rich text editing
- Ticket type configuration (general admission, VIP, early bird)
- Secure checkout process with payment integration
- Digital ticket generation and management

### 🛠️ Admin Features
- Comprehensive dashboard for event organizers
- Real-time attendance tracking
- Sales analytics and reporting
- Bulk attendee management tools

### ✨ User Experience
- Responsive design for all devices
- Interactive event browsing with filters
- Personalized event recommendations
- Social sharing capabilities

## Technology Stack

### Backend
- **Django 4.2** - Full-stack web framework
- **PostgreSQL** - Relational database

### Frontend
- **Tailwind CSS 3.3** - Utility-first CSS framework
- **Alpine.js 3.12** - Lightweight JavaScript framework
- **HTMX** - Dynamic content loading

### Services
- **Stripe** - Payment processing

## Screenshots

### 1. Landing Page

<img width="1427" alt="Screenshot 2025-06-13 at 03 11 40" src="https://github.com/user-attachments/assets/803e5e98-2449-4f55-8cd5-846ee5e1e317" />

<img width="1427" alt="Screenshot 2025-06-13 at 03 12 14" src="https://github.com/user-attachments/assets/e4e6cb7a-cc05-457b-a1df-9168603fc151" />


<img width="1427" alt="Screenshot 2025-06-13 at 03 12 48" src="https://github.com/user-attachments/assets/69e0ef45-25fe-4563-bd90-5c4067444bc8" />


*Clean, modern homepage showcasing featured events with search functionality*

### 2. Event Creation

<img width="1427" alt="Screenshot 2025-06-13 at 03 14 16" src="https://github.com/user-attachments/assets/42296541-4ef6-4cdc-bb99-0da6fa9b050b" />

*Multi-step form for organizers to create events with ticket options, dates, and rich descriptions*

### 3. Checkout Process
![Checkout Flow](https://via.placeholder.com/800x450?text=Ticket+Checkout+Process)
*Secure checkout flow with ticket selection, attendee details, and payment processing*

### 4. User Dashboard

<img width="1427" alt="Screenshot 2025-06-13 at 03 13 57" src="https://github.com/user-attachments/assets/4ffbacb8-26a2-42ff-81bd-0c70fd644c81" />

*Personalized dashboard showing upcoming events, past purchases, and saved events*

### 5. Event and Ticket Page listing

<img width="1377" alt="Screenshot 2025-06-13 at 03 14 37" src="https://github.com/user-attachments/assets/f32c8b17-d2ea-4dc2-8114-a1ef40979c2f" />

*Comprehensive event view with description, ticket options, and interactive map*

## Installation

### Prerequisites
- Python 3.10+
