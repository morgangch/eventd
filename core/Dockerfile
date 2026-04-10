FROM gcc:14-bookworm AS builder

WORKDIR /app
COPY . /app

RUN cmake -S . -B build && cmake --build build --config Release

FROM debian:bookworm-slim

WORKDIR /opt/eventd
COPY --from=builder /app/build/eventd-core /usr/local/bin/eventd-core

ENTRYPOINT ["eventd-core"]
