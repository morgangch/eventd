FROM gcc:14-bookworm AS builder

WORKDIR /app
COPY . /app

RUN apt-get update && \
	apt-get install -y --no-install-recommends cmake && \
	rm -rf /var/lib/apt/lists/*

RUN cmake -S . -B build && cmake --build build --config Release

FROM gcc:14-bookworm

WORKDIR /opt/eventd
COPY --from=builder /app/build/eventd-core /usr/local/bin/eventd-core

ENTRYPOINT ["eventd-core"]
