#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

function print_header() {
    echo -e "\n${BLUE}===========================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}===========================================================${NC}\n"
}

function print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

function print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

function print_error() {
    echo -e "${RED}✗ $1${NC}"
}

function setup_environment() {
    print_header "Setting up the CDC Workshop Environment"
    
    echo "Starting Docker containers..."
    docker-compose up -d
    
    echo "Setting up Python virtual environment..."
    python -m venv venv
    
    # Activate virtual environment (varies by OS)
    if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "linux-gnu"* ]]; then
        source venv/bin/activate
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        print_warning "Unknown OS type. Please activate the virtual environment manually."
    fi
    
    echo "Installing Python requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    print_success "Environment setup completed"
    print_warning "Remember to activate the virtual environment before running Python scripts:"
    echo "  source venv/bin/activate  # On Linux/Mac"
    echo "  venv\\Scripts\\activate    # On Windows"
}

function cleanup() {
    print_header "Cleaning up the environment"
    
    echo "Stopping Docker containers..."
    docker-compose down
    
    echo "Removing volumes..."
    docker volume rm workshop-cdc_pulsar_data workshop-cdc_pulsar_conf workshop-cdc_postgres_data || true
    
    print_success "Cleanup completed"
}

function insert_test_data() {
    print_header "Inserting test data into PostgreSQL"
    
    echo "Inserting events..."
    docker exec -it workshop-cdc-postgres-1 psql -U postgres -c "
    INSERT INTO events (aggregatetype, aggregateid, payload)
    VALUES 
      ('user', '123', '{\"event\": \"user-created\", \"name\": \"John Doe\"}'),
      ('user', '124', '{\"event\": \"user-created\", \"name\": \"Jane Smith\"}'),
      ('order', '456', '{\"event\": \"order-created\", \"amount\": 100.50}'),
      ('payment', '789', '{\"event\": \"payment-received\", \"amount\": 100.50, \"method\": \"credit-card\"}');
    "
    
    print_success "Test data inserted"
}

function show_help() {
    echo "CDC Workshop Helper Script"
    echo
    echo "Usage: $0 [command]"
    echo
    echo "Commands:"
    echo "  setup       - Set up the workshop environment"
    echo "  cleanup     - Clean up the workshop environment"
    echo "  test-data   - Insert test data into PostgreSQL"
    echo "  help        - Show this help message"
}

case "$1" in
    setup)
        setup_environment
        ;;
    cleanup)
        cleanup
        ;;
    # Removed create-topic option as Pulsar creates topics automatically
    test-data)
        insert_test_data
        ;;
    help|*)
        show_help
        ;;
esac
