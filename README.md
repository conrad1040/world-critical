# World Critical

World Critical is a backend system designed to identify the most important events currently happening in the world.

It is not intended to be a traditional news application. Instead of showing an endless stream of articles, categories, opinions, and notifications, World Critical groups reporting into real-world events and displays only events that exceed a defined importance threshold.

The core question World Critical attempts to answer is:

> Has anything happened that is important enough that an informed person should know about it?

## Problem

Traditional news applications are designed around articles, publication volume, recency, and user engagement.

This creates several problems:

* The same event appears as many separate articles.
* Important events compete with entertainment and low-impact stories.
* Users are encouraged to keep scrolling.
* Heavy media coverage can appear more important than actual consequences.
* Users are rarely told when they are fully caught up.

World Critical is designed to provide a finite, explainable report rather than an endless feed.

## Core Principles

### Events, Not Articles

Articles are treated as evidence about a real-world event.

Multiple articles describing the same occurrence should update one event rather than create multiple feed entries.

### Importance, Not Popularity

Events are selected based on estimated consequences, not clicks, social-media activity, publication volume, or public attention.

### No Forced Content

World Critical does not need to display a fixed number of events.

If only three events exceed the threshold, the report should contain three events.

If no new events qualify, the system should say so.

### Explainable Decisions

Every published event should include the factors that caused it to qualify.

The system should store the component scores, evidence, confidence level, and reasoning used to calculate the final importance score.

### Meaningful Updates Only

A new article should update an existing event only when it adds materially new information.

Repeated reporting or minor commentary should not trigger a new event or user-facing update.

## Phase One Goal

Phase One will build a backend-only prototype that can:

1. Retrieve recent news articles from one provider.
2. Normalize and store the articles.
3. Detect exact and near-duplicate articles.
4. Group articles describing the same real-world event.
5. Create a neutral summary of each event.
6. Evaluate event credibility.
7. Score event importance using a transparent algorithm.
8. Publish only events that exceed the importance threshold.
9. Update existing events when meaningful new information appears.
10. Produce a terminal and JSON report of qualifying events.

## Phase One Does Not Include

* Mobile applications
* User accounts
* Personalization
* Local-news weighting
* Push notifications
* Comments
* Advertising
* Payments
* Social features
* A production frontend
* Real-time streaming infrastructure

## Initial Technical Direction

The Phase One backend is expected to use:

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Docker
* pytest
* Git

AI services may later be used for article matching, event summaries, structured scoring, and material-change detection.

The final importance score and threshold decision will be calculated by normal application code rather than being decided directly by an AI model.

## Project Status

World Critical is currently in the initial project setup and design stage.
