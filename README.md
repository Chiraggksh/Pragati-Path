# प्रगतिpath (PragatiPath)

**प्रगतिpath** is an AI-powered, crowdsourced Civic Issue Reporting and Resolution System designed to bridge the gap between citizens and civic authorities.  
Unlike traditional complaint platforms that stop at issue registration, PragatiPath enables **end-to-end automation**, **intelligent prioritization**, **proof-based resolution**, and **data-driven governance** at scale.

The platform follows an **AI-first, citizen-centric architecture** to make civic governance faster, more transparent, and participatory.

---

## 🚩 Problem Statement

Existing civic platforms (e.g., CitySourced, Swachhata App, Citizen Matters):
- Primarily focus on complaint registration
- Lack intelligent prioritization and automation
- Provide limited transparency in resolution
- Do not scale well across multiple civic domains

As a result, issues remain unresolved, duplicated complaints flood systems, and accountability is weak.

---

## 💡 Solution Overview

PragatiPath solves these challenges by combining **AI, computer vision, NLP, geospatial intelligence, and automation** to create a unified civic governance platform.

Key highlights:
- Intelligent issue understanding (text + image)
- Severity-based prioritization
- Automated department routing
- Proof-based resolution verification
- Predictive analytics for proactive governance

---

## 🔁 End-to-End Workflow

### 1️⃣ Citizen Complaint Registration
- Multiple input modes:
  - Web portal
  - WhatsApp integration
  - AI chatbot
  - Voice-to-text support for low-literacy users
- Automatic location extraction from **non-geo-tagged images** using metadata and contextual analysis

---

### 2️⃣ AI-Powered Issue Understanding
- **LLM-based Issue Detection**
  - Classifies complaints into categories such as:
    - Potholes
    - Garbage
    - Waterlogging
    - Streetlights
    - Encroachment
- **Severity Scoring**
  - Deep learning models assign urgency scores  
  - Example: open manhole > pothole crack > graffiti
- **Redundancy & Duplication Detection**
  - NLP similarity (transformers)
  - Geospatial clustering to merge duplicate complaints in the same locality

---

### 3️⃣ Smart Routing & Alerts
- Automatic routing to:
  - Relevant civic departments
  - Contractors
  - NGOs (based on jurisdiction mapping)
- Real-time alerts:
  - WhatsApp notifications to officials
  - Status updates to citizens

---

### 4️⃣ Resolution Tracking & Proof Verification
- Departments upload **post-resolution images**
- Computer vision verifies:
  - Before vs after images
  - Timestamp consistency
  - Geolocation authenticity
- **Predictive Analytics**
  - Identifies recurring issue hotspots
  - Enables proactive intervention before escalation

---

### 5️⃣ Community & NGO Outsourcing
- Non-critical issues routed to:
  - NGOs
  - Local community groups
- Gamification:
  - Leaderboards
  - Rewards for active volunteers

---

### 6️⃣ Pragati-Bot 🤖
- Multi-lingual AI chatbot
- Features:
  - Track complaint status using User ID
  - View deadlines and resolution progress
  - Submit structured feedback
- Feedback data is stored as backend variables and used to **improve system decisions and UX**

---

### 7️⃣ Two-Way Transparency
- **Citizen Portal**
  - Complaint status
  - Resolution timelines
  - Before/after photos
  - Department remarks
- **Department Portal**
  - Analytics dashboard
  - Pending issues
  - SLA breach tracking
  - Hotspot analysis
  - Citizen satisfaction index

---

## 🧠 AI & ML Architecture

### 🔍 Issue Detection
- Fine-tuned **LLaMA-2 / GPT-based models**
- Multimodal input (text + image)

### 🔁 Redundancy Detection
- Transformer-based similarity models (RoBERTa)

### ⚠️ Severity Scoring
- CNN-based image classification
- ResNet architectures for visual severity assessment

### 📸 Proof Verification
- Siamese Neural Networks
- Before–after image comparison for fake closure prevention

---

## 🛠️ Tech Stack

### Frontend (Citizen & Department Portals)
- HTML, CSS, JavaScript
- Bootstrap, Tailwind CSS, Material UI
- Leaflet.js (Map Integration)

### Backend
- Flask (Python)
- PostgreSQL (structured complaint data)
- MongoDB (chatbot conversations, logs)

### Chatbot & Integrations
- Omnidim.io (Chatbot)
- Twilio API (WhatsApp / SMS notifications)

---

## 🌟 Key Differentiators (USP)

- AI-first civic governance platform
- Automatic location extraction from normal photos
- LLM-powered validation and classification
- Multi-lingual chatbot for inclusive access
- Proof-based governance via image verification
- Predictive analytics for hotspot detection
- Scalable across **all civic issue categories**, not limited to sanitation

---

## 🚀 Impact

PragatiPath enables:
- Faster issue resolution
- Reduced corruption and fake closures
- Data-driven civic planning
- Stronger citizen participation
- Transparent and accountable governance

---

## 📌 Future Scope
- Integration with state-level and national civic systems
- IoT sensor-based issue detection
- Public APIs for NGOs and third-party audits
- Advanced reinforcement learning for routing optimization

---

## 👥 Team & Ownership
This project was developed as part of **Smart India Hackathon (SIH)** with a focus on scalable, real-world civic impact.

