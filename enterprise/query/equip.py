try:
    from . import db
except Exception as e:
    import db

__all__ = ['get_lastendtime']



class FDA:
    """INNOUX db
    
    Here just get the lastendtime to check the equipmnet flow
    """
    def __int__(self, *, equipment):
        self.equipment = equipment

    def get_lastendtime(self):
        cursor = db.get_cursor()
        cursor.execute(
            """
            SELECT "apname", "enabled" FROM "lastendtime"
            WHERE TOOLID = %(equipment)s
            """,
            {'equipment': self.equipment.upper()},
        )
        rows = cursor.fetchall()
        return rows
