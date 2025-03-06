### Fixed Assets Management System
## Overview
The Fixed Assets Management System is designed to help organizations efficiently track and manage their fixed assets. Fixed assets, also known as property, plant, and equipment (PP&E), are long-term tangible assets that a company owns and uses in its operations to generate income. These assets typically have a useful life of more than one year and are not easily converted into cash. 
INVESTOPEDIA.COM

## Features
Asset Management: Add, update, delete, and view details of fixed assets.
Assignment Management: Assign assets to employees or departments and track their status.
Location Management: Define and manage locations where assets are stored or utilized.
Depreciation Tracking: Monitor asset depreciation over time to reflect their current value.
# Installation
Clone the Repository:

git clone https://github.com/CorneliusKibetDC/fixed_assets.git
cd fixed_assets
Create and Activate a Virtual Environment:

# bash
python -m venv env
source env/bin/activate  # On Windows, use 'env\Scripts\activate'
Install Dependencies:

# bash
pip install -r requirements.txt

Set Up Environment Variables:

Create a .env file in the project root directory and define the necessary environment variables, such as database connection strings and secret keys.

Initialize the Database:

Run the database migration scripts or use the provided setup scripts to initialize the database schema.

# Usage
Start the Application:
python app.py
Access the Application:

Open your web browser and navigate to http://localhost:5000 to access the Fixed Assets Management System.

# Contributing
Contributions are welcome! Please follow these steps:

# Fork the repository.
Create a new branch: git checkout -b feature-branch-name.
Make your changes and commit them: git commit -m 'Add new feature'.
Push to the branch: git push origin feature-branch-name.
Submit a pull request detailing your changes.

# License
This project is licensed under the MIT License. See the LICENSE file for more details.


