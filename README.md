# Python Flask OAuth CRUD App

## Usage:

### Build and Run with Docker Compose:

1. Build the Docker images:

   ```bash
   docker-compose build
   ```
   
   This will run the tests and build the image if successful.

2. Run the Docker containers:

   ```bash
   docker-compose up
   ```

   This will start the application and run tests.

3. Access the application:

   Open your web browser and navigate to [http://localhost:5000](http://localhost:5000) to access the app.

### Alternative: Build and Run Manually:

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run tests:

   ```bash
   python -m pytest
   ```

   Ensure that tests pass before proceeding to the next step.

3. Run the application:

   ```bash
   python main.py
   ```

   The application will be accessible at [http://localhost:5000](http://localhost:5000).