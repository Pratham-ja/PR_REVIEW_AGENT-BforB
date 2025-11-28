# Implementation Plan

- [x] 1. Update Dockerfile for SQLite deployment



  - Modify Dockerfile to remove PostgreSQL dependencies
  - Add SQLite3 support
  - Update DATABASE_URL environment variable to use SQLite
  - Add volume mount point for /app/data directory
  - Optimize image size for faster deployment

  - _Requirements: 1.1, 1.2, 1.4_

- [x] 2. Update database configuration for SQLite

  - Modify `repositories/database.py` to support SQLite connection strings
  - Update database initialization to create SQLite database file
  - Ensure directory exists before creating database
  - Add error handling for SQLite-specific issues
  - _Requirements: 1.3, 7.1_

- [x] 3. Update Alembic migrations for SQLite compatibility


  - Review existing migrations for PostgreSQL-specific features
  - Replace JSONB columns with TEXT columns
  - Replace UUID with TEXT for ID fields
  - Update timestamp columns for SQLite compatibility
  - Test migrations work with SQLite
  - _Requirements: 1.3_

- [x] 4. Add default configuration values


  - Update `config.py` to provide sensible defaults for optional environment variables
  - Ensure application starts without all env vars present
  - Document which variables are required vs optional
  - _Requirements: 1.5_

- [ ]* 4.1 Write property test for default configuration
  - **Property 1: Missing environment variables use defaults**
  - **Validates: Requirements 1.5**

- [x] 5. Implement log sanitization


  - Create utility function to sanitize log messages
  - Identify all environment variables that contain secrets
  - Replace secret values with [REDACTED] in logs
  - Apply sanitization to all logging calls
  - _Requirements: 5.5_

- [ ]* 5.1 Write property test for log sanitization
  - **Property 2: Secrets never appear in logs**
  - **Validates: Requirements 5.5**

- [x] 6. Create EC2 user data script


  - Write bash script to install Docker on Amazon Linux 2023
  - Add commands to enable Docker service on boot
  - Create application directory structure
  - Generate .env file from user data parameters
  - Pull and run Docker container
  - Set up log rotation
  - _Requirements: 2.3, 2.4, 5.3_

- [x] 7. Create deployment scripts


  - Create `deploy/build.sh` to build Docker image locally
  - Create `deploy/setup-ec2.sh` with EC2 setup commands
  - Create `deploy/update.sh` to update running container
  - Create `deploy/backup.sh` to create EBS snapshots
  - Make all scripts executable
  - Add error handling and validation
  - _Requirements: 8.1, 8.2, 8.4, 8.5_

- [x] 8. Create deployment documentation


  - Write `README_DEPLOYMENT.md` with step-by-step instructions
  - Document EC2 instance launch process
  - Document security group configuration
  - Document Elastic IP allocation and association
  - Include troubleshooting section
  - Add cost estimation and monitoring tips
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2_

- [x] 9. Update docker-compose.yml for SQLite


  - Modify docker-compose.yml to use SQLite instead of PostgreSQL
  - Remove PostgreSQL service
  - Update volume mounts for SQLite database
  - Update environment variables
  - _Requirements: 1.1, 7.1_

- [x] 10. Create .env.example for deployment


  - Create template with all required environment variables
  - Add comments explaining each variable
  - Include sensible defaults where applicable
  - Document which variables are required
  - _Requirements: 5.1, 5.3_

- [x] 11. Add Docker restart policy configuration


  - Update docker-compose.yml with restart: unless-stopped
  - Update deployment scripts to use --restart unless-stopped
  - Document restart behavior
  - _Requirements: 6.1_

- [ ]* 12. Test Docker build and container startup
  - Build Docker image and verify it completes successfully
  - Start container with minimal configuration
  - Verify API responds to health checks
  - Test database initialization creates SQLite file
  - Verify volume mounts work correctly
  - Test container restart preserves data
  - _Requirements: 1.2, 1.3, 1.4, 6.2, 7.2, 7.3_

- [ ]* 13. Test deployment scripts
  - Test build.sh creates image with correct tag
  - Test update.sh pulls and restarts container
  - Test backup.sh creates snapshots (if AWS configured)
  - Verify all scripts have proper error handling
  - _Requirements: 8.1, 8.2, 8.4, 8.5_

- [x] 14. Create AWS infrastructure setup guide


  - Document EC2 instance launch steps
  - Provide user data script template
  - Document security group rules (ports 22, 8000)
  - Document Elastic IP allocation steps
  - Include screenshots or CLI commands
  - _Requirements: 2.1, 2.2, 3.1, 3.2, 3.3, 4.1_

- [x] 15. Final checkpoint - Verify deployment works end-to-end


  - Ensure all tests pass, ask the user if questions arise
