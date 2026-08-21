# IoT Asset Inventory

## Overview

The NYC OTI IoT Asset Inventory is a Streamlit-based application designed to provide a centralized view of Internet of Things (IoT) assets and support the investigation of potential security vulnerabilities.

The application combines inventory management with on-demand vulnerability analysis. Asset information is maintained in a local SQLite database, while Common Platform Enumeration (CPE) and Common Vulnerabilities and Exposures (CVE) information can be retrieved dynamically from the National Vulnerability Database (NVD).

The application is designed to support the following workflow:

1. Review and explore the IoT asset inventory.
2. Select an individual device.
3. Retrieve potential CPE matches based on the device's manufacturer, model, and firmware version.
4. Allow the user to select the most appropriate CPE.
5. Retrieve and display CVE information associated with the selected CPE.

This approach separates inventory management from vulnerability enrichment and allows security data to be retrieved when needed rather than requiring all vulnerability information to be permanently stored in the local database.

## Key Features

### Inventory Dashboard

The dashboard provides a high-level overview of the IoT asset inventory, including:

- Total number of registered devices
- Number of represented agencies
- Number of device manufacturers
- Device distribution by agency
- Distribution of devices by manufacturer

The dashboard is intended to provide an accessible summary of the current inventory and support identification of trends across the asset environment.

### Inventory Management

The Inventory page provides an interface for browsing and exploring registered IoT assets.

Users can:

- View the complete inventory
- Search for devices
- Filter devices by manufacturer
- Filter devices by agency
- Review device information
- Select an individual device for additional security analysis

## Vulnerability Analysis Workflow

The application supports an interactive vulnerability analysis workflow.

```text
IoT Asset Inventory
        │
        ▼
   Select Device
        │
        ▼
 Retrieve CPE Candidates
        │
        ▼
   User Selects CPE
        │
        ▼
 Retrieve CVE Information
        │
        ▼
 Display Vulnerability Metrics
