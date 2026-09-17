# MyBigProject

## AI-Powered Software Engineering Agent

MyBigProject is a modular AI software engineering agent designed to assist with real-world development workflows.

The system combines codebase analysis, task-aware context retrieval, multi-provider AI routing, structured planning, implementation proposal generation, and code validation into a unified development workflow.

The architecture is designed to evolve toward a reliable, project-aware coding agent rather than a conventional conversational AI application.

---

## Engineering Overview

```text
Developer Task
      │
      ▼
┌─────────────────────┐
│    Coding Agent     │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Project Context     │
│ Builder             │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Codebase Analyzer   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│     AI Router       │
│                     │
│ Task Classification │
│ Provider Routing    │
│ Fallback Handling   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│      Planner        │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Implementation      │
│ Engine              │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Change Validator    │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Controlled Execution│
└─────────────────────┘
Core Capabilities
Multi-Provider AI Architecture
The system uses a provider abstraction layer so AI services can be integrated without coupling the core agent to a single provider.
Current provider integrations include:
- OpenAI
- Google Gemini
- Groq
Provider selection and fallback are handled through a centralized routing layer.
Codebase-Aware Context Retrieval
Instead of sending the entire repository to the model for every request, the system:
- Analyzes the project structure
- Identifies relevant source files
- Scores files against the developer task
- Retrieves task-specific context
- Applies context-size limits
This provides the model with targeted project information while reducing unnecessary context.
Structured Task Planning
Development tasks are converted into structured execution plans containing controlled actions:
- understand
- inspect
- implement
- test
- report
Plans are validated before entering the execution layer.
Implementation Proposals
The implementation layer generates structured change proposals containing:
- Target file
- Description of the change
- Complete proposed file content
Generated proposals are validated before proceeding toward modification.
Code Validation
The validation layer currently performs checks including:
- Project-path validation
- Protected-file protection
- Code-size limits
- Placeholder detection
- Python syntax validation
AI-generated changes are currently treated as proposals rather than being blindly written to the project.
Technology Stack
- Python
- OpenAI API
- Google Gemini API
- Groq API
- Git
- Visual Studio Code
Project Architecture
MyBigProject/
│
├── agent/
│   └── coding_agent.py
│
├── config/
│   └── loader.py
│
├── core/
│   ├── analyzer/
│   │   ├── codebase_analyzer.py
│   │   └── project_context.py
│   │
│   ├── executor/
│   │   └── agent_executor.py
│   │
│   ├── implementer/
│   │   ├── code_implementer.py
│   │   ├── change_validator.py
│   │   └── change_writer.py
│   │
│   ├── planner/
│   │   └── planner.py
│   │
│   ├── ai_router.py
│   └── tool_registry.py
│
├── providers/
│   ├── base_provider.py
│   ├── openai_provider.py
│   ├── gemini_provider.py
│   ├── groq_provider.py
│   └── provider_factory.py
│
├── tools/
│   ├── filesystem/
│   │   └── filesystem_tool.py
│   │
│   └── terminal/
│       └── terminal_tool.py
│
├── workspace/
│
├── .gitignore
├── dell_power_coder.py
└── README.md
Development Workflow
A typical request follows this pipeline:
Task
 ↓
Classification
 ↓
Relevant Context Retrieval
 ↓
Planning
 ↓
Implementation Proposal
 ↓
Validation
 ↓
Review
 ↓
Controlled Execution
 ↓
Testing
The separation between planning, implementation, validation, and execution provides clear boundaries for improving reliability as the system becomes more capable.
Reliability and Safety
The project is being developed with explicit safeguards around AI-generated changes.
Current protections include:
- Environment files excluded from project analysis
- Protected configuration files
- Project-bound filesystem access
- Path traversal protection
- File-size limits
- Generated-code validation
- Python syntax validation
- Controlled terminal execution
- Change proposals separated from automatic modification
- Backup support for file changes
Further hardening is planned before enabling more autonomous execution.
Development Status
Implemented
- Modular AI provider architecture
- Provider factory
- Provider fallback
- Task classification
- Codebase analysis
- Task-aware context retrieval
- Structured planning
- Implementation proposal generation
- Change validation
- Filesystem tooling
- Terminal tooling
- Tool registry
- Agent execution pipeline
In Development
- Robust change-writing workflow
- Human approval and diff review
- Stronger semantic code validation
- Safer command execution
- Dependency and symbol analysis
- Improved repository retrieval
- Persistent project memory
- Automated verification
- Advanced coding workflows
- Developer interface
Engineering Roadmap
The long-term architecture is intended to support increasingly capable software-engineering workflows.
1. Advanced Repository Understanding
- Symbol indexing
- Dependency analysis
- Import relationships
- Structural code search
2. Intelligent Context Management
- Hybrid retrieval
- Relevance ranking
- Context budgeting
- Error-aware retrieval
3. Reliable Code Modification
- Diff generation
- Patch-based changes
- Automated validation
- Test-driven verification
4. Agent Memory
- Project-level knowledge
- Development history
- Persistent task context
5. Advanced Agent Workflows
- Multi-step implementation
- Test execution
- Failure analysis
- Iterative repair
Project Objective
The objective of MyBigProject is to explore the engineering challenges involved in building a capable AI software engineering system with modular architecture, project awareness, controlled execution, and reliable validation.
The project prioritizes engineering depth, reliability, and extensibility over a simple chatbot interface.
Author
Anandh Kanaparthy
Computer Science Engineering Student