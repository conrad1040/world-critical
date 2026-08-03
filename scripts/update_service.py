from app.services.importance_scoring_service import update_importance_scores
scores_updated = update_importance_scores()
print(f"Importance scores updated: {scores_updated}")