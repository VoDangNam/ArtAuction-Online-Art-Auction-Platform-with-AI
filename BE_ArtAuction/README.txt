================================================================================
                    INSTALLATION GUIDE
                    ART AUCTION BACKEND SYSTEM
================================================================================

I. SYSTEM REQUIREMENTS
================================================================================

1. Java Development Kit (JDK)
   - Version: JDK 17 or higher
   - Download: https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html
   - Or OpenJDK: https://adoptium.net/

2. Apache Maven
   - Version: 3.6.0 or higher
   - Download: https://maven.apache.org/download.cgi
   - Or use the Maven Wrapper (mvnw) included in the project

3. MongoDB
   - Version: 4.4 or higher
   - Download: https://www.mongodb.com/try/download/community
   - Or use MongoDB Atlas (cloud service)

4. Redis
   - Version: 6.0 or higher
   - Download: https://redis.io/download
   - Or use Redis Cloud

5. IDE (Optional but recommended)
   - IntelliJ IDEA
   - Eclipse
   - Visual Studio Code with Java Extension Pack

================================================================================
II. TOOLS & LIBRARIES
================================================================================

1. Framework & Core
   - Spring Boot 3.2.0
   - Spring Framework
   - Spring Security
   - Spring Data MongoDB
   - Spring Data Redis
   - Spring WebSocket
   - Spring Mail
   - Spring WebFlux

2. Database & Cache
   - MongoDB (Primary database)
   - Redis (Cache and session management)

3. Authentication & Security
   - JWT (JSON Web Token) – io.jsonwebtoken:jjwt-api:0.11.5
   - Spring Security

4. API Documentation
   - SpringDoc OpenAPI 2.2.0 (Swagger UI)
   - Access URL: http://localhost:8081/swagger-ui/index.html

5. Cloud Services
   - Cloudinary (Image management) – cloudinary-http44:1.33.0

6. Utilities
   - Lombok (Reduce boilerplate code)
   - ModelMapper 3.1.1 (Object mapping)
   - Jackson (JSON processing)
   - Thymeleaf (Email templates)

7. Build Tool
   - Apache Maven
   - Maven Compiler Plugin (Java 17)

8. Development Tools
   - Spring Boot DevTools (Hot reload)

9. Testing
   - Spring Boot Test
   - Spring Security Test

================================================================================
III. DETAILED INSTALLATION GUIDE
================================================================================

STEP 1: Install Java JDK 17
---------------------------
1. Download and install JDK 17
2. Set the JAVA_HOME environment variable
3. Add JAVA_HOME/bin to the system PATH
4. Verify installation:
   java -version

STEP 2: Install Maven (If not available)
----------------------------------------
1. Download Maven from https://maven.apache.org/download.cgi
2. Extract Maven to a directory (e.g., C:\Program Files\Apache\maven)
3. Set the MAVEN_HOME environment variable
4. Add MAVEN_HOME/bin to the system PATH
5. Verify installation:
   mvn -version

NOTE: This project already includes Maven Wrapper (mvnw, mvnw.cmd),
so this step can be skipped.

STEP 3: Install MongoDB
-----------------------
Option 1: Local MongoDB Installation
1. Download MongoDB Community Server
2. Install and start the MongoDB service
3. Default MongoDB port: 27017

Option 2: MongoDB Atlas (Cloud)
1. Register at https://www.mongodb.com/cloud/atlas
2. Create a cluster and obtain the connection string
3. Update the connection string in the configuration file

STEP 4: Install Redis
---------------------
Option 1: Local Redis Installation
- Windows: Download from https://github.com/microsoftarchive/redis/releases
- Linux/macOS:
  sudo apt-get install redis-server
  or
  brew install redis
- Start Redis:
  redis-server
- Default Redis port: 6379

Option 2: Redis Cloud
1. Register at https://redis.com/try-free/
2. Create a database and obtain the connection string
3. Update the connection information in the configuration file

STEP 5: Configure Cloudinary (Optional – for image upload)
----------------------------------------------------------
1. Register at https://cloudinary.com/
2. Obtain Cloud Name, API Key, and API Secret
3. Update these values in application.properties

STEP 6: Configure Email Service (Optional)
------------------------------------------
1. Configure SMTP server settings in application.properties
2. Example services: Gmail SMTP, Outlook SMTP, or custom SMTP server

STEP 7: Build and Run the Project
---------------------------------
1. Open terminal/command prompt in the project root directory

2. Build the project:
   - Windows:
     mvnw.cmd clean install
   - Linux/macOS:
     ./mvnw clean install

3. Run the application:
   - Windows:
     mvnw.cmd spring-boot:run
   - Linux/macOS:
     ./mvnw spring-boot:run

   Or using Maven (if installed):
     mvn clean install
     mvn spring-boot:run

4. The application will run at:
   http://localhost:8081

5. Access Swagger UI:
   http://localhost:8081/swagger-ui/index.html

================================================================================
IV. ENVIRONMENT CONFIGURATION
================================================================================

Create application.properties or application.yml in:
src/main/resources/

Required configurations:
- MongoDB connection string
- Redis connection (host, port, password if applicable)
- JWT secret key
- Cloudinary credentials (if used)
- Email SMTP settings (if used)
- Server port (default: 8081)

Example basic configuration:
spring.data.mongodb.uri=mongodb://localhost:27017/artauction
spring.data.redis.host=localhost
spring.data.redis.port=6379
server.port=8081

================================================================================
V. INSTALLATION VERIFICATION
================================================================================

1. Check Java:
   java -version (must show version 17)
2. Check Maven:
   mvn -version or mvnw -version
3. Check MongoDB:
   mongosh (or mongo) to connect
4. Check Redis:
   redis-cli ping (should return PONG)
5. Build project:
   mvnw clean install (no errors)
6. Run application:
   mvnw spring-boot:run
7. Access:
   http://localhost:8081/swagger-ui/index.html

================================================================================
VI. TROUBLESHOOTING
================================================================================

Issue: Port already in use
- Solution: Change the port in application.properties or stop the application
  currently using that port

Issue: Cannot connect to MongoDB
- Ensure MongoDB service is running
- Verify the connection string in configuration
- Check firewall settings

Issue: Cannot connect to Redis
- Ensure Redis server is running
- Verify Redis host and port configuration

Issue: Lombok does not work
- Install Lombok plugin in your IDE
- Enable annotation processing in IDE settings


All sensitive information (API keys, passwords, tokens, secrets)
has been removed from this repository.

Please create your own `application.properties` file
and replace the placeholder values (e.g. {{JWT_SECRET}})
with valid credentials before running the project.