# ---- Stage 2: runtime ----
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH" \
    PORT=8080 

WORKDIR /app

# Install ONLY the runtime system dependencies for WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 \
    libffi8 \
    shared-mime-info \
    libharfbuzz0b \
    libicu-dev \
    libgirepository-1.0-1 \
    fonts-dejavu \
    fonts-liberation \
 && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from the builder stage
COPY --from=builder /venv /venv

# ---- ADD STATICFILES PERMISSIONS HERE ----
# Create the staticfiles directory and set ownership before switching to appuser
RUN mkdir -p /app/staticfiles \
    && chown -R appuser:appuser /app/staticfiles

# Create non-root user and switch to it
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Copy the app code
COPY --chown=appuser:appuser . .

# Copy and set up the entrypoint script
COPY --chown=appuser:appuser ./entrypoint.sh /usr/src/app/
RUN chmod +x /usr/src/app/entrypoint.sh

EXPOSE 8080 

# Use the entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
