FROM python:3.12-slim

# Install system dependencies and create a non-root user
RUN apt update && apt install -y git && apt clean && apt autoremove -y && \
    groupadd --gid 1000 --system ignifai && \
    useradd --uid 1000 --system --gid ignifai --create-home --shell /bin/bash ignifai


# Switch to the newly created user
USER ignifai

# Add environment variables
ENV USER_SPACE=/home/ignifai
ENV PATH=$USER_SPACE/.local/bin:$PATH
ENV WORKSPACE_DIR=$USER_SPACE/workspace 
ENV TMP_DIR=$USER_SPACE/tmp
ENV PYTHONUNBUFFERED=1
ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.0.0

WORKDIR $WORKSPACE_DIR

COPY --chmod=777 pyproject.toml .
RUN pip install -U pip setuptools && \
    pip install --no-build-isolation -e . && pip cache purge

ARG PRIVATE_REPOS_GH
ARG SUFFIX_ignifai_devkit=''

# END of docker cache
ARG CACHEBUST=1
RUN pip install "git+https://$PRIVATE_REPOS_GH/ignifai-devkit.git$SUFFIX_ignifai_devkit" && \
    pip cache purge

# Copy and install the application from source
COPY --chmod=777 . .
RUN pip install -e . && pip cache purge

# run the application
CMD ["uvicorn", "api_private.main:app", "--host", "0.0.0.0", "--port", "8091", "--proxy-headers", "--log-level", "warning"]