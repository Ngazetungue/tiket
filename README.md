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

2. **Event Details Page**

<img width="1231" alt="Screenshot 2025-06-13 at 03 16 08" src="https://github.com/user-attachments/assets/18b443e5-0c6e-4581-91ed-7db86875c0b0" />

   - Click on any event card to see full details
   - View:
     - Event description (with rich text formatting)
     - Date/time with location (map integration)
     - Available ticket types with pricing
     - Organizer information
     - Social sharing buttons


### 2. Buy Tickets

<img width="1231" alt="Screenshot 2025-06-13 at 03 16 43" src="https://github.com/user-attachments/assets/0e6d4eea-9d2b-4f2b-9115-249f8210efa2" />

   - Select from available options (e.g., General Admission, VIP)
   - View price breakdown and any included perks


### 3. Checkout Process

<img width="1231" alt="Screenshot 2025-06-13 at 03 17 13" src="https://github.com/user-attachments/assets/8ab25819-fad3-4280-bee0-f16b15cf805a" />

*Secure checkout flow with ticket selection, attendee details, and payment processing*

# FOR STAFF MEMBER OR ORGANISERS

### 🔐 Authentication Prerequisites
**Before creating events, organizers must:**
1. **Register an Organizer Account**

   <img width="1377" alt="Screenshot 2025-06-13 at 03 15 12" src="https://github.com/user-attachments/assets/c1b4c2d7-e938-4f3c-9f4f-3fc69b04f3b8" />

   - Click "Sign Up" 

3. **Login**

   <img width="1427" alt="Screenshot 2025-06-13 at 03 13 18" src="https://github.com/user-attachments/assets/a7bf532c-8369-4643-a63d-4c5e4b528762" />

   - Use credentialed login (username/password)

### 🎪 Event Creation Flow (Post-Authentication)
```mermaid
graph LR
    A[Organizer Login] --> B[Dashboard]
    B --> C[New Event Button]
    C --> D[Event Creation Wizard]
    D --> E[Publish]
```

**Key Restrictions:**
- ❌ Unauthenticated users see disabled "Create Event" buttons
- ⚠️ Attempting to access `/create-event` redirects to login


### 4. User Dashboard

<img width="1427" alt="Screenshot 2025-06-13 at 03 13 57" src="https://github.com/user-attachments/assets/4ffbacb8-26a2-42ff-81bd-0c70fd644c81" />

*Personalized dashboard showing upcoming events, past purchases, and saved events*

### 2. Event Creation

<img width="1427" alt="Screenshot 2025-06-13 at 03 14 16" src="https://github.com/user-attachments/assets/42296541-4ef6-4cdc-bb99-0da6fa9b050b" />

*Multi-step form for organizers to create events with ticket options, dates, and rich descriptions*


### 5. Event and Ticket Page listing

<img width="1377" alt="Screenshot 2025-06-13 at 03 14 37" src="https://github.com/user-attachments/assets/f32c8b17-d2ea-4dc2-8114-a1ef40979c2f" />

*Comprehensive event view with description, ticket options, and interactive map*

## Installation

### Prerequisites
- Python 3.10+
