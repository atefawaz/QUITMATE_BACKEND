from auth_services.database import engine, Base
Base.metadata.create_all(bind=engine)
