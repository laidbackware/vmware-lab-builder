#!/bin/sh

# Detect system architecture
ARCH=$(uname -m)

# Set the appropriate software path based on architecture
if [ "$ARCH" = "x86_64" ]; then
    cp /usr/local/bin/om-amd64 /usr/local/bin/om
elif [ "$ARCH" = "aarch64" ]; then
    cp /usr/local/bin/om-arm64 /usr/local/bin/om
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi
chmod +x /usr/local/bin/om \

exec "$@"
