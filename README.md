# LLM-texforge-cli
## Latex LLM Orchestrator

A headless and stateless document synthesis pipeline built with PowerShell, Python, and the Anthropic Claude CLI. This engine automates deterministic LaTeX typesetting and API telemetry tracking for tailored application materials.

## Overview of Resume Building Efficiency

Traditional AI generation tools suffer from prompt drift and context bloat because they rely on continuous conversational memory. This pipeline introduces a strict stateless architecture designed around pure factual data extraction. 

* **Single Source of Truth (`master.md`):** The model never guesses or extrapolates history. It reads a centralized markdown file containing raw verified professional data and maps it cleanly against target job requisitions.
* **Stateless Context Enforcement:** The build orchestrator purges global session history prior to every execution. This eliminates context snowballing and ensures complete isolation between distinct company applications.
* **Deterministic Spatial Guardrails:** Prompt constraints enforce strict line-budgeting and character ceilings during the single-shot generation phase. This guarantees that the output compiles cleanly into a single page via `pdflatex` without margin overflow.

## Core Engineering Highlights

* **Automated CLI Orchestration:** A single PowerShell orchestrator script coordinates virtual environment activation, API generation, metadata extraction, and compilation.
* **Fail-Fast Circuit Breakers:** Integrated exit-code checks halt the pipeline instantly if Claude encounters a JSON parsing error or Python throws a compilation exception.
* **ATS-Compliant Typography:** Configured with specialized ligature suppression rules (`microtype`) and custom `ToUnicode` mapping tables to ensure 100% parseability across enterprise Applicant Tracking Systems.
* **Real-Time Token Telemetry:** Includes an automated Python log parser that extracts input, cache-write, cache-read, payload, and extended-thinking token metrics to render an in-terminal distribution dashboard after every run.

## Project Structure

```text
Resume/
├── archive/               # Target destination for version-controlled job packages
├── output/                # Staging ground for active TeX files and metadata JSON
├── scripts/               # Core Python modules (generate, compile, telemetry tracking)
├── template/              # Read-only LaTeX class files and blueprint templates
├── build.ps1              # Primary PowerShell automation orchestrator
├── instructions.md        # Deterministic prompt rules and formatting geometry
├── master.md              # Template file representing the factual professional data source (example provided in repo)
├── job_listing.txt        # Contains listing for which job should be generated (example provided in repo)


