from db.queries.core import SyncCore
from db.queries.orm import SyncORM
from core.logger import app_logger, error_logger, access_logger


if __name__ == "__main__":
    # SyncCore.create_tables()
    # SyncCore.insert_data()
    # SyncCore.select_authors()
    # SyncCore.update_author(1, "Антон", "Чехов", "Павлович", "1860-01-29", "1904-07-15", "Русский писатель, прозаик, драматург, публицист, врач, общественный деятель", "chekhov.jpg")
    
    SyncORM.create_tables()
    SyncORM.insert_data()
    SyncORM.select_authors()
    SyncORM.update_author(1, "Антон", "Чехов", "Павлович", "1860-01-29", "1904-07-15", "Русский писатель, прозаик, драматург, публицист, врач, общественный деятель", "chekhov.jpg")

    app_logger.info("Приложение запущено")
    error_logger.error("Произошла ошибка")
    access_logger.info("Получен запрос GET /authors")
    