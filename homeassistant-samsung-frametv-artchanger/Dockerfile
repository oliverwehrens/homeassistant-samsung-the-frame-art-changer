ARG BUILD_FROM=ghcr.io/home-assistant/base:3.23
FROM ${BUILD_FROM}

# Install dependencies
RUN \
  apk add --no-cache \
    python3 py3-pip git curl tar

# Download and install dezoomify-rs based on the platform
ARG TARGETARCH
RUN case "${TARGETARCH}" in \
      amd64) dezoomify_arch="x86_64" ;; \
      arm64) dezoomify_arch="aarch64" ;; \
      *) echo "Unsupported TARGETARCH: ${TARGETARCH}" && exit 1 ;; \
    esac && \
    curl -fsSL "https://github.com/vivalatech/dezoomify-rs/releases/download/master/dezoomify-rs-${dezoomify_arch}-unknown-linux-musl.tgz" \
      | tar xz -C /usr/local/bin

# Install Python dependencies
RUN \
    pip3 install --no-cache-dir --break-system-packages git+https://github.com/NickWaterton/samsung-tv-ws-api.git pillow

# Copy data for add-on
COPY run.sh /
COPY *.py /
RUN mkdir -p /sources/
COPY sources/*.py /sources/
RUN mkdir -p /utils/
COPY utils/*.py /utils/

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]

LABEL \
    org.opencontainers.image.title="Samsung The Frame - Art Changer" \
    org.opencontainers.image.source="https://github.com/oliverwehrens/homeassistant-samsung-the-frame-art-changer"
