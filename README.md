
# **Ticketa - Event Ticketing Platform**  


## **Project Overview**  
**Ticketa.** is a full-featured event management and ticketing platform built with **Django**, designed to empower:  
- **Event organizers** to create, manage, and promote events.  
- **Attendees** to discover, purchase tickets, and save events.  
- **Administrators** to oversee platform operations.  

The platform combines **Django’s backend robustness** with the modern interactivity of **Alpine.js** and the sleek design of **Tailwind CSS**.  

## **Key Features**  

### **🎟️ Core Functionality**  
- **User authentication system** (registration, login, password reset).  
- **Event creation wizard** with rich text editing.  
- **Ticket type configuration** (general admission, VIP, early bird).  
- **Secure checkout process** with payment integration.  
- **Digital ticket generation and management**.  

### **Admin Features**  
- **Comprehensive dashboard** for event organizers.  
- **Sales analytics and reporting**.  

### **User Experience**  
- **Responsive design** for all devices.  
- **Interactive event browsing** with filters.  

## **Technology Stack**  

### **Backend**  
| Technology | Description | Why It Was Chosen |
|------------|-------------|-------------------|
| **<img src="https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white" alt="Django" />** | High-level Python web framework. | Provides **built-in security** (CSRF, SQL injection protection), **scalability**, and a **batteries-included** approach (admin panel, ORM, auth). Ideal for rapid development of complex platforms like TicketA. |
| **<img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL" />** | Relational database system. | Chosen for **ACID compliance**, **performance** with large datasets (e.g., event/ticket records), and **Django’s native support**. Supports JSON fields for flexible event metadata. |

### **Frontend**  
| Technology | Description | Why It Was Chosen |
|------------|-------------|-------------------|
| **<img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />** | Utility-first CSS framework. | Enables **rapid UI development** with responsive design out-of-the-box. Eliminates context-switching between HTML/CSS, perfect for dynamic interfaces like event dashboards. |
| **<img src="https://img.shields.io/badge/Alpine.js-8BC0D0?logo=alpine.js&logoColor=black" alt="Alpine.js" />** | Lightweight JavaScript framework. | Provides **reactivity** (e.g., dynamic ticket counters) without the overhead of heavier frameworks like React. Integrates seamlessly with Django templates. |
| **<img src="https://img.shields.io/badge/HTMX-1E4A75?logo=html5&logoColor=white" alt="HTMX" />** | Library for dynamic HTML. | Allows **AJAX-like behavior** (e.g., filtering events, cart updates) without writing JavaScript. Reduces frontend complexity while maintaining interactivity. |

### **Services**  
| Technology | Description | Why It Was Chosen |
|------------|-------------|-------------------|
| **<img src="https://img.shields.io/badge/Stripe-008CDD?logo=stripe&logoColor=white" alt="Stripe" />** | Payment processing API. | Industry-standard for **secure transactions**, supports **global payments**, and handles PCI compliance. Django’s Stripe library simplifies integration. |


## **Project Screenshots**  

### **1. Landing Page**  
<img width="1427" alt="Landing Page" src="https://github.com/user-attachments/assets/803e5e98-2449-4f55-8cd5-846ee5e1e317" />  
<img width="1427" alt="Landing Page" src="https://github.com/user-attachments/assets/e4e6cb7a-cc05-457b-a1df-9168603fc151" />  
<img width="1427" alt="Landing Page" src="https://github.com/user-attachments/assets/69e0ef45-25fe-4563-bd90-5c4067444bc8" />  
*Clean, modern homepage showcasing featured events with search functionality.*  

### **2. Event Details Page**  
<img width="1231" alt="Event Details" src="https://github.com/user-attachments/assets/18b443e5-0c6e-4581-91ed-7db86875c0b0" />  

- Click on any event card to see full details.  
- View:  
  - Event description (with rich text formatting).  
  - Date/time with location (map integration).  
  - Available ticket types with pricing.  
  - Organizer information.  

### **3. Buy Tickets**  
<img width="1231" alt="Buy Tickets" src="https://github.com/user-attachments/assets/0e6d4eea-9d2b-4f2b-9115-249f8210efa2" />  
- Select from available options (e.g., General Admission, VIP).  
- View price breakdown and any included perks.  

### **4. Checkout Process**  
<img width="1231" alt="Checkout" src="https://github.com/user-attachments/assets/8ab25819-fad3-4280-bee0-f16b15cf805a" />  
*Secure checkout flow with ticket selection, attendee details, and payment processing.*  

## **For Staff Members or Organizers**  

### **🔐 Authentication Prerequisites**  
**Before creating events, organizers must:**  
1. **Register an Organizer Account**  
   <img width="1377" alt="Registration" src="https://github.com/user-attachments/assets/c1b4c2d7-e938-4f3c-9f4f-3fc69b04f3b8" />  
   - Click **"Register"**.  

2. **Login**  
   <img width="1427" alt="Login" src="https://github.com/user-attachments/assets/a7bf532c-8369-4643-a63d-4c5e4b528762" />  
   - Use credentialed login (username/password).  

### **🎪 Event Creation Flow (Post-Authentication)**  
```mermaid  
graph LR  
    A[Organizer Login] --> B[Dashboard]  
    B --> C[New Event Button]  
    C --> D[Event Creation Wizard]  
    D --> E[Publish]  
```  
**Key Restrictions:**  
- ⚠️ Attempting to access `/create-event` redirects to login.  


### **3. User Dashboard**  
<img width="1427" alt="User Dashboard" src="https://github.com/user-attachments/assets/4ffbacb8-26a2-42ff-81bd-0c70fd644c81" />  
Personalized dashboard showing upcoming events, past purchases, and saved events. 

### **4. Event Creation**  
<img width="1427" alt="Event Creation" src="https://github.com/user-attachments/assets/42296541-4ef6-4cdc-bb99-0da6fa9b050b" />  
Multi-step form for organizers to create events with ticket options, dates, and rich descriptions.  

### **5. Event and Ticket Listing**  
<img width="1377" alt="Event Listing" src="https://github.com/user-attachments/assets/f32c8b17-d2ea-4dc2-8114-a1ef40979c2f" />  
Comprehensive event view with description, ticket options. 


## **Installation**  
### **Prerequisites**  
- Python 3.10+  
