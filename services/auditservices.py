from models.database import AuditLog

class AuditService:

    @staticmethod
    def create_log(user_id, action, details, db):

        log = AuditLog(user_id=user_id, action=action, details=details)

        db.add(log)
        db.commit()

        return log

    @staticmethod
    def get_logs(db):

        logs = db.query(AuditLog).order_by(
            AuditLog.created_at.desc()
        ).all()

        return [log.to_dict() for log in logs]