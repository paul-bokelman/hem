# Hem

Effortless Control, Infinite Possibility — Your Home, Your Way.

## What is Hem?

Hem is an intelligent home assistant designed to simplify and enhance home automation. It allows users to control smart devices, automate tasks, and create custom workflows using voice commands. Hem integrates with various APIs and services, enabling users to define macros (multi-step workflows) and actions for personalized automation.

## Project Structure

### Frontend (`web/`)

The frontend is built with **Next.js** and **React**. It provides the user interface for interacting with Hem, including creating macros, managing actions, and recording audio.

#### Key Directories:

- **`components/`**: Reusable UI components (e.g., buttons, forms, dialogs).
- **`partials/`**: Feature-specific components like `dashboard` and `user-context`.
- **`hooks/`**: Custom React hooks for API interactions and utilities.
- **`app/`**: Next.js pages and layouts for the application.
- **`lib/`**: Utility functions for the frontend.

### Backend (`server/`)

The backend is built with **Flask** and provides APIs for user management, macros, actions, and audio processing. It integrates with external services like OpenWeather, Eleven Labs, and Coingecko.

#### Key Directories:

- **`services/routes/`**: Flask route blueprints for handling API endpoints (e.g., users, macros, actions).
- **`lib/`**: Core logic for processing user requests, converting audio to text, and executing actions.
- **`db/`**: Database models and utilities using **Peewee ORM**.
- **`prompts/`**: Contains the system prompt for the AI assistant.

## Notable Aspects

1. **AI Integration**:

   - Uses **Anthropic's Claude** for natural language understanding and processing.
   - Supports tool-based workflows for executing user-defined macros.

2. **Audio Processing**:

   - Converts audio commands to text using **Vosk**. The `audio_to_text` function in the backend leverages the Vosk speech recognition model to transcribe audio files into text.
   - Converts text responses to audio using **Eleven Labs**. The `text_to_audio` function generates speech from text using Eleven Labs' API and returns the audio as an MP3 file.

3. **Custom Actions and Macros**:

   - Users can define workflows (macros) combining multiple actions.
   - Actions are dynamically loaded and can be extended via the backend.

4. **Database**:

   - Uses **PostgreSQL** for persistent storage.
   - Models are defined using **Peewee ORM**.

5. **Frontend-Backend Communication**:
   - The frontend communicates with the backend via REST APIs.
   - CORS is enabled to allow cross-origin requests.

## Installation, Build, and Run

### Prerequisites:

- **Node.js** (for the frontend)
- **Python 3.12** (for the backend)
- **PostgreSQL** (for the database)

### 1. Install Dependencies

Run the following commands in the project root:

```bash
# Install backend dependencies
make install-server

# Install frontend dependencies
make install-web
```

### 2. Setup Environment Variables

Create a `.env` file in the `server/` directory and add the following variables:

```env
ADMIN_API_KEY=your_admin_key
DATABASE_URL=postgresql://username:password@localhost:5432/hem
ANTHROPIC_API_KEY=your_anthropic_key
OPEN_WEATHER_API_KEY=your_openweather_key
ELEVEN_LABS_API_KEY=your_elevenlabs_key
MARKET_STACK_API_KEY=your_marketstack_key
```

Create a `.env.local` file in the `web/` directory and add the following variables:

```env
NEXT_PUBLIC_API_URL=http://localhost:2512
```

### 3. Run the Project

To start both the frontend and backend in development mode:

```bash
make dev
```

This will:

- Start the backend on http://localhost:2512.
- Start the frontend on http://localhost:3000.

### 4. Run in Production Mode

To build and run the project in production mode:

```bash
make prod
```

## Deployment Details

- Frontend: Vercel (hem.pab.dev)
- Backend: Railway (server-hem.pab.dev)

## Screenshots

<sub>Homepage</sub>
![Homepage](./static/hem-homepage.png)

<sub>Homepage Recording</sub>
![Homepage Recording](./static/hem-homepage-recording.png)

<sub>Dashboard</sub>
![Dashboard](./static/hem-dashboard.png)

<sub>Dashboard</sub>
![Dashboard](./static/hem-create-macro.png)
