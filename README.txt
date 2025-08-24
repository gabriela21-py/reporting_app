Project Overview

General Description

This project is an interactive web application built using the Flask and
Dash frameworks. Its main purpose is to display data extracted from a
PostgreSQL database in the form of charts and tables.

The application analyzes JIRA tickets and allows filtering them by teams
as well as classifying them according to status, priority, severity,
testing state, etc.

⚠️ Note: The application is not functional outside the company because
it is connected to a database specifically created for the internship
program. Therefore, a folder with screenshots of the graphical interface
is included.

------------------------------------------------------------------------

Project Structure

database/

Contains classes for database connections and SQL abstraction:
- db_interface.py – common interface for database connections
- postgres.py – PostgreSQL implementation

graph/

Contains all components that generate the dashboard charts:
- chart_interface.py – common interface for all charts
- donut_chart.py, pie_chart.py – circular charts
- CRD_SYRD_chart.py – chart for CRD/SyRD requirements
- test_case_chart.py – chart for requirements with/without testing
- syrd_state_chart.py – visualization of SyRD requirement states
- bar_chart.py – optional, for bar charts
- table.py – interactive table with statuses and priorities

static/

Contains static files:
- css/style.css – CSS styles applied to graphical elements and layout

templates/

Contains HTML templates for the Flask side:
- index.html – main page served at route /
- dashboard.html – layout for the dashboard page

------------------------------------------------------------------------

Containerization Files

-   Dockerfile – defines instructions to build the Docker image of the
    application

-   docker-compose.yml – configures services (e.g., app + PostgreSQL)
    and runs them together

-   requirements.txt – list of all dependencies required to run the
    project in Python environment.
    Install with:

        pip install -r requirements.txt

------------------------------------------------------------------------

Folder: Web Application Screenshots

Contains graphical interface screenshots.

------------------------------------------------------------------------

Main Python Files

-   app.py
    Initializes the Flask and Dash application, defines the / route for
    the main page and /dashboard for the interactive dashboard.

-   config.py
    Stores SQL queries in variables, e.g.: PROBLEM_QUERY,
    PRIORITY_QUERY, SEVERITY_QUERY, etc.

-   dashboard.py
    Defines the dashboard layout and registers Dash callbacks to update
    charts based on selected filters.

-   utils.py
    Contains helper functions, e.g., create_dropdown for styled
    dropdowns.

------------------------------------------------------------------------

Main Functionality

-   User accesses the main page (/)
-   From there, the dashboard can be accessed (/dashboard)
-   The dashboard displays:
    -   Donut and pie charts with distributions by status, priority,
        severity
    -   Interactive tables
    -   Dropdowns for filtering by team or other parameters
-   Charts are built with Plotly and updated automatically via Dash
    callbacks
-   Data is extracted from the jira_snapshot table in PostgreSQL
-   The project can be easily run in a Docker container using the
    Dockerfile and docker-compose (tested on an Ubuntu VM)

------------------------------------------------------------------------

Conclusion

The project is organized in a modular way:
- Clear separation between application logic, graphical components,
configuration, and utilities
- Reusable and extensible graphical components
- Easy to add new filters, charts, or data sources

✅ Suitable for monitoring issues and requirements in an Agile team.
