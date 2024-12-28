from db.queries.core.SyncCore import SyncCore
from db.queries.orm.SyncORM import SyncORM
from core.logger import app_logger, error_logger, access_logger


if __name__ == "__main__":
    SyncORM.create_tables()
    SyncCore.insert_quotes()
    SyncORM.select_workers_with_joined_relationship()
    SyncORM.select_workers_with_lazy_relationship()
    SyncORM.select_workers_with_selectin_relationship()

    app_logger.info("Приложение запущено")
    error_logger.error("Произошла ошибка")
    access_logger.info("Получен запрос GET /authors")
    