# IoT Asset Inventory & Vulnerability Intelligence

A security-focused IoT asset management application that combines centralized inventory visibility with on-demand vulnerability analysis using the National Vulnerability Database (NVD).

The application allows users to explore registered IoT devices, identify potential Common Platform Enumeration (CPE) matches, and retrieve associated Common Vulnerabilities and Exposures (CVE) information to support security investigation and asset risk assessment.

## Overview

IoT environments can contain devices from multiple manufacturers, with different models and firmware versions. Maintaining an inventory is only one part of managing this environment; connecting device information to known security vulnerabilities is another.

This project demonstrates an end-to-end workflow for connecting asset inventory data with external vulnerability intelligence. A local SQLite database stores the registered assets, while the NVD API provides CPE candidates and associated CVE information when a user investigates an individual device.

Rather than permanently storing all vulnerability data, the application retrieves security information on demand, keeping inventory management separate from vulnerability enrichment.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Streamlit | Interactive dashboard and user interface |
| SQLite | Local asset inventory database |
| NVD API | External vulnerability intelligence |
| CPE | Device and product identification |
| CVE | Known vulnerability identification |

## Key Features

### 1. Inventory Dashboard

Provides a high-level overview of the IoT asset environment through inventory metrics and interactive visualizations.

- Total registered devices
- Number of represented agencies
- Number of device manufacturers
- Device distribution by agency
- Device distribution by manufacturer

The dashboard makes it easier to understand the composition of the inventory and identify how devices are distributed across agencies and manufacturers.

### 2. Asset Inventory Management

Provides a centralized interface for exploring registered IoT devices.

- Browse the complete asset inventory
- Search for specific devices
- Filter by manufacturer and agency
- Review device details, including manufacturer, model, and firmware version
- Select an individual device for vulnerability analysis

This provides the starting point for investigating an asset without requiring users to work directly with database records.

### 3. CPE Matching

Before vulnerability information can be retrieved, a device must be associated with an appropriate product identifier.

The application uses available device information, including manufacturer, model, and firmware version, to retrieve potential CPE matches from the NVD.

Users can review the candidate matches and select the CPE that most appropriately represents the device being investigated.

This human-in-the-loop approach helps account for differences in product naming and avoids automatically treating the first search result as a definitive match.

### 4. CVE Vulnerability Analysis

After a CPE is selected, the application retrieves associated CVE information from the NVD.

The workflow connects an inventory record to known vulnerability information and presents the results for further investigation.

The goal is to make external security intelligence accessible from the same interface used to manage and explore assets.

**Important distinction:** A retrieved CPE match or associated CVE does not, by itself, confirm that a device is vulnerable. Product versions, configuration, and the applicability of individual vulnerabilities must be considered.

## End-to-End Workflow

The application follows an asset-to-vulnerability enrichment workflow:

```text
┌──────────────────────────┐
│   IoT Asset Inventory    │
│       SQLite Database    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Select an IoT Device   │
│ Manufacturer / Model /   │
│     Firmware Version     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     NVD CPE Search       │
│ Retrieve Candidate CPEs  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   User Reviews and       │
│    Selects a CPE         │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     NVD CVE Lookup       │
│ Retrieve Related CVEs    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Vulnerability Results    │
│ Review and Investigation │
└──────────────────────────┘
```

## Application Architecture

The application separates local inventory data from external security intelligence.

**Inventory layer:** SQLite stores the registered IoT asset records and provides the data used by the dashboard and inventory interface.

**Application layer:** Streamlit provides the interactive interface and coordinates inventory exploration, CPE candidate retrieval, user selection, and vulnerability lookups.

**External intelligence layer:** The NVD API supplies product identification and vulnerability information through CPE and CVE queries.

**Analysis workflow:** The selected CPE connects an inventory device to its associated vulnerability records, allowing users to investigate potential security concerns without manually navigating between separate systems.

## Data Flow

The application follows two related data flows:

**Inventory flow**
1. Read asset records from the local SQLite database.
2. Calculate inventory metrics for the dashboard.
3. Display device records and support search and filtering.

**Vulnerability enrichment flow**
1. Retrieve the selected device's identifying information.
2. Query the NVD for potential CPE matches.
3. Present candidates for user review.
4. Submit the selected CPE for CVE lookup.
5. Display the resulting vulnerability information.

This design keeps the core inventory available locally while allowing vulnerability information to be retrieved when needed.

## Engineering Decisions

### On-Demand Vulnerability Retrieval

Vulnerability information is retrieved when a user initiates an investigation rather than requiring the entire vulnerability dataset to be stored locally. This reduces the need to maintain a separate, continuously synchronized vulnerability database.

### Human-in-the-Loop Product Identification

CPE matching is not always straightforward because device names, manufacturers, product identifiers, and firmware versions may differ across data sources. Allowing users to review candidate matches provides an additional validation step before retrieving CVE records.

### Separation of Inventory and Security Intelligence

The asset inventory and vulnerability enrichment workflow serve different purposes. Keeping them separate makes the application easier to reason about and provides a foundation for extending the analysis workflow independently of the inventory interface.

### Interactive Security Investigation

Using Streamlit allows inventory exploration and vulnerability lookup to take place within a single application, connecting device-level information with external security intelligence through a straightforward user workflow.

## Setup and Installation

### Prerequisites

- Python 3.10 or later, or the version required by the project dependencies
- pip
- An NVD API key if required by your usage and request volume

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment.

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

If the repository includes a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Configure NVD Access

If the application uses an NVD API key, configure it through the application's expected environment variable or Streamlit secrets configuration. Avoid committing API keys or other credentials to the repository.

### 5. Launch the Application

Run Streamlit using the actual entry-point filename in your repository:

```bash
streamlit run app.py
```

Replace `app.py` if your application's entry point has a different name.

## Future Improvements

Potential extensions to the application include:

- CVE severity summaries and CVSS-based filtering
- Device-level vulnerability summaries and prioritization
- Improved CPE matching and product-version validation
- Inventory export and reporting
- Vulnerability lookup caching and API error handling
- Historical vulnerability tracking and change detection
- Authentication and role-based access controls
- Risk prioritization based on severity, exposure, and asset criticality

These improvements would build on the existing inventory and vulnerability enrichment workflow to support more comprehensive security operations.

## Skills Demonstrated

- Python application development
- Interactive dashboard development with Streamlit
- Relational data storage with SQLite
- REST API integration
- IoT asset inventory management
- CPE-based product identification
- CVE vulnerability intelligence retrieval
- Data exploration, filtering, and visualization
- Workflow design and security-focused application development

## Disclaimer

This project is a mock IoT asset inventory developed for demonstration and educational purposes. Vulnerability results depend on the accuracy of product identification and the information returned by the NVD. The application does not independently establish exploitability or confirm that a device is vulnerable.

