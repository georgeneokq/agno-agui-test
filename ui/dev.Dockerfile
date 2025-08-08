FROM node:22-alpine AS runtime

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app/ui

# Package management
COPY ui/package.json \
  ui/pnpm-lock.yaml \
  ./

# Install dependencies
RUN mount=type=cache,id=pnpm,target=/pnpm/store \
  pnpm install --frozen-lockfile

# Copy code
COPY ./ui/src ./src/

COPY ui/next.config.ts \
  ui/postcss.config.mjs \
  ui/tsconfig.json \
  ./

EXPOSE 3000

# Disable Nextjs telemetry
RUN pnpm exec next telemetry disable

ENTRYPOINT ["pnpm", "dev"]
