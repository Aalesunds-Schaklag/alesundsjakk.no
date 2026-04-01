FROM node:22-bookworm-slim

RUN npx -y playwright install --with-deps chrome

ENTRYPOINT ["npx", "-y", "@playwright/mcp@latest"]
