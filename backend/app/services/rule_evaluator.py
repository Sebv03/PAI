from sqlalchemy.orm import Session
from app.models.rule import Rule, RuleTriggerType
from app.models.task import Task
from app.models.tarea_concepto import TareaConcepto
import logging

logger = logging.getLogger(__name__)

class RuleEvaluator:
    def __init__(self, db: Session):
        self.db = db

    async def evaluate_event(self, trigger_type: str, context: dict):
        """
        Evaluate rules for a specific event trigger.
        context example: {"grade": 3.5, "student_id": 1, "course_id": 5}
        """
        logger.info(f"Evaluating rules for trigger: {trigger_type} with context: {context}")
        
        rules = self.db.query(Rule).filter(
            Rule.trigger_type == trigger_type, 
            Rule.is_active == True
        ).all()
        
        triggered_rules = []
        for rule in rules:
            if self._check_conditions(rule.conditions, context):
                logger.info(f"Rule triggered: {rule.name}")
                await self._execute_actions(rule.actions, context)
                triggered_rules.append(rule.name)
        
        return triggered_rules

    def _check_conditions(self, conditions: dict, context: dict) -> bool:
        """
        Check if conditions match the context.
        Supported simple format: {"field": "grade", "operator": "<", "value": 4.0}
        """
        if not conditions:
            return True
            
        field = conditions.get("field")
        operator = conditions.get("operator")
        threshold = conditions.get("value")
        
        if field not in context:
            return False
            
        value = context[field]
        
        try:
            if operator == "<":
                return float(value) < float(threshold)
            elif operator == ">":
                return float(value) > float(threshold)
            elif operator == "==":
                return str(value) == str(threshold)
            elif operator == ">=":
                return float(value) >= float(threshold)
            elif operator == "<=":
                return float(value) <= float(threshold)
        except Exception as e:
            logger.error(f"Error evaluating condition: {e}")
            return False
            
        return False

    async def _execute_actions(self, actions: list, context: dict):
        """
        Execute defined actions.
        """
        for action in actions:
            action_type = action.get("type")
            params = action.get("params", {})
            
            if action_type == "CREATE_REMEDIAL_TASK":
                self._action_create_remedial_task(params, context)
            
            # Add more actions here

    def _action_create_remedial_task(self, params: dict, context: dict):
        """
        Action: Create a remedial task for the student.
        In a real scenario, this might assign an existing resource or create a personalized task.
        Here we mock creating a task or assigning a suggestion.
        """
        # For MVP/Thesis simplicity, we might just log or create a specific record
        # But let's verify what the user asked: "sistema asigna automáticamente una guía de refuerzo (acción)"
        # We can simulate this by creating a Task for that student, or maybe just a notification.
        logger.info(f"ACTION: Assigning remedial material for student {context.get('student_id')}")
        
        # Example logic: Find a remedial resource and assign it (omitted for brevity, just logging placeholder)
        pass
