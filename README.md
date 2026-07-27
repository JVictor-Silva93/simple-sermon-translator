# Simple Sermon Translator

An open-source application for producing real-time translated sermon captions and optional translated audio.

A church connects a soundboard or microphone feed to the application. Congregation members open a webpage on their phones to read translated captions, hear translated speech, or use both.

> [!IMPORTANT]
> This project is in its early development and experimentation stage. It is not yet ready for use during a live service.

## Goals

The project aims to provide:

* Real-time speech transcription.
* Spanish and Portuguese translation.
* Optional text-to-speech output.
* A simple browser interface for listeners.
* Local operation on a computer at the church.
* An optional deployment path for a GPU virtual machine owned by the church.
* Offline local operation after models have been downloaded.
* An open-source codebase that organizations can inspect, modify, and deploy themselves.

## Architecture

The project is divided into two Python components and a collection of deployment configurations.

```text
simple_sermon_translator/
├── engine/
├── app/
├── deployments/
├── docs/
├── scripts/
├── pyproject.toml
├── uv.lock
└── README.md
```

### Engine

The `engine` package contains the reusable audio and machine-learning pipeline.

Its intended responsibilities include:

* Receiving audio from a local device or network source.
* Detecting speech boundaries.
* Transcribing speech.
* Translating finalized transcripts.
* Optionally generating translated speech.
* Emitting typed caption, translation, audio, status, and error events.
* Loading and managing models.
* Detecting available hardware.
* Benchmarking pipeline performance.

The engine must remain independent of FastAPI, HTML, WebSockets, and deployment-specific code.

### Application

The `app` package contains the FastAPI application and browser interfaces.

Its intended responsibilities include:

* Starting and stopping translation sessions.
* Selecting audio inputs and target languages.
* Displaying source and translated captions to the operator.
* Broadcasting captions to listener devices.
* Streaming translated audio when TTS is enabled.
* Displaying listener links and QR codes.
* Reporting latency, model status, connection counts, and errors.
* Receiving audio over the network when running in cloud mode.

The application uses the engine through its public Python interface. It does not load or call machine-learning models directly.

### Deployments

The `deployments` directory contains packaging and infrastructure configuration.

Planned deployment targets include:

```text
deployments/
├── docker/
├── gcp/
└── windows/
```

This directory is not a Python package and is not a member of the uv workspace.

## Operating Modes

The same FastAPI application is intended to support two modes.

### Local mode

In local mode:

* The application runs on a computer at the church.
* Audio is captured directly from a microphone, USB interface, or soundboard input.
* Listener devices connect over the church’s local network.
* Processing occurs on the church’s hardware.
* Internet access is not required after installation, activation, and model download.

### Cloud mode

In cloud mode:

* The church deploys the application into its own cloud account.
* Audio is sent from the church to the cloud application.
* Listeners connect to a public HTTPS address.
* The church owns its infrastructure, data, and cloud bill.
* The GPU virtual machine should be stopped when it is not being used.

Cloud mode is a deployment option, not a vendor-operated SaaS.

## uv Workspace

This repository uses a uv workspace containing two members:

```toml
[tool.uv.workspace]
members = [
    "engine",
    "app",
]
```

Each member has its own `pyproject.toml` and declares its own direct dependencies.

The workspace shares:

* One `uv.lock` file.
* One default `.venv`.
* One compatible dependency resolution.
* Shared development dependencies.

The application depends on the local engine workspace member.

```toml
# app/pyproject.toml

[project]
dependencies = [
    "engine",
]

[tool.uv.sources]
engine = { workspace = true }
```

## Development Setup

### Requirements

* Python 3.12
* uv
* Git

GPU acceleration and model-specific native dependencies will be documented after the initial compatibility experiments are complete.

### Clone the repository

```bash
git clone https://github.com/JVictor-Silva93/simple-sermon-translator.git
cd simple_sermon_translator
```

### Install the workspace

```bash
uv sync --all-packages
```

### Confirm the Python environment

```bash
uv run python --version
```

### Add a dependency to the engine

```bash
uv add --package engine <dependency>
```

### Add a dependency to the application

```bash
uv add --package app <dependency>
```

Additional test, lint, benchmark, and application commands will be documented as those commands are implemented.

## Development Principles

The project currently follows these principles:

1. Prove the difficult pipeline before building a polished interface.
2. Keep the engine independent of web frameworks.
3. Use the same application for local and cloud operation.
4. Avoid services such as Redis, Celery, and external databases until they solve a demonstrated problem.
5. Load models once per session rather than once per request.
6. Measure real-time performance instead of estimating it from VRAM alone.
7. Keep listener pages lightweight and accessible on lower-powered phones.
8. Preserve local and offline operation as a primary capability.
9. Do not store raw audio or complete transcripts by default.
10. Add abstractions and directories when the implementation requires them, not before.

## Planned Pipeline

```text
Audio input
    ↓
Voice activity detection and segmentation
    ↓
Speech transcription
    ↓
Text translation
    ↓
Translated caption event
    ↓
Optional text-to-speech
    ↓
Listener browser
```

The first release will use finalized speech segments. Continuously changing partial captions may be added later.

## Roadmap

### Phase 0 — Compatibility and hardware spike

Determine whether the proposed tools can operate together and keep up with real-time audio.

Planned work:

* Confirm the supported Python version.
* Compare faster-whisper and alternative transcription implementations.
* Test the selected translation model.
* Test Spanish and Portuguese translation quality.
* Test the selected TTS implementation.
* Pin compatible PyTorch and CUDA versions.
* Measure CPU, system memory, and GPU memory usage.
* Calculate the real-time factor of the complete pipeline.
* Test browser-based audio capture for cloud mode.
* Document model licenses and redistribution restrictions.

**Deliverable:** A technical decision and benchmark report.

### Phase 1 — Transcription engine and CLI

Build:

* Audio-device enumeration.
* Local audio capture.
* Speech segmentation.
* Transcription.
* Typed engine events.
* Session startup and shutdown.
* A basic command-line interface.

**Deliverable:** Live microphone audio produces finalized captions in the terminal.

### Phase 2 — Translation

Build:

* Translation interface.
* Spanish translation.
* Portuguese translation.
* Translation events.
* Language configuration.
* Translation tests.

**Deliverable:** Live microphone audio produces translated terminal captions.

### Phase 3 — Local browser application

Build:

* Minimal FastAPI application.
* Operator page.
* Start and stop controls.
* Audio-device selection.
* Listener page.
* Caption WebSocket.
* Listener QR code.
* Local-network access.

**Deliverable:** A listener can read translated captions from a phone connected to the church network.

### Phase 4 — Text-to-speech

Build:

* TTS engine interface.
* Translated audio events.
* Browser audio playback.
* Audio buffering and sequencing.
* Per-language TTS controls.
* TTS performance benchmark.

**Deliverable:** A listener can hear translated audio through the browser.

### Phase 5 — Setup and reliability

Build:

* First-run setup.
* Input-level testing.
* Hardware benchmarking.
* Recommended hardware profiles.
* Settings persistence.
* Automatic reconnection.
* Operator diagnostics.
* Error recovery.
* Exportable support logs.

**Deliverable:** A church operator can configure and run the application without editing source code.

### Phase 6 — Cloud mode

Build:

* Network audio input.
* Authenticated audio connections.
* Operator authentication.
* Public listener sessions.
* HTTPS support.
* Cloud-specific configuration and health reporting.

**Deliverable:** Audio sent to a GPU server produces translated captions on listener devices.

### Phase 7 — GCP deployment

Build:

* GPU-compatible Docker image.
* Persistent model storage.
* VM startup configuration.
* Automatic shutdown.
* Firewall and HTTPS configuration.
* Deployment and upgrade documentation.
* Cost-control guidance.

**Deliverable:** An organization can deploy the application into its own GCP project.

### Phase 8 — Windows packaging and stable release

Build:

* Windows packaging.
* Model installation workflow.
* Release automation.
* Upgrade instructions.
* Stable user documentation.

**Deliverable:** A stable version suitable for testing with participating churches.

## Version-One Scope

The planned first stable version includes:

* Local audio capture.
* Network audio input for cloud mode.
* Finalized live captions.
* Spanish translation.
* Portuguese translation.
* Optional translated audio.
* Operator and listener browser interfaces.
* Local-network operation.
* Docker packaging.
* A documented GCP deployment.
* Windows as the primary local platform.
* Hardware benchmarking and capability reporting.
* Model checksum verification.
* Connection recovery and diagnostic logging.

## Not Planned for Version One

The following are intentionally outside the initial scope:

* Vendor-operated SaaS.
* Subscription billing.
* Django.
* Native mobile applications.
* Voice cloning.
* Multiple voices per language.
* Long-term sermon storage.
* Analytics dashboards.
* OBS or ProPresenter integration.
* Partial captions.
* Automatic multi-server scaling.
* Multiple simultaneous sermons in one process.

## Model Files and Licenses

Large model files will not be committed to this repository.

Each supported model may have licensing terms that differ from the source-code license. Before a model is officially supported, the project must document:

* The model name and version.
* Its source.
* Its license.
* Whether redistribution is allowed.
* Whether commercial use is allowed.
* Any attribution requirements.

Users are responsible for complying with the licenses of the models they download and use.

## Privacy

The application should process sermon audio without retaining it by default.

The project should not store the following unless an operator explicitly enables storage:

* Raw sermon audio.
* Complete transcripts.
* Translated transcripts.
* Generated translated audio.

Diagnostic logs should contain performance and error information without unnecessarily including sermon content.

## Contributing

The project is currently in early development.

Before beginning a substantial change:

1. Check the existing GitHub issues.
2. Open or comment on an issue describing the proposed work.
3. Keep changes focused on one feature, bug, or technical decision.
4. Add or update tests when behavior changes.
5. Update documentation when setup or usage changes.

Detailed contribution guidelines may be moved into `CONTRIBUTING.md` as the contributor community grows.

## Reporting Bugs

When reporting a bug, include:

* The operating system.
* The Python version.
* Whether processing ran on CPU or GPU.
* The GPU model and VRAM, when applicable.
* The relevant application or engine version.
* Steps to reproduce the problem.
* Expected and actual behavior.
* Relevant logs with private information removed.

Do not include private sermon audio or transcripts in a public issue.

## Security

Do not publicly disclose a vulnerability that could expose audio, transcripts, credentials, or administrative access.

Until a dedicated security policy and private reporting address are published, open a minimal issue stating that you found a potential security problem without including exploitation details or sensitive data.

A separate `SECURITY.md` will be added before the project is recommended for production deployment.

## Project Management

Development work is tracked with GitHub Issues and GitHub Projects.

The project board uses the following statuses:

* Backlog
* Ready
* In progress
* Blocked
* Done

Each roadmap phase has a parent issue. Concrete features, experiments, tasks, documentation work, and bugs are tracked as individual issues or sub-issues.

Only the next one or two phases are broken down in detail. Later phases remain broad until earlier experiments provide enough information to plan them accurately.

## License

The source-code license has not yet been finalized.

A `LICENSE` file will be added before the project accepts outside contributions or publishes a stable release. Model files remain governed by their respective licenses regardless of the license selected for this repository.
