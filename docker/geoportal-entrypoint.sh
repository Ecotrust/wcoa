#!/bin/bash
###################################
# This file 100% written by Copilot
###################################
set -e

echo "Starting Geoportal with configuration override..."

# Install gettext for envsubst command
echo "Installing gettext package for environment variable substitution..."
apt-get update -qq && apt-get install -y gettext-base && apt-get clean && rm -rf /var/lib/apt/lists/*

# Cleanup function for graceful shutdown
cleanup() {
    if [ ! -z "$TOMCAT_PID" ] && kill -0 $TOMCAT_PID 2>/dev/null; then
        echo "Cleaning up Tomcat process (PID: $TOMCAT_PID)..."
        kill $TOMCAT_PID 2>/dev/null
        sleep 2
        if kill -0 $TOMCAT_PID 2>/dev/null; then
            kill -9 $TOMCAT_PID 2>/dev/null
        fi
    fi
}
trap cleanup EXIT INT TERM

# Function to wait for WAR deployment
wait_for_deployment() {
    local app_name=$1
    local max_wait=120
    local wait_time=0
    
    echo "Waiting for $app_name to deploy..."
    while [ ! -d "/usr/local/tomcat/webapps/$app_name" ] && [ $wait_time -lt $max_wait ]; do
        sleep 2
        wait_time=$((wait_time + 2))
        echo "Waiting... ${wait_time}s"
    done
    
    if [ $wait_time -ge $max_wait ]; then
        echo "ERROR: $app_name failed to deploy within ${max_wait} seconds"
        return 1
    fi
    
    echo "$app_name deployed successfully"
    return 0
}

# Function to substitute environment variables in templates
substitute_variables() {
    local template_file=$1
    local output_file=$2
    
    echo "Processing template: $template_file -> $output_file"
    
    # Validate required environment variables
    local missing_vars=()
    if [ -z "$gpt_frame_options" ]; then
        missing_vars+=("gpt_frame_options")
    fi
    if [ -z "$gpt_allowed_origin" ]; then
        missing_vars+=("gpt_allowed_origin")
    fi
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        echo "WARNING: Missing required environment variables: ${missing_vars[*]}"
        echo "Check your .env file and ensure these variables are set"
    fi
    
    # Display current values for debugging
    echo "  gpt_frame_options = '$gpt_frame_options'"
    echo "  gpt_allowed_origin = '$gpt_allowed_origin'"
    
    # Validate CSP format (check for problematic characters)
    if echo "$gpt_allowed_origin" | grep -q ":.*\*"; then
        echo "  WARNING: Port wildcards (*) in CSP frame-ancestors may not be supported by all browsers"
        echo "  Consider using specific ports or removing wildcards if you encounter issues"
    fi
    
    # Use envsubst to replace environment variables
    envsubst < "$template_file" > "$output_file"
    
    if [ $? -eq 0 ]; then
        echo "Successfully processed $template_file"
        
        # Show a sample of the processed content for verification
        echo "Sample of processed content:"
        grep -E "(frame-options|Content-Security-Policy)" "$output_file" | head -2 | sed 's/^/  /'
    else
        echo "ERROR: Failed to process $template_file"
        return 1
    fi
}

# Start Tomcat in background to deploy WARs
echo "Starting Tomcat to deploy applications..."
catalina.sh run &
TOMCAT_PID=$!
echo "Tomcat started with PID: $TOMCAT_PID"

# Wait for both applications to deploy
wait_for_deployment "geoportal" || exit 1
wait_for_deployment "harvester" || exit 1

# Additional wait to ensure full extraction
echo "Waiting for full application extraction..."
sleep 10

# Create config directory if it doesn't exist
CATALOG_CONFIG_DIR="/usr/local/tomcat/webapps/geoportal/WEB-INF/classes/config"
mkdir -p "$CATALOG_CONFIG_DIR"
HARVESTER_CONFIG_DIR="/usr/local/tomcat/webapps/harvester/WEB-INF/classes/config"
mkdir -p "$HARVESTER_CONFIG_DIR"

# Process and copy authentication configuration
if [ -f "/templates/authentication-simple.xml" ]; then
    substitute_variables "/templates/authentication-simple.xml" "$CATALOG_CONFIG_DIR/authentication-simple.xml"
    substitute_variables "/templates/authentication-simple.xml" "$HARVESTER_CONFIG_DIR/authentication-simple.xml"
else
    echo "WARNING: authentication-simple.xml template not found"
fi

# Process and copy security configuration
if [ -f "/templates/catalog-app-security.xml" ] && [ -f "/templates/harvester-app-security.xml" ]; then
    substitute_variables "/templates/catalog-app-security.xml" "$CATALOG_CONFIG_DIR/app-security.xml"
    substitute_variables "/templates/harvester-app-security.xml" "$HARVESTER_CONFIG_DIR/app-security.xml"
else
    echo "WARNING: app-security.xml templates not found"
    if [ ! -f "/templates/catalog-app-security.xml" ]; then
        echo "  Missing: /templates/catalog-app-security.xml"
    fi
    if [ ! -f "/templates/harvester-app-security.xml" ]; then
        echo "  Missing: /templates/harvester-app-security.xml"
    fi
fi

# Verify the configuration files were created
echo "Verifying configuration files..."
if [ -f "$CATALOG_CONFIG_DIR/authentication-simple.xml" ]; then
    echo "✓ authentication-simple.xml configured"
else
    echo "✗ authentication-simple.xml missing"
fi

if [ -f "$CATALOG_CONFIG_DIR/app-security.xml" ]; then
    echo "✓ CATALOG app-security.xml configured"
else
    echo "✗ CATALOG app-security.xml missing"
fi

if [ -f "$HARVESTER_CONFIG_DIR/authentication-simple.xml" ]; then
    echo "✓ HARVESTER authentication-simple.xml configured"
else
    echo "✗ HARVESTER authentication-simple.xml missing"
fi

if [ -f "$HARVESTER_CONFIG_DIR/app-security.xml" ]; then
    echo "✓ app-security.xml configured"
else
    echo "✗ app-security.xml missing"
fi

# Stop background Tomcat gracefully so H2 can flush and release its lock
echo "Stopping background Tomcat (PID: $TOMCAT_PID)..."

if kill -0 $TOMCAT_PID 2>/dev/null; then
    echo "Requesting graceful Tomcat shutdown via catalina.sh stop..."
    catalina.sh stop 30 -force
    # Wait for the background process to exit
    for i in {1..35}; do
        if ! kill -0 $TOMCAT_PID 2>/dev/null; then
            echo "Tomcat stopped gracefully"
            break
        fi
        echo "Waiting for shutdown... ${i}/35"
        sleep 1
    done
    # Final safety net
    if kill -0 $TOMCAT_PID 2>/dev/null; then
        echo "Force stopping Tomcat..."
        kill -9 $TOMCAT_PID
        sleep 2
    fi
else
    echo "Tomcat process was not running (PID $TOMCAT_PID)"
fi

echo "Tomcat stopped successfully"

# Remove any stale H2 lock/trace files left by the background Tomcat run.
# These persist in the named volume and prevent the DB from opening on restart.
echo "Cleaning up stale H2 artifacts in /root..."
rm -f /root/harvester.lock.db /root/harvester.trace.db

# Start Tomcat in foreground
echo "Starting Tomcat with updated configuration..."
exec catalina.sh run