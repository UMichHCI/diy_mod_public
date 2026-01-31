# DIY-MOD User Study Interface (Reddit Clone)

This is a Next.js application designed to simulate a Reddit feed for the DIY-MOD user studies. It interacts with the DIY-MOD backend to display content and allows researchers to compare "Original" vs. "Transformed" feeds side-by-side.

## Overview

This interface was used in User Study 2 of the paper *"What If Moderation Didn't Mean Suppression?"*. It provides a controlled environment to evaluate the efficacy of content transformations without the variability of a live social media platform.

## Prerequisites

*   Node.js 16+
*   Running DIY-MOD Backend (see root README)

## Setup

1.  **Install Dependencies**:
    ```bash
    npm install
    ```

2.  **Environment Setup**:
    Create a `.env.local` file in this directory:
    ```bash
    NEXT_PUBLIC_API_URL=http://localhost:8001
    NEXT_PUBLIC_DEFAULT_USER_ID=demo-user
    ```

3.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    The application will be available at [http://localhost:3000](http://localhost:3000).

## Project Structure

*   `/app`: Next.js App Router pages.
*   `/components`: UI components (Feed, Post, Sidebar).
*   `/lib`: Utility functions and API clients.

## Connection to Backend

This frontend fetches processed feeds from the Backend API. Ensure the backend is running and you have processed some custom feeds using `process_json_custom_feed.py` (see root README for instructions).
