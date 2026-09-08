# Simple Sermon Translator

An open-source application for producing real-time translated sermon captions and optional translated audio.

A church connects a soundboard or microphone feed to the application. Congregation members open a webpage on their phones to read translated captions, hear translated speech, or use both.

> [!IMPORTANT]
> This project is in its early development and experimentation stage. It is not yet ready for use during a live service.

## Goals

The project aims to provide:

* Real-time speech transcription.
* Spanish and Portuguese translation (to start, but it should be easy to add more).
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

## Development Setup

### Requirements

* Python 3.12
* uv
* Git

GPU acceleration and model-specific native dependencies will be documented after the initial compatibility experiments are complete.

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

The roadmap follows YAGNI: build the smallest working vertical slice, validate
it, and add complexity only when a demonstrated requirement calls for it.
Technical choices are evaluated in the phase that uses them rather than in a
large up-front compatibility project.

### Phase 0 — Compatibility and hardware spike

Prepare only what is needed to begin engine development:

* confirm that the `uv` workspace installs both packages;
* settle the public package and command names;
* add the basic lint and test commands used by the first implementation work;
* add a small CI check for those commands;
* document the supported development Python version.

Do not select or benchmark translation, TTS, cloud-audio, or deployment tools in this phase.

**Deliverable:** A clean workspace in which both packages import and the basic development checks run successfully.

### Phase 1 — Engine transcription CLI

Build:

* audio-device enumeration.
* local audio capture.
* audio normalization and segmentation;
* speech segmentation.
* one plausible transcription implementation;
* typed caption events;
* engine CLI;
* clean session shutdown;
* focused tests for the behavior introduced in this phase.

**Deliverable:**

```bash
sermon-engine listen
```

prints finalized live captions in the terminal with enough timing information to identify whether transcription is falling behind real time.

### Phase 2 — Translation

Build:

* one plausible translation implementation;
* initial Spanish support;
* initial Portuguese support;
* translation events;
* language configuration;
* focused translation tests.

**Deliverable:** Live local audio produces translated terminal captions in Spanish and Portuguese.

### Phase 3 — Local FastAPI application

Build:

* minimal operator page;
* start and stop controls;
* audio-device selection;
* listener join page;
* caption WebSocket;
* listener QR code;
* local-network operation;
* focused application and WebSocket tests.

**Deliverable:** A listener can read translated captions from a phone connected to the church network.

### Phase 4 — Text-to-speech

Build:

* one plausible TTS implementation for the supported languages;
* TTS engine interface;
* translated audio events;
* audio buffering and sequencing;
* browser playback;
* per-language TTS enablement;
* end-to-end timing measurement with TTS enabled.

**Deliverable:** A listener can hear translated audio from the phone browser without the pipeline continually falling behind.

### Phase 5 — Setup and reliability

Build:

* first-run setup;
* audio-level testing;
* download and checksum verification for the models actually in use;
* a hardware benchmark based on the working pipeline;
* a recommended capability profile;
* settings persistence;
* automatic WebSocket reconnection;
* diagnostics and operator monitoring;
* recovery for failures observed during development and local testing.

**Deliverable:** A church operator can configure and run the application without editing source code.

### Phase 6 — Windows packaging and local pilot

Add:

* a Windows packaging approach for the working local application;
* persistent application, configuration, and model directories;
* model setup during or after installation;
* startup and uninstall support;
* installation and operator documentation;
* the fixes required by testing with participating churches.

Do not build a general-purpose updater or distribution service unless pilot experience demonstrates that it is needed.

**Deliverable:** A participating church can install and evaluate the local application on a supported Windows computer.

### Phase 7 — Cloud mode

Build:

* pushed-audio engine source;
* authenticated cloud audio endpoint;
* the smallest browser audio-capture implementation needed to test real church input;
* public listener sessions;
* operator authentication;
* HTTPS deployment;
* cloud-specific health reporting;
* connection and message limits appropriate for a public service.

**Deliverable:** Audio sent to a GPU server produces translated captions on listener devices.

### Phase 8 — GCP deployment

Build:

* Docker image;
* GPU VM deployment configuration;
* persistent model storage;
* startup automation;
* shutdown automation;
* documented cost controls;
* upgrade procedure;
* recovery instructions based on the selected deployment design.
* firewall and HTTPS configuration.
* deployment and upgrade documentation.
* cost-control guidance.

**Deliverable:** A church can deploy the project into its own GCP account using documented commands.

### Phase 9 — Stable version-one release

Complete the work required to support the already-built version-one features:

* release automation;
* supported-hardware and known-limitations documentation;
* security and privacy review;
* accessibility and low-powered-phone testing;
* installation, operation, upgrade, and troubleshooting documentation;
* signed release artifacts where practical;
* final license, contribution, security, and model-license documentation.

**Deliverable:** A stable open-source release supporting local Windows operation and a documented GCP deployment.

---

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

## Workflow Conventions

This repo uses an issue-driven workflow. The issue number is the source of truth.

Issues: clear, intent-focused titles (e.g. `#123 Add retry logic to uploads`)

Branches:
<type>/<issue>-<desc>
Types: feat, fix, refactor, chore, docs, test
Example: feat/123-upload-retry

Commits:
#123 Short, descriptive message

Pull Requests:
Title: #123 Short description
Description: Closes #123

All work should reference its issue number.

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
