from models.database import Stock


class StockService:

    @staticmethod
    def get_all_stock(db):
        stocks = db.query(Stock).all()

        return [stock.to_dict() for stock in stocks]

    @staticmethod
    def get_stock_by_location(location_id, db):

        stocks = db.query(Stock).filter(
            Stock.location_id == location_id
        ).all()

        return [stock.to_dict() for stock in stocks]