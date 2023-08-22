#!/bin/sh
# Provided kubernetes environment variables cannot be injected to the nginx in run-time.
# Because frontend/src/main.js is already built when k8s env is provided.
# That's why we find this solution to replace special keys before running nginx

ROOT_DIR=/usr/share/nginx/html

# Replace env vars in files served by NGINX
for file in "$ROOT_DIR"/assets/*.js* $ROOT_DIR/index.html; do
    sed -i 's|VITE_BACKEND_API_BASE_URL|'${VITE_BACKEND_API_BASE_URL}'|g' $file
    # Your other variables here...
done
